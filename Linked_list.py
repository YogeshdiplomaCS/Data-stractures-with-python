class node:
    def __init__ (self,data):
        self.data = data
        self.next = None

class singlylinkedlist:
    def __init__ (self):
        self.first = None
    def insertfirst(self,data):
        temp = node(data)
        temp.next = self.first
        self.first = temp
    def removefirst(self):
        if (self.first == None):
            print("Nothing to remove")
        else:
            cur= self.first
            self.first = self.first.next
            print("Removed first node",cur.data)
    def disply(self):
        if(self.first == None):
            print("Nothing to display")
            return
        cur = self.first
        while(cur):
            print(cur.data, end=" ")
            cur = cur.next
    def search(self,item):
        if(self.first == None):
            print("Nothing to display")
            return
        cur = self.first
        while cur!=None:
            if cur.data == item:
                return cur
            else:
                cur = cur.next
        print("Item is not present in the linkd list")
sll=singlylinkedlist()
while(True):
    ch=int(input("\n Enter the choice 1-insert 2-delete 3-display 4-display 5-exit: "))
    if(ch==1):
        item=int(input("Enter the item to insert: "))
        sll.insertfirst(item)
        sll.disply()
    elif(ch==2):
        sll.removefirst()
        sll.disply()
    elif(ch==3):
        item=input("Enter item to search: ")
        sll.search(item)
    elif(ch==4):
        sll.disply()
    elif(ch==5):
        break
    else:
        print("Invalid choice")
