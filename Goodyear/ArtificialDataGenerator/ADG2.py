from __future__ import division
__author__ = 'Xiaolin Li'
__date__ = 'Sept 7, 2015'
__credits__ = ['Xiaolin Li', 'Pavan Kolluru', 'Karl Putz'];
__copyright__ = ['Advanced Materials Lab', 'Integrate Design and Automation Lab']
__version__ = 'v2.0'

import csv
import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sympy import symbol
import copy
from math import sin, cos, sqrt, tan, exp, trunc, log 

class ADG2():
	""" ADG2 is a class that could read decay function, broadening function and
	 the compound effect function to generate a set of artificial data.
	 ===================================================================
	 ADG2() is an updated version of ADG(). It is more compatible with the GUI"""
	 
	size = -1 # initialize the size
	
	def __init__(self, size):
		""" Initialize the object with a given integer. The size of the matrix will be set as this integer
		@para: size --> integer, the size of the field matrix"""
		
		self.Bimg = np.zeros((size, size)) # Init the binary matrix
		self.Iimg = np.zeros((size, size)) # Init the filler/matrix/intph label matrix
		self.Timg = np.zeros((size, size)) # Init the interphase thickness matrix
		self.size = size # assign the matrix size as an attribute of the object
		
		# Coefficients of the line function
		self.AList = []
		self.BList = []
		self.CList = []
		
		#half of the line width
		self.spanList = []
		
		# initialize the gradient field matrix
		temp_array = []
		for i in range(size):
			temp_array.append([])
		self.Cimg = []
		for i in range(size):
			self.Cimg.append(copy.deepcopy(temp_array))
			
		temp_array = []
		for i in range(size):
			temp_array.append([-1])
		self.DisMat = []
		for i in range(size):
			self.DisMat.append(copy.deepcopy(temp_array))
		
		self.negDisMat = copy.deepcopy(self.DisMat)
		
			
	def getSize(self):
		""" query the size of the image from the object """
		if self.size != -1:
			# the size has been updated when creating the object
			return self.size
		else:
			print "No size info assigned!"
	
	def __str__(self):
		return self.Bimg
	
	def addLine(self, X1, Y1, X2, Y2, width):
		""" generate a line of filler through two points (X1, Y1) and (X2, Y2) with the given width
		@para: X1: x coordinate of the first point
			   Y1: y coordinate of the first point 
			   X2: x coordinate of the second point
			   Y2: y coordinate of the second point
		@return: 1--> success 0--> fail"""
		
		span = trunc(float(width-1)/2)
		if (X1 == X2) and (Y1 == Y2):
			# the inputs are two identical points
			return 0
		else:
			# starts to calculate the coefficients
			A = Y2 - Y1
			B = X1 - X2
			C = - X1 * (Y2 - Y1) + Y1 * (X2 - X1)
			self.AList.append(A)
			self.BList.append(B)
			self.CList.append(C)
			self.spanList.append(span)
			for i in range(self.size):
				for j in range(self.size):
					# calculate the distances to the line
					d = abs(A*i + B*j + C) / sqrt(A**2 + B**2)
					if d <= span:
						self.Bimg[i][j] = 1 #update the binary matrix
	
	def visualize(self, type = 0):
		""" visualize the current field
		@para: type --> 0/1 integer, 0 indicates binary and 1 indicates gradient
		@return: 1 --> success, 0 --> fail
		"""
		
		if type == 0:
			# plot the binary image
			mark1 = plt.imshow(self.Bimg, cmap = 'Greys', interpolation = 'nearest')
			plt.show()
			return 1
		elif type == 1:
			# before plotting the colorful image, we should firstly check if self.Cimg exist
			try:
				self.Cimg
			except AttributeError:
				print "Field has not been created yet!"
				return 0
			
			#plot the colorful gradient image
			imgplot = plt.imshow(self.Cimg)
			imgplot.set_cmap('hot')
			plt.colorbar()
			plt.show()
			
	def intphThickness(self, thickness):
		""" define the interphase thickness for the isolated filler
		@para" thickness --> the given interphase thickness
		"""
		self.intphThickness = thickness
		
	def matProp(self, fMod, mMod):
		""" define the filler/matrix properties
		@para: fMod --> the filler property
			   mMod --> the matrix property
		"""
		self.fMod = fMod
		self.mMod = mMod
	
	def calDisMat(self):
		""" calculate the distances to the lines for each point
		@return: 0 --> fail, 1 --> success"""
		num = len(self.AList) # compute the number of the lines
		for acc in range(num):
			for i in range(self.size):
				for j in range(self.size):
					d = abs(self.AList[acc] * i + self.BList[acc] * j + self.CList[acc]) \
					/ sqrt(self.AList[acc]**2 + self.BList[acc]**2) # calculate distance
					if self.DisMat[i][j][0] == -1:
						self.DisMat[i][j].pop(0)
					self.DisMat[i][j].append(d) # save this distance to list
					d = (self.AList[acc] * i + self.BList[acc] * j + self.CList[acc]) \
					/ sqrt(self.AList[acc]**2 + self.BList[acc]**2) # calculate distance
					if self.negDisMat[i][j][0] == -1:
						self.negDisMat[i][j].pop(0)
					self.negDisMat[i][j].append(d) # save this distance to list
					
	
	def defBroadening(self, eq):
		""" define the interphase thickness broadening function 
		@para: eq --> broadening function"""
		self.BroadenEq = eq
		
		  
	def calBroadening(self, dList, intphT):
		""" calculate the interphase broadening factor using the distances and the given intph thickness
		@para: dList: the distances to all the lines from the studied point (a vector)
			   intphT: the interphase thickness for the isolated particle/filler
		@return: broadening factor value for this point
		"""
		x = copy.copy(dList)
		T = intphT
		bf = eval(self.BroadenEq)
		return bf
	
	def calTimg(self):
		""" calculate the effective interphase thickness for each points"""
		for i in range(self.size):
			for j in range(self.size):
				# this line needs to be changed/redefined in the future, marked by Xiaolin
				d1 = self.negDisMat[i][j]
				d2 = copy.copy(d1)
				for k in range(len(d2)):
					d2[k] = abs(d2[k])
				if (sum(d1) != sum(d2)) and (sum(d1) != -sum(d2)):
					self.Timg[i][j] = self.intphThickness * self.calBroadening(self.DisMat[i][j], self.intphThickness)
				else:
					self.Timg[i][j] = self.intphThickness
	
	def addIntph(self):
		""" assign interphase to the filler/matrix/interphase label matrix """
		try:
			self.fMod
			self.mMod
			self.intphThickness
		except AttributeError:
			print "At least one key parameter is missing!"
		
		num = len(self.AList)
		for acc in range(num):
			for i in range(self.size):
				for j in range(self.size):
					
					d = self.DisMat[i][j][acc]
					
					if d<= self.spanList[acc]:
						self.Cimg[i][j] = [self.fMod]
						self.Iimg[i][j] = 1
	
					elif (d <= (self.spanList[acc] + self.Timg[i][j])) and (self.Bimg[i][j] == 0):
						self.Iimg[i][j] = 0.5
						nbd = float(d) - float(self.spanList[acc])
						prop = self.evalDecayFun(nbd/self.Timg[i][j]*self.intphThickness)
						if self.Cimg[i][j] == [self.mMod]:
							self.Cimg[i][j].pop()
						self.Cimg[i][j].append(prop)
					else:
						if self.Cimg[i][j] == []:
							self.Cimg[i][j].append(self.mMod)
		plt.imshow(self.Iimg)
		plt.show()
		print self.Cimg[:][485]
		
	def checkDecayFun(self,s):
		""" Verify the given decay function 
		@para: s --> string, the decay function string
		@return: True --> valid, False -->invalid"""
		self.eq = s
		if (self.evalDecayFun() >= self.mMod) and (self.evalDecayFun()<=self.fMod) and \
		(self.evalDecayFun(self.intphThickness) >= self.mMod) and (self.evalDecayFun(self.intphThickness)<= self.fMod):
			return True
			# the filler-end point could not exceed filler property / the matrix-end point could not be lower than the mMod
		else:
			return False
	
	def evalDecayFun(self, nbd =0, option =0):
		""" this function returns the material property based on the decay function
		@para: nbd --> float, nearest boundary distance
		"""
		try:
			self.eq
		except AttributeError:
			print "The decay function has not been defined yet!"
		#print eval(self.eq)
		return eval(self.eq)
			
	
	def maxIntph(self):
		""" calculate the maximum number of overlapping interphase layers
		@return: max_ele -->integer. Maximum overlapping interphase layer number
		"""
		max_ele = 0 #reset the counter
		for i in range(self.size):
			for j in range(self.size):
				if len(self.Cimg[i][j]) > max_ele:
					max_ele = len(self.Cimg[i][j])
		return max_ele
	
	def defCompEff(self, layer_num, s):
		""" define the compound effect for each number of overlapping interphase layer
		@para: layer_num --> interger. The number of overlapping interphases
			   s --> string. Compound effect for this case
		"""
		if not hasattr(self, 'CompEff'):
			self.CompEff = ['x[0]'] * (self.maxIntph()+1) # for each element, the default is always itself
		
		x = [0] * layer_num
		try:
			eval(s)
		except IndexError:
			print "Number of interphases mismatch!"
				
		self.CompEff[layer_num] = s # assign new Compound Effect from s
			
		
	def needCompEff(self):
		""" Examine if the functions of compound effects are needed
		@return: True --> Yes, False --> No
		"""
		ele_num = self.maxIntph()
		if ele_num <= 1:
			# there is no overlapping interphase region
			return False
		else: 
			return True	
	
	def checkCompEq(self):
		""" Examine the symmetry of the compound effect equations
		@return: flags --> a list of boolean value. Corresponds to the overlapped interphase layers' comp eff equations"""
		num = self.maxIntph()
		if num > 1:
			flags = [True] * (num+1)
			for i in range(2,num+1):
				eq = self.CompEff[i] # eq is the currently studied equation
				x = [0] * i # initialize the vector before examining the symmetry
				counter = 0 # reset counter
				for trial in range(3): # starts 3 trials
					for j in range(i):
						x[j] = random.uniform(self.mMod, self.fMod) # randomly assigned value
					y1 = eval(eq)
					xx = copy.copy(x)
					#print x,y1
					while True:
						random.shuffle(x)
						if x!= xx:
							break
					y2 = eval(eq)
					#print x,y2
					if y1 == y2:
						counter += 1
				if counter == 3: # all trials succeed
					flags[i] = True
				else:
					flags[i] = False
			return flags
		else:
			return [True, True]
	
	def applyCompEff(self):
		""" After verifying the compound effect function, this function could be applied to apply
		the CompEff to combine the objects
		"""
		for i in range(self.size):
			for j in range(self.size):
				self.Cimg[i][j].sort(reverse = True)
				ele_num = len(self.Cimg[i][j])
				x = copy.copy(self.Cimg[i][j])
				prop = eval(self.CompEff[ele_num])
				#if prop<0:
					#print i,j,self.Cimg[i][j]
				self.Cimg[i][j] = prop
				
				
		
	def extractData(self, X1, Y1, X2, Y2, segs, filename='data.csv'):
		""" Extract Data to generate a data sheet for data mining.
		@para: X1, Y1 --> coordinates of the first point
			   X2, Y2 --> coordinates of the second point (for selected box)
			   segs --> integer. Number of intervals on each dimension
			   filename --> name of the data sheet
			   """
		# consider the special cases first	   
		if (X1<0) or (X1>self.size-1) or (X2<0) or (X2>self.size-1) or (Y1<0) or (Y1>self.size-1) or (Y2<0) or (Y2>self.size-1):
			print "The given coordinates are out of bound"
			sys.exit(0)
		elif (X1==X2) or (Y1==Y2):
			print "The given two points cannot form an rectangle"
			sys.exit(0)
			
		# if the coordinates are valid
		else:
			xmin = min(X1, X2)
			xmax = max(X1, X2)
			ymin = min(Y1, Y2)
			ymax = max(Y1, Y2)
			xIncrement = float(xmax - xmin)/segs
			yIncrement = float(ymax - ymin)/segs
			xSeeds = [xmin + i*xIncrement for i in range(segs+1)]
			ySeeds = [ymin + j*yIncrement for j in range(segs+1)]
			
			temp_array = []
			for i in range(segs+1):
				temp_array.append([])
			self.dataDMat = []
			for i in range(segs+1):
				self.dataDMat.append(copy.deepcopy(temp_array))
			# create the data distances matrix
			for i in range(segs+1):
				for j in range(segs+1):
					# For simplicity, x,y is taken to record the coordinates of the studied point
					x = xSeeds[i]
					y = ySeeds[j]
					for acc in range(len(self.AList)):
						d = abs(self.AList[acc] * x + self.BList[acc] * y + self.CList[acc]) \
						/ sqrt(self.AList[acc] ** 2 + self.BList[acc] ** 2)
						self.dataDMat[i][j].append(d)
			#print self.dataDMat
			# using the coordinates/decay/broadening function, calculate the property
			
			# init the variables
			self.dataBimg = np.zeros((segs+1, segs+1)) #binary
			self.dataCimg = [] #field
			self.dataTimg = [] #broadening thickness
			self.dataIimg = np.zeros((segs+1, segs+1)) #phase label
			for i in range(segs + 1):
				self.dataCimg.append(copy.deepcopy(temp_array))
				self.dataTimg.append(copy.deepcopy(temp_array))
			# update Timg
			for i in range(segs + 1):
				for j in range(segs + 1):
					self.dataTimg[i][j] = self.intphThickness * self.calBroadening(self.dataDMat[i][j], self.intphThickness)
			#print self.dataTimg
			# label the points
			for acc in range(len(self.AList)):
				# iterate over the different lines
				for i in range(segs + 1):
					for j in range(segs + 1):
						d = self.dataDMat[i][j][acc]
						T = self.dataTimg[i][j]
						if d <= self.spanList[acc]:
							#filler
							self.dataBimg[i][j] = 1
							self.dataIimg[i][j] = 1
							if self.dataCimg[i][j] == [self.mMod]:
								self.dataCimg[i][j].pop()
							self.dataCimg[i][j].append(self.fMod)
						elif (d<self.spanList[acc]+T) and (self.Bimg[i][j]==0):
							#interphase
							if self.dataCimg[i][j] == [self.mMod]:
								self.dataCimg[i][j].pop()
							self.dataCimg[i][j].append(self.evalDecayFun(d/T*self.intphThickness))
							self.dataIimg[i][j] = 0.5
						else:
							#matrix
							if self.dataCimg[i][j] == []:
								self.dataCimg[i][j].append(self.mMod)
								
			
			#apply the provided compound effect equation
			for i in range(segs+1):
				for j in range(segs+1):
					#iterate over each data point
					if len(self.dataCimg[i][j]) <= 1:
						#only one component, no overlapping
						self.dataCimg[i][j] = self.dataCimg[i][j][0]
					else:
						self.dataCimg[i][j].sort(reverse = True)
						ele_num = len(self.dataCimg[i][j])
						x = copy.copy(self.dataCimg[i][j])
						prop = eval(self.CompEff[ele_num])
						self.dataCimg[i][j] = prop
			img=plt.imshow(self.dataCimg)
			img.set_cmap('hot')
			plt.show()
			
			data = []
			for i in range(segs+1):
				for j in range(segs+1):
					data.append([xSeeds[i], ySeeds[j], self.dataCimg[i][j]])
			with open(filename, 'wb') as fp:
				a = csv.writer(fp, delimiter=',')
				a.writerows(data)
			fp.close()
	def checkSym(self, eq, num):
		flag = -2
		x = [0]*num
		try:
			eval(eq)
		except IndexError:
			flag = -1
		
		if flag != -1:
			counter = 0
			for trials in range(3):
				for i in range(len(x)):
					x[i] = random.uniform(self.mMod, self.fMod)
				y1 = eval(eq)
				xx = copy.copy(x)
				while True:
					random.shuffle(x)
					if x != xx:
						break
				y2 = eval(eq)
				if y1 == y2:
					counter += 1
			if counter == 3:
				flag = 1
			else:
				flag = 0
		return flag
		
	def appCompEffGUI(self, compEq):
		for i in range(self.size):
			for j in range(self.size):
				x = [0] * len(self.Cimg[i][j])
				for k in range(len(self.Cimg[i][j])):
					x[k] = self.Cimg[i][j][k]
				x.sort()
				using_eq = compEq[len(self.Cimg[i][j])]
				comb_prop = eval(using_eq)
				#if len(self.Cimg[i][j]) >= 2:
					#print self.Cimg[i][j]
					#print comb_prop
				self.Cimg[i][j] = comb_prop
						

# ADG2 completed at 21:38 CST 9/9/15 by Xiaolin Li
						
			
			
		
	
	
		
		
		
			
		
		
		
					
		
	