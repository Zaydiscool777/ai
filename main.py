# import math

print('beginning software...')
print('defining global functions...')

def lerp(given, goal): # small general partition of the future reinforcement function
	return (given*.5)+(goal*.5)
"""sig = lambda x: 1 / (1 + math.exp(-x))
isig = lambda x: -math.log(() - 1)"""
aid = lambda x: x # aid for activator id because id already has a function
iaid = lambda x: x

print('getting classy...')

class Returner: # to allow input and output of a neuron
	def __init__(self, value=0):
		self.r = value
	def __call__(self):
		return self.r

class Neuron(Returner):
	def __init__(self, cons: list):
		super().__init__()
		self.cons = cons # input
		self.w = [1] * len(cons)
		self.b = 0
	def comp(self):
		x = 0
		for i in enumerate(self.cons):
			x += i[1]() * self.w[i[0]]
		x += self.b
		self.r = aid(x)
		return self.r
	def train(self, expected):
		self.b += lerp(self.b, expected - comp()) # b1 = b + (o1 - o)
		for i in self.w:
			pass

print('evaluating tests...')

ai = []
ai.append([Returner(1), Returner(2), Returner(3)])
ai.append(Neuron(ai[0]))
ai[1].w = [1/3] * 3

print('test 1: use pre-made perceptron: expected: 2.0; actual: ' + str(ai[1].comp()))


