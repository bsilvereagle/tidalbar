class Node:
    def __init__(self, data, prev_node, next_node):
        self.data = data
        self.prev_node = prev_node
        self.next_node = next_node

# Double linked list class
class DoubleLinkedList:

    def __init__(self, data=None):
        # Create the first node of the linked list
        if data:
            new_node = Node(data, None, None)
            self.head = new_node
        else:
            self.head = None

    def __str__(self):
        # Python function to pretty print the list with a * at the head
        result = '\r\n'
        # Take the current head
        old_head = self.head

        # Roll back the active head until we're at the beginning of the list 
        # (prev_node is None)
        while self.head.prev_node:
            self.head = self.head.prev_node
        
        # Roll through printing the data of each node
        while self.head:
            if self.head is old_head:
                result = result +' * ' + str(self.head.data) + '\r\n'
            else:
                result = result +'   ' + str(self.head.data) + '\r\n'
            self.head = self.head.next_node 
        # Retun the head to where it was prior to printing
        self.head = old_head
        return result
    
    # Inserts node after head, no head movement
    def insert(self, data):
        if self.head is None:
            self.head = Node(data, None, None)
        else:
            new_node = Node(data, self.head, self.head.next_node)
            if self.head.next_node:
                self.head.next_node.prev_node = new_node
                self.head.next_node = new_node
            else:
                self.head.next_node = new_node

    # Inserts node after head, moves head forward
    def insertAfter(self, data):
        if self.head is None:
            # If inserting to an empty list, create fresh node
            self.head = Node(data, None, None)
        else:    
            # Insertnode, with edge case that next_node is None
            new_node = Node(data, self.head, self.head.next_node)
            if self.head.next_node:
                self.head.next_node.prev_node = new_node
                self.head.next_node = new_node
            else:
                self.head.next_node = new_node
            self.head = new_node
    # Inserts node before head, moves head backwards
    def insertBefore(self,data):
        if self.head is None:
            # If isnerting to an empty list, create fresh node
            self.head = Node(data, None, None)
        else:
            # Insert node with edge case that prev_node is None
            new_node = Node(data, self.head.prev_node, self.head)
            if self.head.prev_node:
                self.head.prev_node.next_node = new_node
                self.head.prev_node = new_node
            else:
                self.head.prev_node = new_node
            self.head = new_node

    # Appends node at end of list, doesn't tamper with head
    def append(self, data):
        if self.head is None:
            # Empty list, append at head
            self.head = Node(data, None, None)
        else:
            # Save the current head
            old_head = self.head
            # Roll forward
            self.fastforward()
            # No sense reinventing the wheel
            self.insertAfter(data)
            # Reset our head to where it was
            self.head = old_head

    # Prepends node at beginning of list, doesn't tamper with head
    def prepend(self,data):
        if self.head is None:
            # Empty list
            self.head = Node(data, None, None)
        else:
            # Save the current head
            old_head = self.head
            self.rewind()
            self.insertBefore(data)
            # Reset the head
            self.head = old_head

    def remove(self, node):
        # Remove a node by pointing it's previous element at the node's next 
        # and vice versa
        prev_node = node.prev_node
        next_node = node.next_node

        # Couple of fun things here
        #   Could be deleting a non-head node, in which case self.head is left alone
        #   The head could be the node being deleted
        #   The head could be the only node and is being deleted
        #   The prev_node and next_node could be None meaning prev_node.X will fail
    
        # Check to see if prev_node and next_node are None, in which case the head
        # is the only node and is being deleted
        if prev_node is None and next_node is None:
            self.head = None

        if prev_node and next_node:
            # Both nodes exist, standard procedure
            next_node.prev_node = prev_node
            prev_node.next_node = next_node
            if node is self.head:
                self.head = prev_node # Default to prev as the new head
        elif prev_node is None:
            # Deleting the first node in the dll
            next_node.prev_node = None
            if node is self.head:
                self.head = next_node
        elif next_node is None:
            # Deleting the last node in the dll
            prev_node.next_node = None
            if node is self.head:
                self.head = prev_node

        # Explicitly delete the floating node
        del(node)

    # Move the head forward or backward if possiblei and return head data
    def next(self):
        if self.head.next_node:
            self.head = self.head.next_node
            return self.head.data
        else:
            return None

    def prev(self):
        if self.head.prev_node:
            self.head = self.head.prev_node
            return self.head.data
        else:
            return None

    def rewind(self):
        while self.head.prev_node:
            self.head = self.head.prev_node
        return self.head.data

    def fastforward(self):
        while self.head.next_node:
            self.head = self.head.next_node
        return self.head.data
    
    # Return the data at the head
    def current_data(self):
        return self.head.data
    
    # Returna all the data as a list
    def data(self):
        self.rewind()
        results = []
        while self.head:
            results.append(self.head.data)
            self.head = self.head.next_node
        return(results)

    # Move the head to the node whos data matches the search
    def seek(self, data):
        # Trying to keep traversal time to a minimum
        # From the current position roll backwards checking for data
        # if it's found, great. If not, reset head to original position
        # and move forward. 
        starting_node = self.head
        while self.head.prev_node:
            if self.head.data is data:
                return
            else:
                self.head = self.head.prev_node
        # If code reaches here, backwards search failed
        self.head = starting_node
        while self.head.next_node:
            if self.head.data is data:
                return
            else:
                self.head = self.head.next_node
        # If code reaches here, failed. Shouldn't fail silently, but oh well
        self.head = starting_node

if __name__ == '__main__':
    # Run some incomplete tests
    
    # Test1 - Construct a list 'one','two','three','four' with append
    test1 = DoubleLinkedList()
    test1.append('one')
    test1.append('two')
    test1.append('three')
    test1.append('four')
   
    print('Test #1 - Build list with append')
    print('Expected Result: \n* one\n  two\n  three\n  four\n')
    print('Actual result:' + str(test1))

    # Test2 - Construct a list 'one','two','three','four' with prepend
    test2 = DoubleLinkedList()
    test2.prepend('four')
    test2.prepend('three')
    test2.prepend('two')
    test2.prepend('one')

    print('Test #2 - Build list with prepend')
    print('Expected Result: \n  one\n  two\n  three\n* four\n')
    print('Actual result:' + str(test2))

    # Test3 - Construct a list 'one','two','three','four' with prepend
    #         and move head to beginning with .rewind
    test3 = DoubleLinkedList()
    test3.prepend('four')
    test3.prepend('three')
    test3.prepend('two')
    test3.prepend('one')
    test3.rewind()

    print('Test #3 - Move head to start with rewind')
    print('Expected Result: \n* one\n  two\n  three\n  four\n')
    print('Actual result:' + str(test3))

    for item in test3.data():
        print(item)
