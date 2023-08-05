class Node():                                                   #Declaring the node of the tree
    def __init__(self,val = None,left = None,right = None):     
        self.val = val
        self.min = val
        self.max = val
        self.left = left
        self.right = right

class segmenttree():
    def __init__(self,arr = []):
        self.root = None
        self.arr = [i for i in arr]
        self.n = len(arr)
        self.build(arr)         #Declaring the array

    def build(self, arr):
        a = self.arr

        def fun(start,end):
            if(start == end):
                return Node(a[start-1])
            else:
                mid = (start + end) // 2
                l = fun(start,mid)
                r = fun(mid+1,end)
                node = Node(min(l.min,r.min))
                node.max = max(l.max,r.max)
                node.left = l
                node.right = r
                return node

        self.root = fun(1,self.n)                   #Building the segment tree with min and max nodes

    def findmin(self,left = 0,right = None):
        if(right == None): right = self.n-1

        def find(node,start,end,l,r):
            #print(start,end,l,r,node.min)
            if(l>end or r<start): return None
            if(l<=start and r>=end): return node.min

            mid = (start + end) // 2
            lmin = find(node.left,start,mid,l,r)
            rmin = find(node.right,mid+1,end,l,r)
            if(lmin):
                if(rmin):
                    return min(lmin,rmin)
                else:
                    return lmin
            elif(rmin): return rmin
            return None

        return find(self.root,0,self.n-1,left,right)#Find min in the given range [l,r]

    def findmax(self,left = 0,right = None):
        if(right == None): right = self.n-1

        def find(node,start,end,l,r):
            if(l>end or r<start): return None
            if(l>=start and r<=end): return node.max

            mid = (start + end) // 2
            lmax = find(node.left,start,mid,l,r)
            rmax = find(node.right,mid+1,end,l,r)
            if(lmax):
                if(rmax):
                    return max(lmax,rmax)
                else:
                    return lmax
            elif(rmax): return rmax
            return None

        return find(self.root,0,self.n-1,left,right)    #Find max in the given range [l,r] 

    def update(self,index,val):

        def fun(node,start,end,index,val):

            if(start == end):
                self.arr[index] = val
                node.val = node.min= node.max = val

            else:
                mid = (start + end) // 2
                if(start<=index and index<=mid):
                    fun(node.left,start,mid,index,val)
                else:
                    fun(node.right,mid+1,end,index,val)

                node.min = min(node.left.min,node.right.min)
                node.max = max(node.left.max,node.right.max)
                node.val = node.min

        fun(self.root,1,self.n,index,val)               #update value in the array at given index

    def __len__(self):
        return self.n

    def preorder(self,root):
        if(not(root)): return
        print(root.min,root.max,end="||")
        self.preorder(root.left)
        self.preorder(root.right)

    def __repr__(self):
        print(*self.arr)
        self.preorder(self.root)
        print()
        return "Pre-Order arrangement of tree: |node.min node.max|"                     #This will print when we print the tree.

'''
###Segment Tree implementation
my_tree = segmenttree([i+1 for i in range(10)])
print(my_tree.findmin(2,8))                         #Indexing starts with 0 only.
print(my_tree.findmax(3,9))  
my_tree.update(3,13)
print(my_tree.findmin(2,9))
print(my_tree.findmax(3,8))
print(len(my_tree)) 
print(my_tree)'''