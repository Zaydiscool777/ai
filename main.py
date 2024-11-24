#!/bin/python3

# from math import *
import random as rng
import numpy as np

print('beginning software...')

print('defining global functions...')

def snd(x):
	return (lambda y: -y if x < 0 else y)\
	((np.exp(-(x**2)/2)/np.sqrt(2*np.pi))*20) # standard normal distribution, tweaked wip

def sig(x):
	return np.reciprocal(1 + np.exp(-x))

def datainit(x): # x is a string that contains only [a-z] atleast once
	return [\
		x[0],
		(lambda x: x[1] if len(x) > 2 else '')(x),
		(lambda x: x[2] if len(x) > 3 else '')(x),
		(lambda x: x[3] if len(x) > 4 else '')(x),
		(lambda x: x[4] if len(x) > 5 else '')(x)
	]

print('extracting data...')

with open('3000.txt') as f: # while i do remember open(), the replit autocomplete showed to use the with clause, which might be favored in this situation? it might make proccessing faster to use open() and close() and read each line seperately...
	data = [datainit(i) for i in f.readlines()]

print('getting classy...')

class Returner:  # to allow input (and output? no) of a neuron
	def __init__(self, value=0):
		self.r = value
	def __call__(self):
		return self.r
	def __int__(self): # __int__ and subsequent __iter__s were from cgpt (specifically, how i would implement this form of class output where the object can be used as an iterator/integer in a smooth manner)
		return self.r

class Neuron(Returner):
	def __init__(self, cons=[]):
		super().__init__()
		self.cons = cons  # input
		self.w = [rng.random] * len(cons)
		self.w = list(map((lambda x: x() * 10 - 5), self.w))
		self.b = rng.random() * 10 - 5
		self.w = list(map(snd, self.w))
		self.a = (lambda x: x)
		self.comps = 0 # times comped. may not be used
	def comp(self):
		x = 0
		for i in enumerate(self.cons):
			x += i[1].r * self.w[i[0]]
		x += self.b
		self.comps += 1
		return self.a(self.r)
	def link(self, con):
		self.__init__(self.cons + con)
	def tweak(self):
		self.w += snd(rng.random()*10-5)
		self.b += snd(rng.random()*10-5)
class RLayer:
	def __init__(self, rs):  # rs -> list of Returner
		self.rs = rs
	def __iter__(self):
		return self.rs

class Layer(RLayer): # neurons have to be added in ns to create
	def __init__(self, ns, con):
		super().__init__(ns)
		self.con = con
		for i in self.rs:
			i.link(self.con.rs)
	def link(self):
		for i in self.rs:
			i.link(self.con.rs)
	def comp(self):
		for i in self.rs:
			i.comp()
	def tweak(self):
		for i in self.rs:
			i.tweak()

class PLayer(Layer): # premade
	def __init__(self, len, con):
		i = []
		for _ in range(len):
			i.append(Neuron())
		super().__init__(i, con)

class Thingy: # Neural Network
	def __init__(self, layers):
		self.layers = layers
	#def linkage(self):
		#for i in enumerate(self.layers[1:]): # i often forget about slicing ._. this is from cgpt
			# i[1].link(self.layers[i[0]-1]) replit's ai says this is unnessecary, but i'm having second thoughts...
	def append(self, con):
		self.layers.append(con)
		self.layers[-1].link(self.layers[-2]) # i also forget about reverse indexing ._._. also from
	def comp(self):
		for i in self.layers[1:]:
			i.comp()
	def input(self, inp):
		self.layers[0] = RLayer(inp)
	def tweak(self):
		for i in self.layers[1:]:
			i.tweak()
	def __iter__(self):
		self.comp()
		return self.layers[-1].__iter__()

class PThingy(Thingy):
	def __init__(self, lens): # len is a list of lens for each layer. misnomer!!!11!1
		_in = [RLayer([Returner()] * lens[0])]
		for i in lens[1:]:
			_in += [PLayer(i, _in[-1])]
		super().__init__(_in)
#		super().__init__(\
#			[RLayer([Returner()] * lens[0])] + \
#			[[PLayer(slen, self)] for slen in lens[1:]]) 
		# replit is acting weird. it says super() takes 0 args??? edit: it does if you don't list the parent.
		# self.linkage() see 97
		self.comp()
	def __iter__(self):
		return list(super().__iter__())

#class Community:
#	pass

print('evaluating tests...')

def _test1():
	ai = []
	ai.append([Returner(1), Returner(2), Returner(3)])
	ai.append(Neuron(ai[0]))
	ai[1].w = [1 / 3] * 3 # [], not (). it's not 1
	print('test 1: use pre-made perceptron: expected: 2.0; actual: ' + 			str(ai[1].comp()))
	print("note: added randomization. not 2 anymore...")
#_test1()

def _test2():
	print('test 2: use multiple perceptron layers with input given')
	ai = []
	ai.append(RLayer([Returner(\
		int(input())\
	), Returner(\
		int(input())\
	), Returner(\
		int(input())\
	)])) # i no want () re
	ai.append(PLayer(3, ai[0]))
	ai.append(Neuron(ai[1].rs))
	ai[2].comp()
	print('result: ' + str(ai[2].r)) # replit ai is good; i didn't even see this beforehand yet
# NOTE: a layer returns a LIST of values, all of which have to be factored in for each Neuron of the next layer!
#_test2()

cai = PThingy([3, 3, 3]) # c is for class-defined
print("layers:")
for i in cai.layers:
	print(i)
cai.input([1, 2, 3])
cai.comp()
print("123:", [i.r for i in cai.__iter__()])
cai.tweak()
cai.comp()
print("123 tweaked:", [i.r for i in cai.__iter__()])
cai.input([-8, 2, 4])
print(cai.layers[0].rs)
print("-824 before:", [i.r for i in cai.layers[1].rs])
cai.comp()
print("-824 after:", [i.r for i in cai.layers[1].rs])
print([i.r for i in cai.__iter__()])
# TODO: add dosctrign' and moar comments