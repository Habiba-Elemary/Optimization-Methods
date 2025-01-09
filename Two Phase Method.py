import numpy as np

# Simplex method to solve a linear programming problem
def Simplex(c, A, b):
    # Extract the number of constraints and variables
    NumConstraints, NumVariables = A.shape

    # Create the initial tableau with slack variables and the right-hand side
    Tableau = np.hstack([A, np.eye(NumConstraints), b.reshape(-1, 1)])
    Tableau = np.vstack([Tableau, np.hstack([-c, np.zeros(NumConstraints + 1)])])

    # Start the simplex iterations
    while True:
        # Identify the entering variable (most negative in the objective row)
        PivotCol = np.argmin(Tableau[-1, :-1])
        if Tableau[-1, PivotCol] >= 0:
            # Stop if all entries in the objective row are non-negative
            break

        # Compute the ratios to find the pivot row (smallest positive ratio)
        Ratios = Tableau[:-1, -1] / Tableau[:-1, PivotCol]
        Ratios[Ratios <= 0] = np.inf  # Ignore non-positive ratios
        PivotRow = np.argmin(Ratios)

        # Perform the pivot operation
        PivotElement = Tableau[PivotRow, PivotCol]
        Tableau[PivotRow] /= PivotElement  # Normalize the pivot row
        for i in range(len(Tableau)):
            if i != PivotRow:
                Tableau[i] -= Tableau[i, PivotCol] * Tableau[PivotRow]

    # Extract the solution from the final tableau
    Solution = np.zeros(NumVariables)
    for i in range(NumVariables):
        col = Tableau[:, i]
        if np.count_nonzero(col[:-1]) == 1 and np.isclose(col[-1], 0):
            # If a column corresponds to a basic variable, extract its value
            OneIndex = np.where(col[:-1] == 1)[0][0]
            Solution[i] = Tableau[OneIndex, -1]

    # Return the optimal solution and the optimal value
    return Solution, Tableau[-1, -1]


# Two-Phase method for handling constraints with artificial variables
def TwoPhase(c, A, b):
    # Extract the number of constraints and variables
    NumConstraints, NumVariables = A.shape

    # Add artificial variables to the tableau
    ArtiVars = np.eye(NumConstraints)
    Tableau = np.hstack([A, ArtiVars, b.reshape(-1, 1)])

    # Add the phase-1 objective function to minimize the sum of artificial variables
    Tableau = np.vstack([Tableau, np.hstack([np.zeros(NumVariables), np.ones(NumConstraints), 0])])

    # Phase 1: Eliminate artificial variables
    while True:
        # Identify the entering variable
        PivotCol = np.argmin(Tableau[-1, :-1])
        if Tableau[-1, PivotCol] >= 0:
            # Stop if all entries in the phase-1 objective row are non-negative
            break

        # Compute the ratios to find the pivot row
        Ratios = Tableau[:-1, -1] / Tableau[:-1, PivotCol]
        Ratios[Ratios <= 0] = np.inf  # Ignore non-positive ratios
        PivotRow = np.argmin(Ratios)

        # Perform the pivot operation
        pivot_element = Tableau[PivotRow, PivotCol]
        Tableau[PivotRow] /= pivot_element  # Normalize the pivot row
        for i in range(len(Tableau)):
            if i != PivotRow:
                Tableau[i] -= Tableau[i, PivotCol] * Tableau[PivotRow]

    # Check if the artificial variables have been eliminated (feasibility check)
    if not np.isclose(Tableau[-1, -1], 0):
        print("Infeasible solution due to artificial variables.")
        return None, None

    # Remove artificial variables from the tableau
    Tableau = np.delete(Tableau, np.s_[NumVariables:NumVariables + NumConstraints], axis=1)

    # Phase 2: Solve the original problem using the Simplex method
    return Simplex(c, Tableau[:-1, :-1], Tableau[:-1, -1])


# Example usage of the Two-Phase Method
print("\nTwo-Phase Method Output:")
c = np.array([1, 3])  # Objective function coefficients
A = np.array([[2, -1], [1, 1]])  # Coefficient matrix of constraints
b = np.array([-1, 3])  # Right-hand side vector of constraints

# Solve the problem using the Two-Phase Method
solution, optimal_value = TwoPhase(c, A, b)

# Display results
if solution is not None:
    print("Optimal solution:", solution)
    print("Optimal value:", optimal_value)
