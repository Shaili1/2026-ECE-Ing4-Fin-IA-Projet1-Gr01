from solve_coloring import solve_k_coloring, solve_min_coloring

nodes = [0, 1, 2]
edges = [(0, 1), (1, 2), (0, 2)]

sol2, info2 = solve_k_coloring(nodes, edges, 2)
sol3, info3 = solve_k_coloring(nodes, edges, 3)
km, solm, _ = solve_min_coloring(nodes, edges)

print("k=2", info2.status, sol2)
print("k=3", info3.status, sol3)
print("min", km)
