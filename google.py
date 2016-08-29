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

# 354. Russian Doll Envelopes
    # Sort and dp approach -> Time limit exceeded
    # Sort and binary search 
    # also a good way to find longest increasing sequence
    def maxEnvelopes(self, envelopes):
        """
        :type envelopes: List[List[int]]
        :rtype: int
        """
        import bisect 
        if not envelopes: return 0
        def foo(x,y):
            if x[0] == y[0]:
                return y[1] - x[1]
            else:
                return x[0] - y[0]
        envelopes = sorted(envelopes, cmp=foo)
        dp = [0]*len(envelopes)
        res = 0 
        for item in envelopes:
            index = bisect.bisect_left(dp, item[1], 0, res)
            dp[index] = item[1]
            if index == res: res += 1
        return res

# 363. Max Sum of Rectangle No Larger Than K
# def maxSumSubmatrix(self, matrix, k):
#         """
#         :type matrix: List[List[int]]
#         :type k: int
#         :rtype: int
#         """

# 373. Find K Pairs with Smallest Sums
    #1 get cartesian product and sort on sum 
    #2 use heap 
    def kSmallestPairs(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: List[List[int]]
        """
        
        import heapq 
        def push(i,j):
            if i < len(nums1) and j < len(nums2):
                heapq.heappush(heap, (nums1[i]+nums2[j], i, j))
        heap = []
        push(0,0)
        res = []
        while heap and len(res) < k:
            _,x,y = heapq.heappop(heap)
            res.append([nums1[x],nums2[y]])
            push(x,y+1)
            if y == 0:
                push(x+1,y)
        return res

        # import itertools
        # return sorted(itertools.product(nums1, nums2), key=sum)[:k]

# 388. Longest Absolute File Path
    # clarify: four consecutive white space count as a tab so we need to use number of space as layer
    # number 
    def lengthLongestPath(self, input):
        """
        :type input: str
        :rtype: int
        """
        if not input: return 0
        if '.' not in input: return 0 
        tokens = input.split('\n')
        stack = []  #(layer, len)
        cur = res = 0 
        for token in tokens:
            temp = token.lstrip('\t')
            layer = len(token) - len(temp)
            if stack:
                while stack and stack[-1][0] >= layer:
                    _, rm = stack.pop()
                    cur -= (rm)
            stack.append((layer, len(token)+1))
            cur += len(token)+1
            if '.' in token:
                res = max(res, cur)
        return res-1
    
















