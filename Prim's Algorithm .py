#!/usr/bin/env python
# coding: utf-8

# In[1]:


from typing import List, Tuple, Optional

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = [[0] * vertices for _ in range(vertices)]

    def _min_key(self, key: List[float], in_mst: List[bool]) -> Optional[int]:
        best_val = float("inf")
        best_idx: Optional[int] = None
        for v in range(self.V):
            if not in_mst[v] and key[v] < best_val:
                best_val = key[v]
                best_idx = v
        return best_idx

    def prim_mst(self, start: int = 0) -> Tuple[List[Tuple[int, int, int]], int]:
        key = [float("inf")] * self.V
        parent = [-1] * self.V
        in_mst = [False] * self.V

        key[start] = 0

        for _ in range(self.V):
            u = self._min_key(key, in_mst)
            if u is None:  # graph not fully connected
                break
            in_mst[u] = True

            for v in range(self.V):
                w = self.graph[u][v]
                if w > 0 and not in_mst[v] and w < key[v]:
                    key[v] = w
                    parent[v] = u

        edges: List[Tuple[int, int, int]] = []
        total = 0
        for v in range(self.V):
            u = parent[v]
            if u != -1:
                w = self.graph[u][v]
                edges.append((u, v, w))
                total += w
        return edges, total

    def print_mst(self, edges: List[Tuple[int, int, int]], total: int) -> None:
        print("Edge\tWeight")
        for u, v, w in edges:
            print(f"{u} - {v}\t{w}")
        print(f"Total weight: {total}")

if __name__ == "__main__":
    g = Graph(5)
    g.graph = [
        [0, 2, 0, 6, 0],
        [2, 0, 3, 8, 5],
        [0, 3, 0, 0, 7],
        [6, 8, 0, 0, 9],
        [0, 5, 7, 9, 0],
    ]

    mst_edges, total = g.prim_mst(start=0)
    g.print_mst(mst_edges, total)


# In[ ]:




