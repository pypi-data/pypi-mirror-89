from collections import OrderedDict


#issubset()

class InorderSet:
    def __init__(self):
        self.d=OrderedDict()

        
    def add(self,value):
        self.d[value]=1
        


    def clear(self):
        self.d.clear()


    def copy(self):
        return self.d.copy()


    def isSubset(self,subset):

        for i in subset:
            try:
                assert self.d[i]==1

            except:
                return False

        return True


    def len(self):
        length=0

        for i in self.d:
            if self.d[i]:
                length+=1

        return length



    def pop(self,value):

        try:
            assert self.d[value]==1
            self.d[value]=0
            return value

        except KeyError:
            return -1


    def remove(self,value):
        try:
            assert self.d[value]==1
            self.d[value]=0
            return 

        except KeyError:
            return 



    def __repr__(self):
        
        l=[]
        for i in self.d:
            if self.d[i]==1:
                l.append(str(i))

        
        if not l:
            return "{}"

        else:
            return '{'+','.join(l)+'}'