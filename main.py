#!/bin/python3

# from math import *
import random as rng
import math

print('beginning software...')

print('defining global functions...')

def snd(x):
	return (lambda y: -y if x < 0 else y)\
	((math.exp(-(x**2)/2)/math.sqrt(2*math.pi))*20) # standard normal distribution tweaked

def sig(x):
	return 1 / (1 + math.exp(-x))

def to4(x): # x is a string that contains only [a-z] atleast once -> 
	return [\
		x[0],
		(lambda x: x[1] if len(x) > 2 else '')(x),
		(lambda x: x[2] if len(x) > 3 else '')(x),
		(lambda x: x[3] if len(x) > 4 else '')(x),
		(lambda x: x[4] if len(x) > 5 else '')(x)
	]

def consult(x):
	print(x)
	return x

print('extracting data...')

with open('3000.txt') as f: # while i do remember open(), the replit autocomplete showed to use the with clause, which might be favored in this situation? it might make proccessing faster to use open() and close() and read each line seperately...
	data = [to4(i) for i in f.readlines()]
data[-1][-2] = 'e' # don't ask.
# TODO: Turn back to 3000.txt

def gen_x(thing, times): # i typed gen_x(thing, times){ as if i was in c for some reason. lol
	for _ in range(times): # gen_x? get it? generation X?
		yield thing

#

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
		for i in range(len(self.cons)):
			x += self.cons[i].r * self.w[i]
		x += self.b
		self.comps += 1
		self.r = self.a(x)
		return x # finally figured it out!
	def link(self, con):
		self.__init__(self.cons + con)
	def tweak(self):
		for i in self.w:
			i += snd(rng.random()*10-5)
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
		x = self.layers[-1]
		return list(map(lambda x:x.comp(), x.rs))
	def input(self, inp):
		self.layers[0] = RLayer(inp)
	def tweak(self):
		for i in self.layers[1:]:
			i.tweak()
		return self
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

def unlock(letter, outs=[0]*27): # outs is one-hot encoding! get it?
	want = list("abcdefghijklmnopqrstuvwxyz")
	want.append('')
	want2 = [1 if i == letter else 0 for i in want] # well actually, this is.
	want3 = [] # outs is just a (0,1) list.
	for i in range(len(outs)): # nvm, has 5 1s so yeah
		want3.append(abs(outs[i] - want2[i]))
	return want3

def lock(letters, outs):
	# thanks to geeksforgeeks, the exception
	
	l = outs
	n = 27
	print(len(l))
	x = [l[i:i + n] for i in range(0, len(l), n)]

	print()
	x2 = [sum(unlock(letters[i], x[i])) for i in range(5)]
	return x2

def idk(letters):
	
	l = [[0]*27]*5
	j=[]
	for k in range(5):
		j.append([1 if i == letters[i] else 0 for i in l[k]])
	return j

class Community:
	def __init__(self, len):
		self.things = [PThingy([(27*4), 15, 10, 15, 27])] * len
	def update(self, inp):
		for i in self.things:
			i.input([idk(inp)])
		self.things.sort(key=lambda x: -sum(lock(inp, x.comp())))
		self.things[0:5] = self.things[-4:] # four
		self.things = [i.tweak() for i in self.things[0:5]] + self.things[5:]

print('evaluating tests...')

def _test1():
	ai = []
	ai.append([Returner(1), Returner(2), Returner(3)])
	ai.append(Neuron(ai[0]))
	ai[1].w = [1 / 3] * 3 # [], not (). it's not 1
	x = str(ai[1].comp())
	print('test 1: use pre-made perceptron: expected: 2.0; actual: ' + x)
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

def _test3():
	cai = PThingy([3, 3, 3]) # c is for class-defined
	print("layers:")
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
#_test3()

# TODO: add dosctrign' and moar comments
# nano or ed? actually, i'll just use vscode. it has the mighty power of... DEBUGGING!

def _finale():
	x = Community(20)
	x.update('aaaaa')
	print(x[-1].comp())
_finale()