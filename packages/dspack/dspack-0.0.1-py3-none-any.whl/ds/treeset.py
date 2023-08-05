import bisect
from collections import defaultdict 

class TreeSet:
	def __init__(self):
		self.d=defaultdict(lambda:0)
		self.l=[]


	def add(self,value):
		if self.d[value]==0:
			self.d[value]=1
			bisect.insort_left(self.l, value)
			

	def clear(self):
		self.d.clear()
		self.l.clear()
	

	def copy(self):
		return set(self.l.copy())


	def isSubset(self, subset):
		for i in subset:
			if self.d[i]==0:
				return False

		return True


	def pop(self, value):
		if self.d[value]==0:
			return -1 

		else:
			self.d[value]=0 
			return self.l.pop(bisect.bisect_left(self.l, value))


	def remove(self, value):
		if self.d[value]==0:
			return 

		else:
			self.d[value]=0 
			self.l.pop(bisect.bisect_left(self.l, value))
			return


	def __len__(self):
		return len(self.l)

	def __repr__(self):
		res=[]

		for i in self.l:
			res.append(str(i))

		if not res:
			return '{}'

		else:
			return '{'+ ', '.join(res)+'}'




# t=TreeSet()
# t.add(1)
# t.add(2)
# t.add(2)
# t.add(10)
# t.add(3)
# print(t)
# print(len(t))

# print(t.isSubset({3, 10}))

# print(t.pop(10))

# t.remove(1)
# print(t)

# t_c=t.copy()
# print(t_c)