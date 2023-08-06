
class _Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class List:
    def __init__(self):
        self.__head = None

    def __str__(self):
        l = "List : ["
        tmp = self.__head
        while tmp is not None:
            l += str(tmp.data)
            if tmp.next is not None:
                l += " -> "
            tmp = tmp.next
        return l + "]"

    def __len__(self):
        size = 0
        tmp = self.__head
        while tmp is not None:
            tmp = tmp.next
            size += 1
        return size 

    def empty(self):
        return self.__head is None

    def clear(self):
        while not self.empty():
            ptr = self.__head
            self.__head = self.__head.next
            del ptr

    def insert(self, data, pos=0):
        node = _Node(data)
        if self.empty():
            self.__head = node
        elif pos == 0:
            node.next = self.__head
            self.__head = node
        elif pos == -1:
            self.append(data)
        else:
            tmp = self.__head
            count = 0
            while tmp is not None and count < pos:
                cur = tmp
                tmp = tmp.next
                count += 1
            cur.next = node
            node.next = tmp
        
    def append(self, data):
        node = _Node(data)
        if self.empty():
            self.__head = node
        else:
            tmp = self.__head
            while tmp.next is not None:
                tmp = tmp.next
            tmp.next = node

    def remove(self, pos=0):
        try:
            tmp = self.__head
            count = 0
            if pos == 0:
                ptr = self.__head
                data = self.__head.data
                self.__head = self.__head.next
                del ptr
                return data
            elif pos == -1:
                while tmp.next is not None:
                    cur = tmp
                    tmp = tmp.next
                data = tmp.data
                cur.next = None
                del tmp
                return data
            while count < pos:
                cur = tmp
                tmp = tmp.next
                count += 1
            deta = tmp.data
            cur.next = tmp.next
            del tmp
            return data
        except Exception as ex:
            print("Error, %s" %ex)
    
    def delete(self, data):
        try:
            while self.__head.data == data:
                ptr = self.__head
                self.__head = self.__head.next
                del ptr
            cur = self.__head
            tmp = cur.next
            while tmp is not None:
                if tmp.data == data:
                    ptr = tmp
                    tmp = tmp.next
                    cur.next = tmp
                    del ptr
                else:
                    cur = tmp
                    tmp = tmp.next
        except Exception as ex:
            print("Error, %s" %ex)

    def first(self):
        try:
            return self.__head.data
        except Exception as ex:
            print("Error, %s" %ex, end=', ')
    
    def last(self):
        try:
            tmp = self.__head
            while tmp.next is not None:
                tmp = tmp.next
            return tmp.data
        except Exception as ex:
            print("Error, %s" %ex, end=', ')

    def find(self, data):
        count = 0
        tmp = self.__head
        while tmp is not None:
            if tmp.data == data:
                count += 1
            tmp = tmp.next
        return count

    def reverse(self):
        prv = None
        cur = self.__head
        nxt = cur.next
        while cur is not None:
            nxt = cur.next
            cur.next = prv
            prv = cur
            cur = nxt
        self.__head = prv
    
    def exchange(self, n):
        for i in range(n):
            self.append(self.remove())

    @classmethod
    def merge(cls, l1, l2):
        try:
            lst = List()
            tmp1 = l1.__head
            tmp2 = l2.__head
            while tmp1 is not None:
                lst.append(tmp1.data)
                tmp1 = tmp1.next
            while tmp2 is not None:
                lst.append(tmp2.data)
                tmp2 = tmp2.next
            del tmp1, tmp2
            return lst
        except Exception as ex:
            print("Error, %s" %ex)

    @classmethod
    def swap(cls, l1, l2):
        bid = List()
        while not l1.empty():
            bid.append(l1.remove())
        while not l2.empty():
            l1.append(l2.remove())
        while not bid.empty():
            l2.append(bid.remove())
        del bid
