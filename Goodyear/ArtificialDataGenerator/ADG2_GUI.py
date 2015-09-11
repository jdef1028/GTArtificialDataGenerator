from __future__ import division
# GUI for Artificial Data Generator v2.0
# by Xiaolin Li
# supervised by Prof. Wei Chen, Prof. Cate Brinson
# Sept 10, 2015

from Tkinter import *
from ADG2 import *
import os
import matplotlib.pyplot as plt

class runADG2:
	def __init__(self, master):
		self.master = master
		self.main_Title = Label(self.master, text='ADG v2.0', justify=CENTER)
		self.main_Title.grid(row = 0, columnspan = 10)
		
		self.Lines()
		self.paraInput()
	
	def Lines(self):
		# gadgets alignment
		lineTag = Label(self.master, text = '')
		lineTag.grid(row = 2, column = 0, sticky = 'W')
		Labelx = Label(self.master, text='x1')
		Labelx.grid(row = 2, column = 1, sticky ='W')
		Labely = Label(self.master, text='y1')
		Labely.grid(row = 2, column = 2, sticky = 'W')
		Labelx2 = Label(self.master, text='x2')
		Labelx2.grid(row = 2, column = 3, sticky ='W')
		Labely2 = Label(self.master, text='y2')
		Labely2.grid(row = 2, column = 4, sticky = 'W')
		Imgsize_label = Label(self.master, text='Image size:')
		Imgsize_label.grid(row = 1, column = 0)
		self.Imgsize = Entry(self.master)
		self.Imgsize.grid(row = 1, column = 1)
		Labelwidth = Label(self.master, text='width')
		Labelwidth.grid(row = 2, column = 5)
		
		Line1_Label = Label(self.master, text = 'Line 1')
		Line1_Label.grid(row = 3, column = 0)
		Line2_Label = Label(self.master, text = 'Line 2')
		Line2_Label.grid(row = 4, column = 0)
		self.x11 = Entry(self.master)
		self.x11.grid(row = 3, column = 1, sticky= 'W')
		self.y11 = Entry(self.master)
		self.y11.grid(row = 3, column = 2, sticky= 'W')
		self.x12 = Entry(self.master)
		self.x12.grid(row = 3, column = 3, sticky = 'W')
		self.y12 = Entry(self.master)
		self.y12.grid(row = 3, column = 4, sticky = 'W')
		self.x21 = Entry(self.master)
		self.x21.grid(row = 4, column = 1, sticky = 'W')
		self.y21 = Entry(self.master)
		self.y21.grid(row = 4, column = 2, sticky = 'W')
		self.x22 = Entry(self.master)
		self.x22.grid(row = 4, column = 3, sticky= 'W')
		self.y22 = Entry(self.master)
		self.y22.grid(row = 4, column = 4, sticky = 'W')	
		self.width1 = Entry(self.master)
		self.width1.grid(row = 3, column = 5, sticky = 'W')
		self.width2 = Entry(self.master)
		self.width2.grid(row = 4, column = 5, sticky = 'W')
		
	def paraInput(self):
		#paramenter fields	
		blank = Label(self.master, text ='')
		blank.grid(row = 5)
		fillerLabel = Label(self.master, text = 'Filler Modulus')
		matrixLabel = Label(self.master, text = 'Matrix Modulus')
		self.fMod = Entry(self.master)
		self.mMod = Entry(self.master)
		fillerLabel.grid(row=6, column =0)
		matrixLabel.grid(row=6, column = 2)
		self.fMod.grid(row = 6, column =1)
		self.mMod.grid(row = 6, column =3)
		
		IntphLabel = Label(self.master, text = 'Interphase Thickness for isolated filler')
		self.IntphT = Entry(self.master)
		IntphLabel.grid(row = 6, column =4)
		self.IntphT.grid(row = 6, column =5)
	
		nextButton = Button(self.master, text= 'Next', command = lambda: self.readnum())
		nextButton.grid(row = 7, column =2)
		clearButton = Button(self.master, text= 'Clear', command = lambda: self.startover(1))
		clearButton.grid(row = 7, column = 4)
	def readnum(self):
		# read the numbers from master window
		execfile('ADG.py')
		self.Imgsize_num = int(self.Imgsize.get())
		self.x11_num = int(self.x11.get())
		self.y11_num = int(self.y11.get())
		self.x12_num = int(self.x12.get())
		self.y12_num = int(self.y12.get())
		self.x21_num = int(self.x21.get())
		self.y21_num = int(self.y21.get())
		self.x22_num = int(self.x22.get())
		self.y22_num = int(self.y22.get())
		self.width1_num = int(self.width1.get())
		self.width2_num = int(self.width2.get())
		a = ADG2(self.Imgsize_num)
		a.addLine(self.x11_num,self.y11_num,self.x12_num,self.y12_num,self.width1_num)
		a.addLine(self.x21_num,self.y21_num,self.x22_num,self.y22_num,self.width2_num)
		a.visualize(0)
		# so far, the binary image has been plotted
		
		self.QAwin1 = Tk()
		self.QAwin1.title('NU-GT ADG v2.0')
		text1 = Label(self.QAwin1, text = "Satisfied with the binary image?")
		text1.grid(row = 0, column = 1)
		yesbutton = Button(self.QAwin1, text = "Yes", command = lambda: self.step1(a))
		yesbutton.grid(row = 1, column = 0)
		nobutton = Button(self.QAwin1, text = "No", command = lambda: self.startover())
		nobutton.grid(row = 1, column = 2)
		
	def startover(self, option=0):
		# if the user selects "No" in the former step, this function will be executed
		self.master.destroy()
		if option==0:
			self.QAwin1.destroy()
		root = Tk()
		root.title('NU-GT ADG v1.0')
		myADG = runADG2(root)
		mainloop()
	
	def step1(self, a, option=0):
		# if the user selects "Yes", this function will be executed
		if option==0:
			self.fMod_num = float(self.fMod.get())
			self.mMod_num = float(self.mMod.get())
			self.IntphT_num = int(self.IntphT.get())
			self.master.destroy()
			self.QAwin1.destroy()
			a.matProp(self.fMod_num, self.mMod_num)
			a.intphThickness(self.IntphT_num)
		self.master2 = Tk()
		self.master2.title('NU-GT ADG v2.0')
		decayTitle = Label(self.master2, text="What's your decay function? ")
		decayTitle2 = Label(self.master2, text="Current available descriptor: nbd")
		decayTitle.grid(row = 0)
		decayTitle2.grid(row = 1)
		self.decayEntry = Entry(self.master2)
		self.decayEntry.grid(row = 2)
		submitButton = Button(self.master2, text='Submit', command = lambda: self.step2(a))
		submitButton.grid(row = 3, column = 0)
		plotButton = Button(self.master2, text = 'Plot', command = lambda: self.step2_plot(a))
		plotButton.grid(row = 3, column = 1)
		if option !=0:
			warning = Label(self.master2, text = "The decay function entered is invalid!")
			warning.grid(row=4)
			
	def step2_plot(self,a):
		temp_decay = self.decayEntry.get()
		x = [i*0.01 for i in range(int(a.intphThickness/0.01) + 1)]
		y = []
		for nbd in x: 
			y.append(eval(temp_decay))
		plt.plot(x,y,'-')
		plt.show()
		
	def step2(self, a):
		#read the entered decay function
		tempFun = self.decayEntry.get()
		flag = a.checkDecayFun(tempFun)
		if flag == False:
			self.master2.destroy()
			self.step1(a,1)
		else:
			a.calDisMat()
			self.master2.destroy()
			self.step3(a)
	
	def step3(self, a):
		self.master3 = Tk()
		self.master3.title('NU-GT ADG v2.0')
		broadeningTitle = Label(self.master3, text='Please type in your broadening function')
		broadeningTitle.grid(row = 1)
		broadeningexample = Label(self.master3, text='Example: (x[0]+x[1]-2*T)/2/T')
		broadeningexample.grid(row = 2)
		self.broadeningentry = Entry(self.master3)
		self.broadeningentry.grid(row = 3)
		bsubmit = Button(self.master3, text ='Submit',command = lambda: self.step4(a))
		bsubmit.grid(row = 4)
	
	def step4(self, a):
		self.broadening = self.broadeningentry.get()
		a.defBroadening(self.broadening)
		a.calTimg()
		a.addIntph()
		max_num = a.maxIntph() # max overlapping
		self.master3.destroy()
		if a.needCompEff():
			#overlapping exists
			self.master4 = Tk()
			self.master4.title('NU-GT ADG v2.0')
			compefftitle = Label(self.master4, text = 'Please enter your compound effect')
			compefftitle.grid(row = 1)
			compeffexmp = Label(self.master4, text = 'Example: x[0] + x[1]')
			compeffexmp.grid(row = 2)
			self.compEffs = [Entry(self.master4) for i in range(2, max_num+1)]
			labels = [Label(self.master4, text=str(i)+ ' overlapped:') for i in range(2, max_num+1)]
			for i in range(max_num-1):
				print labels[i]
				labels[i].grid(row = 3+i, column = 0)
				self.compEffs[i].grid(row = 3+i, column = 1)
			submitbutton = Button(self.master4, text = 'Submit', command = lambda: self.step5(a))
			submitbutton.grid(row = 4+i)
		else:
			# no overlapping
			print "Not implemented yet!"
	
	def step5(self,a):
		for i in range(2, len(self.compEffs)+2):
			ss = self.compEffs[i-2].get()
			a.defCompEff(i, ss)
			flags = a.checkCompEq()
			flags.pop(0)
			flags.pop(0)
			sym =[]
			for i in range(len(flags)):
				if flags[i]:
					sym.append('Symmetric')
				else:
					sym.append('Nonsymmetric')
			eq = copy.copy(a.CompEff)
			print eq	
			self.master4.destroy()
			self.master5 = Tk()
			checktitle = Label(self.master5, text = 'Symmetry of the compounf effect equations')
			checktitle.grid(row = 1)
			eqlabel = [Label(self.master5, text = eq[i]) for i in range(2,len(eq))]
			symlabel = [Label(self.master5, text = sym[i]) for i in range(len(eq)-2)]
			for i in range(len(eq)-2):
				eqlabel[i].grid(row = i+2, column = 0)
				symlabel[i].grid(row = i+2, column = 1)
			nextbutton = Button(self.master5, text='Next', command=lambda: self.step6(a))
			nextbutton.grid(row = i+3, column = 1)
		
	def step6(self,a):
		self.master5.destroy()
		a.applyCompEff()
		a.visualize(1)
		self.master6 = Tk()
		self.master6.title('NU-GT ADG v2.0')
		instruction_text = Label(self.master6, text='Please specify two diagonal corners of the select region:')
		instruction_text.grid(row = 0, column = 0)
		xlabel = Label(self.master6, text='x')
		xlabel.grid(row = 1, column = 1)
		ylabel = Label(self.master6, text='y')
		ylabel.grid(row = 1, column = 2)
		point1_text = Label(self.master6, text='Corner Point 1:')
		point1_text.grid(row = 2, column = 0)
		self.point1_x = Entry(self.master6)
		self.point1_x.grid(row = 2, column = 1)
		self.point1_y = Entry(self.master6)
		self.point1_y.grid(row = 2, column = 2)
		point2_text = Label(self.master6, text='Corner Point 2:')
		point2_text.grid(row = 3, column = 0)
		self.point2_x = Entry(self.master6)
		self.point2_x.grid(row = 3, column = 1)
		self.point2_y = Entry(self.master6)
		self.point2_y.grid(row = 3, column = 2)
		interval_text = Label(self.master6, text = 'Number of points on each dimension:')
		interval_text.grid(row = 4, column = 0)
		self.interval_entry = Entry(self.master6)
		self.interval_entry.grid(row = 4, column = 1)
		file_text = Label(self.master6, text = 'File name')
		file_text.grid(row = 4, column = 2)
		self.file = Entry(self.master6)
		self.file.grid(row = 4, column = 3)
		submitbutton = Button(self.master6, text='Submit', command = lambda: self.step7(a))
		submitbutton.grid(row = 5, column = 0)
		
	
	def step7(self, a):
		point1x = int(self.point1_x.get())
		point2x = int(self.point2_x.get())
		point1y = int(self.point1_y.get())
		point2y = int(self.point2_y.get())
		segs = int(self.interval_entry.get())
		filename = self.file.get() + '.csv'
		a.extractData(point1x,point1y,point2x,point2y,segs,filename)
		self.master6.destroy()
			

			
		
			
		
		
	
if __name__ == '__main__':
	root = Tk()
	root.title('NU-GT ADG v2.0')
	myADG = runADG2(root)
	mainloop()
	
# ADG2_GUI is finished at 11:06am 9/11/2015 by Xiaolin Li