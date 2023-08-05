# Python code to implement AVL Trees
class TreeNode(): 
	def __init__(self, val): 
		self.val = val 
		self.left = None
		self.right = None
		self.height = 1

# AVL tree class which supports their methods

class AVL_Tree(object): 
	def __init__(self,lists = []):
		self.root = None
		if(lists):
			for val in lists: 
				#print(val,self.root)
				#print()
				self.insert( val )
				#self.preOrder()
	# Recursive function to insert key in 
	# subtree rooted with node and returns 
	# new root of subtree. 
	def insert(self,key):
		self.root = self.ins(self.root , key)

	def ins(self, root, key): 

		# Step 1 - Perform normal BST 
		if not root:
			return TreeNode(key) 
		elif key < root.val: 
		    root.left = self.ins(root.left, key) 
		else: 
		    root.right = self.ins(root.right, key) 

		# Step 2 - Update the height of the  
		# ancestor node 
		root.height = 1 + max(self.getHeight(root.left), 
		                   self.getHeight(root.right)) 

		# Step 3 - Get the balance factor 
		balance = self.getBalance(root) 

		# Step 4 - If the node is unbalanced,  
		# then try out the 4 cases 
		# Case 1 - Left Left 
		if balance > 1 and key < root.left.val: 
		    return self.rightRotate(root) 

		# Case 2 - Right Right 
		if balance < -1 and key > root.right.val: 
		    return self.leftRotate(root) 

		# Case 3 - Left Right 
		if balance > 1 and key > root.left.val: 
		    root.left = self.leftRotate(root.left) 
		    return self.rightRotate(root) 

		# Case 4 - Right Left 
		if balance < -1 and key < root.right.val: 
		    root.right = self.rightRotate(root.right) 
		    return self.leftRotate(root) 

		return root 

	def leftRotate(self, z): 

		y = z.right 
		T2 = y.left 

		# Perform rotation 
		y.left = z 
		z.right = T2 

		# Update heights 
		z.height = 1 + max(self.getHeight(z.left), 
						self.getHeight(z.right)) 
		y.height = 1 + max(self.getHeight(y.left), 
						self.getHeight(y.right)) 

		# Return the new root 
		return y 

	def rightRotate(self, z): 

		y = z.left 
		T3 = y.right 

		# Perform rotation 
		y.right = z 
		z.left = T3 

		# Update heights 
		z.height = 1 + max(self.getHeight(z.left), 
						self.getHeight(z.right)) 
		y.height = 1 + max(self.getHeight(y.left), 
						self.getHeight(y.right)) 

		# Return the new root 
		return y 

	def getHeight(self, root): 
		if not root: 
			return 0

		return root.height 

	def getBalance(self, root): 
		if not root: 
			return 0

		return self.getHeight(root.left) - self.getHeight(root.right) 

	def preOrder(self ):
		self.pre(self.root)

	def pre(self, root ):
		if not root: 
			return

		print("{0} ".format(root.val), end="-") 
		self.pre(root.left) 
		self.pre(root.right) 

	def delete(self,key):
		self.root = self.dele(self.root,key)

	def dele(self, root, key): 
  
		# Step 1 - Perform standard BST delete 
		if not root: 
		    return root 

		elif key < root.val: 
		    root.left = self.dele(root.left, key) 

		elif key > root.val: 
		    root.right = self.dele(root.right, key) 

		else: 
		    if root.left is None: 
		        temp = root.right 
		        root = None
		        return temp 

		    elif root.right is None: 
		        temp = root.left 
		        root = None
		        return temp 

		    temp = self.getMinValueNode(root.right) 
		    root.val = temp.val 
		    root.right = self.dele(root.right, 
		                              temp.val) 

		# If the tree has only one node, 
		# simply return it 
		if root is None: 
		    return root 

		# Step 2 - Update the height of the  
		# ancestor node 
		root.height = 1 + max(self.getHeight(root.left), 
		                    self.getHeight(root.right)) 

		# Step 3 - Get the balance factor 
		balance = self.getBalance(root) 

		# Step 4 - If the node is unbalanced,  
		# then try out the 4 cases 
		# Case 1 - Left Left 
		if balance > 1 and self.getBalance(root.left) >= 0: 
		    return self.rightRotate(root) 

		# Case 2 - Right Right 
		if balance < -1 and self.getBalance(root.right) <= 0: 
		    return self.leftRotate(root) 

		# Case 3 - Left Right 
		if balance > 1 and self.getBalance(root.left) < 0: 
		    root.left = self.leftRotate(root.left) 
		    return self.rightRotate(root) 

		# Case 4 - Right Left 
		if balance < -1 and self.getBalance(root.right) > 0: 
		    root.right = self.rightRotate(root.right) 
		    return self.leftRotate(root) 

		return root 

	def getMinValueNode(self, root): 
		if root is None or root.left is None: 
		    return root 

		return self.getMinValueNode(root.left) 

'''
# Driver program to test above function 
myTree = AVL_Tree([(i+1)*10 for i in range(6)])
# Preorder Traversal 
myTree.preOrder()
myTree.insert(12)
print("Preorder traversal of the", "constructed AVL tree is") 
myTree.delete(20)
myTree.preOrder() 
# print() 

# This code is contributed by Sai Sanjay'''
