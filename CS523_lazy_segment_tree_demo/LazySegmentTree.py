class SegmentTree:
    def __init__(self):
        self.n = 0 #Số phần tử mảng = số node lá
        self.arr = [0]  #Mảng chứa giá trị
        self.tree = [0]  #Cây
        self.lazy = [0]  #Giá trị lazy
        self.trace = []

    def _build(self, i, tl, tr):
        #i: vị trí node hiện tại
        #tl: vị trí phần tử trái nhất mà node quản lý của mảng
        #tr: vị trí phần tử phải nhất mà node quản lý của mảng

        if tl == tr:
            self.tree[i] = self.arr[tl]
        else:
            mid = (tl + tr) // 2
            self._build(i * 2 + 1, tl, mid)
            self._build(i * 2 + 2, mid + 1, tr)
            self.tree[i] = self.tree[i * 2 + 1] + self.tree[i * 2 + 2]

    def _push(self, i, tl, tr):
        #i: vị trí node hiện tại
        #tl: vị trí phần tử trái nhất mà node quản lý của mảng
        #tr: vị trí phần tử phải nhất mà node quản lý của mảng

        if self.lazy[i] != 0:
            self.tree[i] += (tr - tl + 1) * self.lazy[i]
            if tl != tr:
                self.lazy[i * 2 + 1] += self.lazy[i]
                self.lazy[i * 2 + 2] += self.lazy[i]
            self.lazy[i] = 0

    def _update(self, i, tl, tr, l, r, val):
        #i: vị trí node hiện tại
        #tl: vị trí phần tử trái nhất mà node quản lý của mảng
        #tr: vị trí phần tử phải nhất mà node quản lý của mảng
        #l: vị trí phần tử trái nhất của mảng cần update
        #r: vị trí phần tử trái nhất của mảng cần update
        #val: giá trị update

        self._push(i, tl, tr)

        if l > r:
            return
        
        if tl == l and tr == r:
            self.tree[i] += (tr - tl + 1) * val
            self.trace.append(i)
            if tl != tr:
                self.lazy[i * 2 + 1] += val
                self.lazy[i * 2 + 2] += val

                self.trace.append(i * 2 + 1)
                self.trace.append(i * 2 + 2)
        else:
            if tl <= l or r <= tr:
                self.trace.append(i)
            mid = (tl + tr) // 2
            self._update(i * 2 + 1, tl, mid, l, min(r, mid), val)
            self._update(i * 2 + 2, mid + 1, tr, max(l, mid + 1), r, val)
            self.tree[i] = self.tree[i * 2 + 1] + self.tree[i * 2 + 2]

    def _query(self, i, tl, tr, l, r):
        #i: vị trí node hiện tại
        #tl: vị trí phần tử trái nhất mà node quản lý của mảng
        #tr: vị trí phần tử phải nhất mà node quản lý của mảng
        #l: vị trí phần tử trái nhất của mảng cần query
        #r: vị trí phần tử trái nhất của mảng cần query

        self._push(i, tl, tr)

        if l > r:
            return 0
        
        if tl == l and tr == r:
            self.trace.append(i)
            return self.tree[i]
        
        if tl <= l or r <= tr:
            self.trace.append(i)
        mid = (tl + tr) // 2
        return self._query(i * 2 + 1, tl, mid, l, min(r, mid)) + self._query(i * 2 + 2, mid + 1, tr, max(l, mid + 1), r)

    def build(self, arr):
        self.n = len(arr) #Số phần tử mảng = số node lá
        self.arr = arr  #Mảng chứa giá trị
        self.tree = [0] * (4 * len(arr))  #Cây
        self.lazy = [0] * (4 * len(arr))  #Giá trị lazy
        self.trace = []

        self._build(0, 0, len(self.arr) - 1)

    def update(self, l, r, val):
        #l: vị trí phần tử trái nhất của mảng cần update
        #r: vị trí phần tử trái nhất của mảng cần update
        #val: giá trị update

        if r < 0 or self.n <= l or l > r or l < 0 or self.n <= r:
            return "Index out of range"

        self.trace = []
        
        self._update(0, 0, len(self.arr) - 1, l, r, val)
        return ""

    def query(self, l, r):
        #l: vị trí phần tử trái nhất của mảng cần query
        #r: vị trí phần tử trái nhất của mảng cần query

        if r < 0 or self.n <= l or l > r or l < 0 or self.n <= r:
            return "Index out of range"
        
        self.trace = []
        return self._query(0, 0, len(self.arr) - 1, l, r)
