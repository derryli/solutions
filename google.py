class Union(object):
	def __init__(self):
		self.id = {}
		self.size = {}
		self.count = 0

	def add(self, node):
		self.id[node] = node
		self.size[node] = 1
		self.count += 1 

	def root(self, node):
		while self.id[node] != node:
			self.id[node] = self.id[self.id[node]] #path compression
			node = self.id[node]
		return node

	def unite(self,node1, node2):
		#put smaller tree under a bigger tree 
		root1, root2 = self.root(node1), self.root(node2)
		if root1 == root2: return
		if self.size[root1] < self.size[root2]: 
			root1, root2 = root2, root1
		self.id[root2] = root1
		self.size[root1] += self.size[root2]
		self.count -= 1

# 146. LRU Cache
#Try double linked list and hash apprach 
class DListNode(object):
	def __init__(self, key=None, val=None):
		self.prev = None 
		self.next = None 
		self.val = val 
		self.key = key
class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.head = DListNode('head')
        self.tail = self.head
        self.node = {}
        self.capacity = capacity
        self.count = 0
        
    def get(self, key):
        """
        :rtype: int
        """
        if key not in self.node: return -1 
        node = self.node[key]
        if node == self.tail:
        	return node.val
        node.prev.next = node.next 
        node.next.prev = node.prev
        self.tail.next = node 
        node.prev = self.tail
        self.tail = node 
        self.tail.next = None 
        return self.tail.val
       
    def set(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: nothing
        """
        if key in self.node:
        	self.get(key)
        	self.tail.val = value
        else:
        	
        	if self.count < self.capacity:
        		self.count += 1 
        	else:     #pop from front 
        	    if self.head.next == self.tail:
        	        self.node.pop(self.tail.key)
        	        self.head.next = None 
        	        self.tail.prev = None 
        	        self.tail = self.head 
        	    else:
        	        rm = self.head.next
        	        self.head.next = rm.next 
        	        rm.next.prev = self.head 
        	        self.node.pop(rm.key)
        	        rm.prev = None
        	        rm.next = None 
        	temp = DListNode(key, value)
        	self.node[key] = temp
        	self.tail.next = temp
        	temp.prev = self.tail 
        	self.tail = self.tail.next


class Solution(object):
# 66. Plus One
	def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        if not digits: return []
        remainder = 1 
        for i in range(len(digits)-1, -1, -1):
        	cur = remainder + digits[i]
        	digits[i] = cur % 10
        	remainder = cur // 10
        	if remainder == 0: return digits
        if remainder != 0:
        	digits.insert(0, remainder)
        return digits

# 200. Number of Islands
	def numIslandsDFS(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """
        def dfs(i,j):
        	if i < 0 or i >= m or j < 0 or j >= n: return  #checking if out of the bound
        	if grid[i][j] == '0': return 
        	grid[i][j] = '0'     #visit current pos
        	for di,dj in (1,0),(-1,0),(0,1),(0,-1): #checking if 4 neighbors are not visited 
        		dfs(i+di,j+dj)
        if not grid or not grid[0]: return 0
        m,n = len(grid), len(grid[0])
        res = 0
        for i in range(m):
        	for j in range(n):
        		if grid[i][j] == '1':
        			dfs(i,j)
        			res += 1
       	return res 

    def numIslands(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """
        if not grid or not grid[0]: return 0
       	m,n = len(grid), len(grid[0])
       	islands = Union()
       	for i in range(m):
       		for j in range(n):
       			if grid[i][j] == '1':
       				node = (i,j)
       				islands.add(node)
       				for di, dj in (1,0),(-1,0),(0,1),(0,-1):
       					temp = (i+di, j+dj)
       					if temp in islands.id:
       						islands.unite(temp, node)
       	return islands.count
    
















