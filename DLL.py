class Node:
    def __init__(self, data=None):
        self.data=data
        self.next=None
        self.prev=None
class Doublylinkedlist:
    def __init__(self):
        self.first=None

    def insertatend(self,data):
        temp=Node(data)
        if (self.first==None):
            self.first=temp
        else:
            cur=self.first
            while (cur.next!=None):
                cur=cur.next
            cur.next=temp
            temp.prev=cur

    def deletefirst(self):
        if (self.first==None):
            print("list is empty")
        elif (self.first.next==None):
            print("\nthe deleted item is:", self.first.data)
            self.first=None
        else:
            cur=self.first
            self.first=self.first.next
            self.first.prev=None
            print("\nthe deleted item is:", cur.data)

    def display(self):
        if (self.first==None):
            print("list is empty")
            return
        cur=self.first
        while(cur):
            print(cur.data, end=" ")
            cur=cur.next

    def search(self,item):
        if (self.first==None):
            print("list is empty")
            return
        cur=self.first
        while cur!=None:
            if (cur.data==item):
                print("item is present in list")
                return
            else:
                cur=cur.next
                print("item is not present in list")

dll=Doublylinkedlist()
while(True):
    ch=int(input("\nenter your choice 1-insert 2-delete 3-search 4-display 5-exit :"))
    if ch==1:
        item=int(input("Enter the element you want to insert:"))
        dll.insertatend(item)
        dll.display()
    elif ch==2:
        dll.deletefirst()
        dll.display()
    elif ch==3:
        item=int(input("Enter the element you want to search:"))
        dll.search(item)
    elif ch==4:
        dll.display()
    elif ch==5:
        break
    else:
        print("invalid choice!! ")
