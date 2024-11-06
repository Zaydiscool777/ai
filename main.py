#/bin/python3

# from math import *
import random as rng

#print('beginning software...')
#print('defining global functions...')


def lerp(given,
         goal):  # small general partition of the future reinforcement function
	return (given * .5) + (goal * .5)


"""sig = lambda x: 1 / (1 + exp(-x))
isig = lambda x: -log(() - 1)"""
aid = lambda x: x  # aid for activator id because id already has a function
iaid = lambda x: x
snd = lambda x: x  # standard normal distribution wip

print('getting classy...')


class Returner:  # to allow input and output of a neuron

	def __init__(self, value=0):
		self.r = value

	def __call__(self):
		return self.r


class Neuron(Returner):

	def __init__(self, cons=[]):
		super().__init__()
		self.cons = cons  # input
		self.w = [rng.random] * len(cons)
		self.w = list(map((lambda x: x() * 20 - 10), self.w))
		self.b = rng.random() * 20 - 10

	def comp(self):
		x = 0
		for i in enumerate(self.cons):
			x += i[1]() * self.w[i[0]]
		x += self.b
		self.r = aid(x)
		return self.r

	def train(self, expected):
		self.b += lerp(self.b, expected - self.comp())  # b1 = b + (o1 - o)
		for i in self.w:
			pass  # evol route = true

	def link(self, con):
		self.__init__(self.cons + con)


class RLayer:

	def __init__(self, rs):  # rs -> list of Returner
		self.rs = rs


class Layer(RLayer):

	def __init__(self, ns, con):
		super().__init__(ns)
		self.con = con
		for i in self.rs:
			i.link(self.con.rs)


class PLayer(Layer):

	def __init__(self, len, con):
		super().__init__(([Neuron()] * len), con)


#class Thingy:
#	def __init__

print('evaluating tests...')

ai = []
ai.append([Returner(1), Returner(2), Returner(3)])
ai.append(Neuron(ai[0]))
ai[1].w = [1 / 3] * 3

print('test 1: use pre-made perceptron: expected: 2.0; actual: ' +
      str(ai[1].comp()))
print("note: added randomization. not 2 anymore...")

ai = []
ai.append(RLayer([Returner(1), Returner(2), Returner(3)]))
ai.append(PLayer(3, ai[0]))
ai.append(Neuron(ai[1].rs))
