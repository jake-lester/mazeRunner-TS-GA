#Jacob Lester -- Class of 2020
#Bard College -- Computer Science Department
#Moderation Paper -- mazeRunner, Genetic Algorithm
#48bit Version 1.0  -- March 18 2018

import sys
import math
import random
from operator import itemgetter


class MazeRunner_Run():
	"""Sets ups maze, runs Genetic algortithm to solve maze
	with purpose of visiting as many nodes as possible for
	lowest cumulative path cost. Does not contain mutation.
	made for organisms of 48 bitstring length"""
	def __init__(self):
		print()
		print("New Run! 48 bit")
		self.costsMultiplier = 10
		self.popSize = 90
		self.epochsRemain = 6
		self.maze = self.makeMaze()
		self.generatePop()
		while self.epochsRemain > 0:
			for organism in range(self.popSize):
				self.fitScore(self.population[organism], organism)
			self.display()
			self.select()
			self.newGeneration()
			print("Epochs Remain: ", self.epochsRemain)

	def makeMaze(self):
		"""create maze using listed tuples nested into dictionary"""
		maze = {}
		maze['a'] = [('d',3),('f',1),('a',2),('e',1)]
		maze['b'] = [('b',2),('c',3),('d',1),('e',5)]
		maze['c'] = [('j',3),('c',2),('j',3),('b',3)]
		maze['d'] = [('b',1),('f',3),('a',1),('d',2)]
		maze['e'] = [('b',5),('a',1),('g',2),('e',2)]
		maze['f'] = [('d',3),('f',2),('h',4),('a',1)]
		maze['g'] = [('e',2),('h',1),('i',2),('g',2)]
		maze['h'] = [('h',1),('f',4),('i',4),('g',1)]
		maze['i'] = [('g',2),('h',4),('k',8),('k',7)]
		maze['j'] = [('c',3),('j',2),('c',3),('j',2)]
		maze['k'] = [('i',7),('i',8),('k',2),('k',2)]
		return maze

	def generatePop(self):
		"""create initial population by randomly generating bitstring sequences.
		Each part of the bitstring corresponds to different behaviours.
		Each organism has a bitstring sequence"""
		self.population = []
		for organism in range(self.popSize):
			seq = ""
			for bit in range(48):
				seq += str(random.randint(0,1))
			self.population.append([seq])
		return

	def fitScore(self, seq, ID):
		"""fittness function, assign score in regards to maze perfomance.
		Assign scores based on cummulitive path cost... top scores for lower costs"""
		self.orgLocation = "a"
		self.visited = ["a"]
		self.costs = 0
		for gene in range(24):
			direction = seq[0][2*(gene):2*(gene+1)]
			direction = int(direction[0])*2 + int(direction[1])
			self.move(self.orgLocation, direction)
			done = self.goalCheck()
			if done:
				break
		score = len(self.visited)*100
		score -= self.costs * self.costsMultiplier
		self.population[ID].append(score)

	def move(self, start, direction):
		self.costs += self.maze[start][direction][1]
		if self.maze[start][direction][0] not in self.visited:
			self.visited += self.maze[start][direction][0]
		self.orgLocation = self.maze[start][direction][0]

	def goalCheck(self):
		if self.visited == 11:
			self.costs -= 500
			return True
		else:
			return False

	def select(self):
		"""keep top 30 organisms from old population and randomly select
		organisms from new population to keep in the new population generation.
		sort population by ascending scores"""
		self.population.sort(key=itemgetter(1)) 
		self.population = self.population[60:90]

	def newGeneration(self):
		"""generate new population"""
		for pair in range(15):
			parent1 = self.population[pair][0]
			del self.population[pair][1]
			parent2 = self.population[29 - pair][0]
			del self.population[29 - pair][1]
			children = self.crossover(parent1, parent2)
			for child in range(2):
				self.population.append([children[child]])

		for pair in range(15):
			parent1 = self.population[2*pair][0]
			parent2 = self.population[(2*pair)+1][0]
			children = self.crossover(parent1, parent2)
			for child in range(2):
				self.population.append([children[child]])
		self.epochsRemain -= 1

	def crossover(self, parent1, parent2):
		"""create pair of children by breeding
		pairs of parent organisms"""
		newOrganism1 = ''
		for gene in range(24):
			newOrganism1 += parent1[gene*2]
			newOrganism1 += parent2[(gene*2)+1]
		newOrganism2 = ''
		for gene in range(24):
			newOrganism2 += parent1[(gene*2)+1]
			newOrganism2 += parent2[gene*2]

		return (newOrganism1, newOrganism2)

	def display(self):
		"""display data recorded in text document onto terminal"""
		self.population.sort(key=itemgetter(1))
		self.orgLocation = "a"
		self.visited = ["a"]
		self.costs = 0
		seq = self.population[89][0]
		for gene in range(24):
			direction = seq[2*(gene):2*(gene+1)]
			direction = int(direction[0])*2 + int(direction[1])
			self.move(self.orgLocation, direction)
			done = self.goalCheck()
			if done:
				break
		score = len(self.visited)*100
		score -= self.costs*self.costsMultiplier

		print(score)
		print("visited: ", len(self.visited))
		print(seq)
		print()
		

start = MazeRunner_Run()