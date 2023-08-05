class Node:
	def __init__(self,val = None,prev = None,next = None):
		self.data = val
		self.next = next
		self.prev = prev

class dll:
	def __init__(self,lis = []):
		self.head = None
		for i in lis:
			self.add(i)

	def add(self,val, pos = None):
		if(self.head == None):
			self.head = Node(val)
		else:
			N_node = Node(val)
			if(pos==None):
				t= self.head
				while(t.next): t = t.next
				t.next = N_node
			else:
				if(pos==0):
					N_node.next = self.head
					self.head.prev = N_node
					self.head = N_node
				else:
					t  = prev = self.head
					while(t and pos>0):
						pos-=1
						prev = t
						t = t.next
					N_node.next = prev.next
					if(prev.next):
						prev.next.prev = N_node
					prev.next = N_node
					N_node.prev = prev

	def remove(self,data = None):
		if(self.head == None or data == None): return
		t = self.head
		if(t.data == data):
			self.head = t.next
			if(t.next == None): return
			t.next.prev = None
			t = None
			return
		while(t and t.data != data):
			prevv = t
			t = t.next
		if(t == None): return
		t.next.prev = prevv
		prevv.next = t.next
		t = None
		return

	def getNode(self,data):
		if(self.head == None): return None
		t = self.head
		while(t):
			if(t.data == data):
				return t
			t = t.next
		return None

	def __len__(self):
		length = 0
		node = self.head
		while(node):
			node = node.next
			length += 1
		return length

	def __repr__(self):
		if(self.head == None): return ""
		t = self.head
		element = ''
		while t:
		    element += f'{t.data} <--> '
		    t = t.next
		element += 'None'
		return element

