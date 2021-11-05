#
# source
#	https://github.com/edenau/minimal-blockchain/blob/master/main.ipynb
# useful
# 	https://docs.python.org/3/library/hashlib.html
#
import copy
import datetime
import hashlib

class MinimalChain():
	def __init__(self):
		self.blocks = [self.get_genesis_block()]
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False
	
	def get_genesis_block(self): 
		return MinimalBlock(0, datetime.datetime.utcnow(), "Genesis", "arbitrary")
	
	def add_block(self, data):
		self.blocks.append(MinimalBlock(len(self.blocks), 
										datetime.datetime.utcnow(), 
										data, 
										self.blocks[len(self.blocks)-1].hash))
	
	def get_chain_size(self): 
		# exclude genesis block
		return len(self.blocks) - 1
	
	def verify(self, verbose=True): 
		flag = True
		for i in range(1, len(self.blocks)):
			# assume Genesis block integrity
			if not self.blocks[i].verify():
				flag = False
				if verbose:
					print(f"Wrong data type(s) at block {i}.")
			if self.blocks[i].index != i:
				flag = False
				if verbose:
					print(f"Wrong block index at block {i}.")
			if self.blocks[i-1].hash != self.blocks[i].previous_hash:
				flag = False
				if verbose:
					print(f"Wrong previous hash at block {i}.")
			if self.blocks[i].hash != self.blocks[i].hashing():
				flag = False
				if verbose:
					print(f"Wrong hash at block {i}.")
			if self.blocks[i-1].timestamp >= self.blocks[i].timestamp:
				flag = False
				if verbose:
					print(f"Backdating at block {i}.")
		return flag
	
	def fork(self, head="latest"):
		if head in ["latest", "whole", "all"]:
			# deepcopy since they are mutable
			return copy.deepcopy(self)
		else:
			c = copy.deepcopy(self)
			c.blocks = c.blocks[0:head+1]
			return c
	
	def get_root(self, chain_2):
		min_chain_size = min(self.get_chain_size(), chain_2.get_chain_size())
		for i in range(1,min_chain_size+1):
			if self.blocks[i] != chain_2.blocks[i]:
				return self.fork(i-1)
		return self.fork(min_chain_size)

class MinimalBlock():
	def __init__(self, index, timestamp, data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hashing()
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False
	
	def hashing(self):
		key = hashlib.sha256()
		key.update(str(self.index).encode("utf-8"))
		key.update(str(self.timestamp).encode("utf-8"))
		key.update(str(self.data).encode("utf-8"))
		key.update(str(self.previous_hash).encode("utf-8"))
		return key.hexdigest()
	
	def verify(self): 
		# check data types of all info in a block
		instances = [self.index, self.timestamp, self.previous_hash, self.hash]
		types = [int, datetime.datetime, str, str]
		if sum(map(lambda inst_, type_: isinstance(inst_, type_), instances, types)) == len(instances):
			return True
		else:
			return False

### Testing
c = MinimalChain()

for i in range(0,20):
	c.add_block(f"This is block {i+1} of my first chain.")

# examples
print("\n= = = = timestamp, data and hash")
print(c.blocks[3].timestamp)
print(c.blocks[7].data)
print(c.blocks[9].hash)

# chain size and verification
print("\n= = = = chain size and verification")
print(c.get_chain_size())
print(c.verify())

# copy current blockchain
print("\n= = = = copy")
c_forked = c.fork("latest")
print(c == c_forked)
c_forked.add_block("New block for forked chain!")
print(c.get_chain_size(), c_forked.get_chain_size())

# conflict testing
print("\n= = = = conflict testing")
c_forked = c.fork("latest")
c_forked.blocks[9].index = -9
c_forked.verify()

c_forked = c.fork("latest")
c_forked.blocks[16].timestamp = datetime.datetime(2000, 1, 1, 0, 0, 0, 0)
c_forked.verify()

c_forked = c.fork("latest")
c_forked.blocks[5].previous_hash = c_forked.blocks[1].hash
c_forked.verify()