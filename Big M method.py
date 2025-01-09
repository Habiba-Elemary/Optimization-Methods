import numpy as np
def BigM_Method():
    M = 1e6  # Large value for Big M
    # Step 1: Define the initial Simplex Tableau
    # Variables: x1, x2, s1, s2, a1, RHS
    Tableau = np.array([
        [1, 1, 1, 0, 0, 10],  # Constraint 1: x1 + x2 + s1 = 10
        [1, -1, 0, 1, -1, -2],  # Constraint 2: x1 - x2 + s2 - a1 = -2
        [-2, -1, 0, 0, M, 0]  # Objective function Z = 2x1 + x2 - Ma1
    ], dtype=float)

    NumVariables = 2  # Number of decision variables (x1, x2)
    NumConstraints = Tableau.shape[0] - 1  # Exclude Z-row

    while True:
        print("\nCurrent Tableau:")
        print(Tableau)

        # Step 2: Check for optimality (All values in the objective row are non-negative)
        Z_Row = Tableau[-1, :-1]
        if np.all(Z_Row >= 0):
            print("\nOptimal solution found!")
            break

        # Step 3: Identify entering variable (most negative value in Z-row)
        EnteringIndx = np.argmin(Z_Row)

        # Step 4: Calculate the minimum ratio for the RHS to identify leaving variable
        Ratios = []
        for i in range(NumConstraints):
            if Tableau[i, EnteringIndx] > 0:
                Ratio = Tableau[i, -1] / Tableau[i, EnteringIndx]
            else:
                Ratio = np.inf
            Ratios.append(Ratio)

        LeavingIndx = np.argmin(Ratios)
        if Ratios[LeavingIndx] == np.inf:
            print("The problem is unbounded.")
            return

        # Step 5: Pivot operation
        Pivot = Tableau[LeavingIndx, EnteringIndx]
        Tableau[LeavingIndx] /= Pivot

        for i in range(Tableau.shape[0]):
            if i != LeavingIndx:
                RowFactor = Tableau[i, EnteringIndx]
                Tableau[i] -= RowFactor * Tableau[LeavingIndx]

    # Step 6: Extract solution for x1, x2
    Solution = np.zeros(NumVariables)
    for i in range(NumConstraints):
        BasicVariable = np.where(Tableau[i, :NumVariables] == 1)[0]
        if len(BasicVariable) == 1 and BasicVariable[0] < NumVariables:
            Solution[BasicVariable[0]] = Tableau[i, -1]

    print("\nFinal Tableau (Optimal Solution):")
    print(Tableau)

    print("\nSolution for x1 and x2:")
    print(f"x1 = {Solution[0]}, x2 = {Solution[1]}")
    z_opt = 2 * Solution[0] + Solution[1]
    print(f"Optimal Z = {z_opt}")
    return Solution, z_opt


# Run the Big M Simplex method
Solution, optimal_z = BigM_Method()