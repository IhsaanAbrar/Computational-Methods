#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from typing import List, Tuple, Optional

class MinSpanBuilder:
    def __init__(self, n: int):
        self.n = n
        self.links: List[Tuple[int, int, float]] = []

    def add_link(self, a: int, b: int, w: float) -> None:
        self.links.append((a, b, w))

    @staticmethod
    def _locate(root: List[int], i: int) -> int:
        if root[i] != i:
            root[i] = MinSpanBuilder._locate(root, root[i])
        return root[i]
#Ihsaan Abrars code
    @staticmethod
    def _join(root: List[int], height: List[int], x: int, y: int) -> None:
        if height[x] < height[y]:
            root[x] = y
        elif height[x] > height[y]:
            root[y] = x
        else:
            root[y] = x
            height[x] += 1

    def build(self) -> Tuple[List[Tuple[int, int, float]], float]:
        picked: List[Tuple[int, int, float]] = []
        used = 0
        idx = 0
        pool = sorted(self.links, key=lambda t: t[2])
        root = list(range(self.n))
        height = [0] * self.n
        while used < self.n - 1 and idx < len(pool):
            a, b, w = pool[idx]
            idx += 1
            ra = self._locate(root, a)
            rb = self._locate(root, b)
            if ra != rb:
                picked.append((a, b, w))
                used += 1
                self._join(root, height, ra, rb)
        if used != self.n - 1:
            raise ValueError("No MST exists (graph is disconnected).")
        total = sum(w for _, _, w in picked)
        return picked, total


def from_matrix(mat: List[List[Optional[float]]],
                zero_is_none: bool = True,
                upper_only: bool = True) -> MinSpanBuilder:
    n = len(mat)
    g = MinSpanBuilder(n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            w = mat[i][j]
            if w is None:
                continue
            if zero_is_none and w == 0:
                continue
            if upper_only and j <= i:
                continue
            g.add_link(i, j, float(w))
    return g


def _read_matrix() -> List[List[Optional[float]]]:
    def parse_token(tok: str) -> Optional[float]:
        t = tok.strip().lower()
        if t in ("0", "x", "none", "inf"):
            return 0.0
        return float(t)

    n = int(input("Enter number of vertices: ").strip())
    print(f"\nEnter the {n}×{n} distance matrix, one row per line.")
    print("Separate values with spaces or commas. Use 0/x for no edge.\n")

    mat: List[List[Optional[float]]] = []
    for i in range(n):
        row = input(f"Row {i+1}: ").replace(",", " ").split()
        if len(row) != n:
            raise ValueError(f"Row {i+1} must have exactly {n} values.")
        mat.append([parse_token(tok) for tok in row])
    return mat


if __name__ == "__main__":
    try:
        matrix = _read_matrix()
        G = from_matrix(matrix, zero_is_none=True, upper_only=True)
        edges, cost = G.build()
        print("\nEdges in the constructed MST:")
        for a, b, w in edges:
            print(f"{a} -- {b} = {w}")
        print("Minimum Spanning Tree =", cost)
    except Exception as e:
        print("Error:", e)


# In[ ]:




