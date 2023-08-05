class Node:
    def __init__(self,val=None,next=None):
        self.data = val
        self.next = next

class sll:
    # initialize the object with some iterator like list.
    def __init__(self,arr = []):

        self.head = None
        for i in arr: self.add(i)
    # object.add(value,pos) 
    #add method takes two two argumetns data and pos you can send positon arugument if you 
    #need to add element at particular position or by default it appends to the list
    def add(self,data,pos = None):  
        if(self.head==None):
            self.head = Node(data)
        else:
            New_Node = Node(data)
            if(pos==None):
                
                t = self.head
                while(t.next):
                    t = t.next
                t.next = New_Node
            else:
                if(pos==0):
                    New_Node.next = self.head
                    self.head = New_Node
                else:
                    t = prev =  self.head
                    while(t and pos>0):
                        pos-=1
                        prev = t
                        t = t.next
                    New_Node.next = prev.next
                    prev.next = New_Node
                        
    # removes the node in the linked list with the given value.
    def remove(self,data):
        if(self.head==None):
            return
        t = self.head
        if(t.data==data):
            self.head = t.next
            t = None
            return  
        while(t and t.data!=data):
            prev = t
            t = t.next
        if(t==None):return
        prev.next = t.next
        t = None
        return

    #returns reference to the node of the given value
    def getNode(self,data):
        if(self.head==None):return None
        t = self.head
        while(t):
            if(t.data == data):
                return t
            t = t.next
        return None
    # return a reference to the node of popped element from the linked list
    # Default is last node or can be indexed from zero.
    def pop(self,pos=-1):
        if(pos==-1):
            return (self.del_last())
        t = self.head
        if(pos==0):
            self.head = t.next
            a= t.data
            t = None
            return a        
        while(t and pos>0):
            prev = t
            t = t.next
            pos-=1
        if(t==None):return
        if(pos==0):
            prev.next = t.next
            a = t.data
            t = None
            return a

    def del_last(self):
        t = self.head
        if(t==None):return
        while(t.next):
            prev = t
            t = t.next
        prev.next = t.next
        a = t.data
        t = None
        return a

    # len(object) returns the length of the list
    def __len__(self):

        length = 0
        node = self.head
        while(node):
            node = node.next
            length+=1
        return length

    # print(object) to represent the linked list
    def __repr__(self):
        if self.head is None:
            return ''
        t = self.head
        element = ''
        while t:
            element += f'{t.data} -> '
            t = t.next
        element += 'None'
        return element
