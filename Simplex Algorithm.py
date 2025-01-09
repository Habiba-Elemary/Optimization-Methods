import numpy as np
# generates an empty matrix with adequate size for variables and constraints.
def GenMatrix(var,cons):
    Tab = np.zeros((cons + 1, var + cons + 2))
    return Tab

# checks the furthest right column for negative values ABOVE the last row. If negative values exist, another pivot is required.
def NextRound_R(Table):
    m = min(Table[:-1, -1])
    if m>= 0:
        return False
    else:
        return True

# checks that the bottom row, excluding the final column, for negative values. If negative values exist, another pivot is required.
def NextRound(Table):
    NumRows = len(Table[:, 0])
    m = min(Table[NumRows - 1, :-1])
    if m>=0:
        return False
    else:
        return True

# Similar to next_round_r function, but returns row index of negative element in furthest right column
def FindNeg_R(Table):
    # NumCol = number of columns, NumRows = number of rows
    NumCol = len(Table[0, :])
    # search every row (excluding last row) in final column for min value
    m = min(Table[:-1, NumCol - 1])
    if m<=0:
        # n = row index of m location
        n = np.where(Table[:-1, NumCol - 1] == m)[0][0]
    else:
        n = None
    return n

#returns column index of negative element in bottom row
def FindNeg(Table):
    NumRows = len(Table[:, 0])
    m = min(Table[NumRows - 1, :-1])
    if m<=0:
        # n = row index for m
        n = np.where(Table[NumRows - 1, :-1] == m)[0][0]
    else:
        n = None
    return n

# locates pivot element in tableau to remove the negative element from the furthest right column.
def LocPiv_R(Table):
        total = []
        # r = row index of negative entry
        r = FindNeg_R(Table)
        # finds all elements in row, r, excluding final column
        row = Table[r, :-1]
        # finds minimum value in row (excluding the last column)
        m = min(row)
        # c = column index for minimum entry in row
        c = np.where(row == m)[0][0]
        # all elements in column
        col = Table[:-1, c]
        # need to go through this column to find smallest positive ratio
        for i, b in zip(col, Table[:-1, -1]):
            # i cannot equal 0 and b/i must be positive.
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # placeholder for elements that did not satisfy the above requirements. Otherwise, our index number would be faulty.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,c]
# similar process, returns a specific array element to be pivoted on.
def LocPiv(Table):
    if NextRound(Table):
        total = []
        n = FindNeg(Table)
        for i,b in zip(Table[:-1, n], Table[:-1, -1]):
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # placeholder for elements that did not satisfy the above requirements. Otherwise, our index number would be faulty.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,n]

# Takes string input and returns a list of numbers to be arranged in tableau
def Convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i)*-1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq

# The final row of the tableau in a minimum problem is the opposite of a maximization problem so elements are multiplied by (-1)
def ConvertMin(Table):
    Table[-1, :-2] = [-1 * i for i in Table[-1, :-2]]
    Table[-1,-1] = -1 * Table[-1,-1]
    return Table

# generates x1,x2,...xn for the varying number of variables.
def GenVar(Table):
    NumCol = len(Table[0, :])
    NumRows = len(Table[:, 0])
    var = NumCol - NumRows - 1
    v = []
    for i in range(var):
        v.append('x'+str(i+1))
    return v

# pivots the tableau such that negative elements are purged from the last row and last column
def Pivot(row,col,Table):
    # number of rows
    lr = len(Table[:, 0])
    # number of columns
    lc = len(Table[0, :])
    t = np.zeros((lr,lc))
    pr = Table[row, :]
    if Table[row,col]**2>0: #new
        e = 1 / Table[row,col]
        r = pr*e
        for i in range(len(Table[:, col])):
            k = Table[i, :]
            c = Table[i,col]
            if list(k) == list(pr):
                continue
            else:
                t[i,:] = list(k-r*c)
        t[row,:] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

# checks if there is room in the matrix to add another constraint
def AddCons(Table):
    NumRows = len(Table[:, 0])
    # want to know IF at least 2 rows of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(NumRows):
        total = 0
        for j in Table[i, :]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j**2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There are at least 2 rows with all zero elements if the following is true
    if len(empty)>1:
        return True
    else:
        return False

# adds a constraint to the matrix
def Constrain(Table,eq):
    if AddCons(Table) == True:
        NumCol = len(Table[0, :])
        NumRows = len(Table[:, 0])
        var = NumCol - NumRows -1
        # set up counter to iterate through the total length of rows
        j = 0
        while j < NumRows:
            # Iterate by row
            row_check = Table[j, :]
            # total will be sum of entries in row
            total = 0
            # Find first row with all 0 entries
            for i in row_check:
                total += float(i**2)
            if total == 0:
                # We've found the first row with all zero entries
                row = row_check
                break
            j +=1

        eq = Convert(eq)
        i = 0
        # iterate through all terms in the constraint function, excluding the last
        while i<len(eq)-1:
            # assign row values according to the equation
            row[i] = eq[i]
            i +=1
        #row[len(eq)-1] = 1
        row[-1] = eq[-1]

        # add slack variable according to location in tableau.
        row[var+j] = 1
    else:
        print('Cannot add another constraint.')

# checks to determine if an objective function can be added to the matrix
def AddObj(Table):
    NumRows = len(Table[:, 0])
    # want to know IF exactly one row of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(NumRows):
        total = 0
        for j in Table[i, :]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j**2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There is exactly one row with all zero elements if the following is true
    if len(empty)==1:
        return True
    else:
        return False

# adds the objective function to the matrix.
def Obj(Table,eq):
    if AddObj(Table) ==True:
        eq = [float(i) for i in eq.split(',')]
        NumRows = len(Table[:, 0])
        row = Table[NumRows - 1, :]
        i = 0
    # iterate through all terms in the constraint function, excluding the last
        while i<len(eq)-1:
            # assign row values according to the equation
            row[i] = eq[i]*-1
            i +=1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')

# solves maximization problem for optimal solution, returns dictionary w/ keys x1,x2...xn and max.
def MaxZ(Table, output='summary'):
    while NextRound_R(Table) ==True:
        Table = Pivot(LocPiv_R(Table)[0], LocPiv_R(Table)[1], Table)
    while NextRound(Table) ==True:
        Table = Pivot(LocPiv(Table)[0], LocPiv(Table)[1], Table)

    NumCol = len(Table[0, :])
    NumRows= len(Table[:, 0])
    var = NumCol - NumRows -1
    i = 0
    val = {}
    for i in range(var):
        col = Table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[GenVar(Table)[i]] = Table[loc,-1]
        else:
            val[GenVar(Table)[i]] = 0
    val['max'] = Table[-1,-1]
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return Table
    else:
        return val
if __name__ == "__main__":

  m = GenMatrix(2, 3)
  Constrain(m, '1,1,L,4')
  Constrain(m, '1,0,L,3')
  Constrain(m, '0,1,L,2')
  Obj(m, '3,2,0')
  print(MaxZ(m))

