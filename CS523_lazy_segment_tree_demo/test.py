from LazySegmentTree import *

a = [i for i in range(6)]

sgtree = SegmentTree(a)

sgtree.build()

print(sgtree.query(0, len(sgtree.arr) - 1))

print(sgtree.update(0, 0, 10))

print(sgtree.query(0, len(sgtree.arr) - 1))

print(sgtree.query(0, 0))

print(sgtree.arr)

print(sgtree.tree)

print(sgtree.lazy)
