#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys
import string
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Circle

def draw_multigraph_from_adj(adj: np.ndarray, labels, title: str, filename: str):
    n = len(labels)
    if adj.shape != (n, n):
        raise ValueError("adj must be an n×n matrix matching len(labels)")

    G = nx.MultiGraph()
    G.add_nodes_from(labels)

    # Add undirected multiedges
    for i in range(n):
        for j in range(i + 1, n):
            w = int(adj[i, j])
            if w < 0:
                raise ValueError("Negative weights are not supported.")
            for _ in range(w):
                G.add_edge(labels[i], labels[j])

    # Loops (diagonal entries)
    loops = {labels[i]: int(adj[i, i]) // 2 for i in range(n) if int(adj[i, i]) > 0}

    pos = nx.circular_layout(G)

    plt.figure(figsize=(6, 6))
    
    # Draw black nodes with white labels
    nx.draw_networkx_nodes(G, pos, node_size=900, node_color='black', edgecolors='white', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')

    # Draw multiple edges as arcs
    edges = list(G.edges())
    seen_pairs = set()
    for (u, v) in edges:
        pair = tuple(sorted((u, v)))
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        k = sum(1 for e in edges if set(e[:2]) == set(pair))
        if k == 1:
            nx.draw_networkx_edges(G, pos, edgelist=[pair], edge_color='black', width=2)
        else:
            import numpy as _np
            rads = _np.linspace(0.15, 0.5, k)
            signs = [1 if i % 2 == 0 else -1 for i in range(k)]
            for rad, s in zip(rads, signs):
                nx.draw_networkx_edges(
                    G, pos, edgelist=[pair],
                    connectionstyle=f'arc3,rad={s * rad}',
                    edge_color='black', width=2
                )

    # Draw loops as white circles around nodes
    ax = plt.gca()
    for node, count in loops.items():
        (x, y) = pos[node]
        for r in np.linspace(0.08, 0.18, count):
            circ = Circle((x, y), r, fill=False, lw=2, edgecolor='black')
            ax.add_patch(circ)

    plt.title(title, color='black', fontsize=13)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=220, bbox_inches='tight', facecolor='white')
    print(f"\n Saved graph to: {filename}")
    plt.show()


def parse_row(row: str, n: int):
    parts = [p for p in row.replace(',', ' ').split() if p.strip() != '']
    if len(parts) != n:
        raise ValueError(f"Expected {n} integers, got {len(parts)}")
    vals = [int(x) for x in parts]
    if any(v < 0 for v in vals):
        raise ValueError("Use non-negative integers only.")
    return vals


def main():
    print("=== Graph from Adjacency Matrix (Undirected) ===")

    # Number of vertices
    while True:
        try:
            n = int(input("Number of vertices n: ").strip())
            if n <= 0:
                print("n must be positive.")
                continue
            break
        except ValueError:
            print("Please enter an integer.")

    # Labels
    default_labels = list(string.ascii_uppercase[:n])
    custom = input(f"Labels (comma/space separated) [default: {' '.join(default_labels)}]: ").strip()
    if custom:
        labels = [tok for tok in custom.replace(',', ' ').split() if tok]
        if len(labels) != n:
            print(f"Warning: expected {n} labels, got {len(labels)} — using defaults.")
            labels = default_labels
    else:
        labels = default_labels

    # Enter adjacency matrix
    print("\nEnter adjacency matrix row by row.")
    print("Off-diagonal: number of edges between vertices.")
    print("Diagonal: 2m for m loops at that vertex (0 if none).")

    rows = []
    for i in range(n):
        while True:
            try:
                row = input(f"Row {i+1} ({labels[i]}): ")
                vals = parse_row(row, n)
                rows.append(vals)
                break
            except Exception as e:
                print(f"  Error: {e} (try again)")

    adj = np.array(rows, dtype=int)

    # Symmetry check
    if not np.array_equal(adj, adj.T):
        print("\n Warning: matrix not symmetric — converting to symmetric (max(A, Aᵀ))")
        adj = np.maximum(adj, adj.T)

    # Diagonal check
    diag = np.diag(adj)
    if np.any(diag % 2 != 0):
        print(" Warning: diagonal has odd entries — rounding down to make even (loop convention).")
        for i in range(n):
            if adj[i, i] % 2 == 1:
                adj[i, i] -= 1

    title = input("Plot title [optional]: ").strip() or "Graph from adjacency"
    out = input("Output filename [.png] [default: graph.png]: ").strip() or "graph.png"
    if not out.lower().endswith(".png"):
        out += ".png"

    draw_multigraph_from_adj(adj, labels, title, out)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)


# In[ ]:




