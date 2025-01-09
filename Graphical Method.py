import matplotlib.pyplot as plt
import numpy as np
# Define the constraints and the objective function
def graphical_method():
    # Define the inequality lines (boundaries of the constraints)
    x1 = np.linspace(0, 5, 100)  # Generate 100 points for x1 between 0 and 5

    # Constraints
    y1 = 4 - x1       # x1 + x2 ≤ 4 -> x2 = 4 - x1
    y2 = np.full_like(x1, 2)  # x2 ≤ 2 (constant line)
    y3 = np.maximum(3 - x1, 0)  # x1 ≤ 3 (line; values capped at x1=3)

    # Feasible region: minimum of all constraint lines (intersection area)
    y_feasible = np.minimum(y1, y2)
    y_feasible = np.minimum(y_feasible, np.where(x1 <= 3, y1, 0))

    # Plotting the constraints
    plt.figure(figsize=(8, 6))
    plt.plot(x1, y1, label=r'$x_1 + x_2 \leq 4$', color='blue')
    plt.plot(x1, y2, label=r'$x_2 \leq 2$', color='green')
    plt.axvline(x=3, label=r'$x_1 \leq 3$', color='red')

    # Highlight the feasible region
    plt.fill_between(x1, 0, y_feasible, where=(y_feasible >= 0), color='gray', alpha=0.5)

    # Determine vertices of the feasible region
    vertices = [(0, 0), (0, 2), (2, 2), (3, 1), (3, 0)]
    vertices = [v for v in vertices if v[0] <= 3 and v[1] <= 2 and v[0] + v[1] <= 4]

    # Evaluate the objective function at each vertex
    z_values = {v: 3 * v[0] + 2 * v[1] for v in vertices}
    optimal_vertex = max(z_values, key=z_values.get)

    # Plot vertices and optimal point
    for v in vertices:
        plt.scatter(*v, color='orange', label=f"Vertex {v}, Z = {z_values[v]}")
    plt.scatter(*optimal_vertex, color='red', label=f"Optimal Point {optimal_vertex}", s=100)

    # Graph labels and legend
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.title("Graphical Method for Linear Programming")
    plt.legend()
    plt.grid()
    plt.show()

    # Print results
    print("Vertices and their Z values:")
    for v, z in z_values.items():
        print(f"Vertex {v}: Z = {z}")
    print(f"Optimal Solution: Vertex {optimal_vertex}, Z = {z_values[optimal_vertex]}")

# Call the function to solve the problem
graphical_method()
