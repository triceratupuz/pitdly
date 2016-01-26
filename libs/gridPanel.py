import wx
from math import modf
import floatops
#import delayGUI

class GridPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.dcw =  k.pop('dcw', None)
		self.dch = k.pop('dch', None)
		self.stepsDict = k.pop('stepsDict', None)
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(GridPanel, self).__init__(*a, **k)#super the subclass
		
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		stepsIndex = "1/8"
		self.stepsMultiplier = self.stepsDict[stepsIndex]
		self.steps = 8.0#needs to be float for zoom
		self.startOnDc = 0
		self.SetBackgroundColour((0, 100, 250))
		#
		self.timeQt = 1
		#Coordinates
		self.plength = 10
		self.pradius = 5
		#points storage
		self.points = []
		#recycle storage
		#self.recycle = [0, 0]
		self.recycle = 0
		
		#points verbose, displays no screen
		self.pointsVerbose = 0
		
		self.semitones = []
		self.pirange = 25
		for i in range(-1 * self.pirange, self.pirange + 1):
			self.semitones.append(i)
		
		#self.Bind(wx.EVT_LEFT_DOWN, self.movePoint)	
		self.Bind(wx.EVT_RIGHT_DOWN, self.openDelay)	
		self.Bind(wx.EVT_RIGHT_DCLICK, self.deletePoint)	
		self.Bind(wx.EVT_LEFT_DCLICK, self.recordPoint)	
		#Grid
		self.dcx, self.dcy = 0, 0
		self.bordx, self.bordy = 60, 60
		self.InitBuffer()
		#????????????????
		self.Bind(wx.EVT_PAINT, self.OnPaint)#paint event
		
		
		#quantiz
		self.timeQuantize = 0
		self.pitcQuantize = 0
		
		#????????????????
		self.Bind(wx.EVT_CHAR, self.onCharEvent)
		
		
		self.openDelayFrames = []
		#Display
		#mainSizer.AddSpacer(self.dcw)
		#mainSizer.Add(controlSizer, 1, wx.ALL)
		#self.SetSizer(mainSizer)
		#mainSizer.Fit(self)
		

	def onCharEvent(self, evt):
		"""do stuff when a key is pressed"""
		keycode = evt.GetKeyCode()
		if keycode == 118:
			self.pointsVerbose = (self.pointsVerbose + 1) % 2
			dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
			self.DrawIt(dc)		

	
		
	def recordPoint(self, evt):
		"""record position on left down"""
		position= evt.GetPositionTuple()
		toappend = 1
		ktime = 0
		kpitch = 0
		kquality = .1
		kfeed = 0
		klf = 20
		khf = 15000
		kpan = 0.5
		kreso = 0.0
		kdist = 0.0
		kinvol = 1.0
		kinvolr = 0.0
		koutvol = 1.0
		koutvolr = 0.0
		kmode = 0
		#add condition to chech if on the grid
		if ((self.bordx/2) <= position[0] <= (self.dcw - self.bordx/2)) and ((self.bordy/2) <= position[1] <= (self.dch - self.bordy/2)):
			#if point is on the grid - create a delay
			musicalV = self.screenToValues(position)
			ktime = musicalV[0]
			if self.timeQuantize:#se tempo quantizzato
				ktime = floatops.floatMultRound(ktime, self.stepsMultiplier)
			kpitch = musicalV[1]
			if self.pitcQuantize:#se pitch quantizzato
				kpitch = floatops.floatMultRound(kpitch, 1.0)
			ind = 1
			if len(self.points) == 0:
				evento = [ind, ktime, kpitch, kquality, kfeed, klf, khf, kpan, kreso, kdist, kinvol, kinvolr, koutvol, koutvolr, kmode]
				self.points.append(evento)
			else:
				toappend = 1
				count = 0
				while count < len(self.points):
					tocheck = self.points[count]
					if tocheck[0] <= 0:
						ind = count + 1
						evento = [ind, ktime, kpitch, kquality, kfeed, klf, khf, kpan, kreso, kdist, kinvol, kinvolr, koutvol, koutvolr, kmode]
						self.points[count] = evento
						toappend = 0
						break
					count += 1
				if toappend == 1:
					ind = len(self.points) + 1
					evento = [ind, ktime, kpitch, kquality, kfeed, klf, khf, kpan, kreso, kdist, kinvol, kinvolr, koutvol, koutvolr, kmode]
					self.points.append(evento)
			#to csound
			ftable = 'f %i 0 16 -2 %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f' % (evento[0] + 100, evento[0], evento[1], evento[2], evento[3], 
																													evento[4], evento[5], evento[6], evento[7], evento[8], evento[9], 
																													evento[10], evento[11], evento[12], evento[13], evento[14])
			instr = 'i %f 0.02 -1' % (30.0 + evento[0] * 0.001)
			#print self.points
			self.cSound.InputMessage(ftable + '\n' + instr)
			#update interface
		elif ((self.bordx/2) <= position[0] <= (self.dcw - self.bordx/2)) and (((self.bordy/2) > position[1]) or ((self.dch - self.bordy/2) < position[1])):
			#if point is above or below the grid - recycle
			musicalV = self.screenToValues(position)
			ktime = musicalV[0]
			if self.timeQuantize:#se tempo quantizzato
				ktime = floatops.floatMultRound(ktime, self.stepsMultiplier)
			#self.recycle[0] = ktime
			self.recycle = ktime
			#ToCsound
			self.cSound.TableSet(99, 1, ktime)
			instr = 'i 40 0.02 -1'
			self.cSound.InputMessage(instr)
			#Update inputPanel
			self.GetParent().inPanel.updateGraphics("ON", ktime)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)


	def screenToValues(self, position):
		"""calculate musical values based on coords"""
		time = self.startOnDc + (self.steps - 1) * ((1.0 * position[0] - (self.bordx / 2.0)) / (1.0 * (self.dcw- (self.bordx))))
		pitch = self.pirange - 2 * self.pirange * (position[1] - (self.bordy / 2.0)) / (1.0 * self.dch- (self.bordy))
		return (time, pitch)
		

	def valuesToScreen(self, values):
		"""calculate coords from musical values"""
		onestepvalueX = 1.0 * (self.dcw - self.bordx) / (self.steps - 1) 
		onestepvalueY = 1.0 * (self.dch - self.bordy) / (2 * self.pirange) 
		px = self.bordx/2 + (values[0] - self.startOnDc) * onestepvalueX#x coord on the grid
		py = self.bordy/2 + ((2 * self.pirange) - (values[1] + self.pirange)) * onestepvalueY#x coord on the grid
		return (px, py)


	def deletePoint(self, evt):
		"""to delete points"""
		pos= evt.GetPositionTuple()
		for point in self.points:
			px, py = self.valuesToScreen((point[1], point[2]))
			if (((px - self.pradius) < pos[0] < (px + self.pradius)) and ((py - self.pradius) < pos[1] < (py + self.pradius))):
				index = self.points.index(point)
				self.points[index][0] = -1 * self.points[index][0]#negative index is no more valid istance
				#Csound turnoff instrument code here
				self.cSound.InputMessage('i %f 0 -1' %(-30 + self.points[index][0] * 0.001))
				#Csound turnoff instrument code here
		#if (self.valuesToScreen((self.recycle[0], -1))[0] - 5) < pos[0] < (self.valuesToScreen((self.recycle[0], -1))[0] + 5):
		if (self.valuesToScreen((self.recycle, -1))[0] - 5) < pos[0] < (self.valuesToScreen((self.recycle, -1))[0] + 5):
			#self.recycle[0] = self.recycle[0] * -1.0
			self.recycle = self.recycle * -1.0
			#to Csound
			instr = 'i -40 0.02 -1'
			self.cSound.InputMessage(instr)
			#Update inputPanel
			self.GetParent().inPanel.updateGraphics("OFF", 0.0)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)
		print self.points
			
		
	def setStartOnDc_m(self, evt):
		"""set the first duration point in grid"""
		if self.startOnDc > 0:
			self.startOnDc -= 1
		#print self.startOnDc 
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)		


	def setStartOnDc_p(self, evt):
		"""set the first duration point in grid"""
		self.startOnDc += 1
		#print self.startOnDc 
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)		

	def setZoom_in(self, evt):
		"""zoom in the grid"""
		if self.steps >= 4.0:
			self.steps = self.steps * 0.5
			#print self.steps 
		else:
			#print "NO MORE ZOOM"
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)		


	def setZoom_out(self, evt):
		"""zoom in the grid"""
		self.steps = self.steps * 2
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)		


		
	def timeGridSetting(self, evt):
		"""time grid variable"""
		self.stepsMultiplier = self.stepsDict[self.stepsIndex]
		#print self.stepsMultiplier
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)		
		

	def OnPaint(self, evt):
		#dc = wx.BufferedPaintDC(self, self.buffer)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawIt(dc)

	
	def InitBuffer(self):
		"""initialize drawing buffer"""
		self.buffer = wx.EmptyBitmap(self.dcw, self.dch)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		#print dc.GetSize() 
		dc.SetBackgroundMode(wx.TRANSPARENT)
		self.DrawIt(dc)
		

	def DrawIt(self, dc):
		"""Drawing procedure"""
		dc.SetDeviceOrigin(self.dcx, self.dcy)
		dc.SetBackgroundMode(wx.TRANSPARENT)
		dc.Clear()
		self.DrawAxis(dc)
		self.DrawPoints(dc)
		self.drawRecycle(dc)
		
		
	def DrawAxis(self, dc):
		"""draw axis and indications on screen"""
		dc.SetPen(wx.Pen('DIM GRAY', 1, wx.DOT))
		dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
		#bordx = 60
		#bordy = 60
		#Time Drawing
		dc.SetTextForeground((0,255,0))
		
		i = 0.0
		#for i in range(0, self.steps):#Time text indication
		while i < self.steps:
			sttxt = "%d" % (self.startOnDc + i)
			sttw, stth = dc.GetTextExtent(sttxt)
			if self.steps == 1.0:
				safer = 0
			else:
				safer = int(i * (self.dcw - self.bordx) / (self.steps-1))
			dc.DrawText(sttxt, (self.bordx / 2) - sttw / 2 + safer, self.bordy/2 - stth)
			#dc.DrawText(sttxt, (self.bordx / 2) - sttw / 2+ int(i * (self.dcw - self.bordx) / (self.steps-1)), self.bordy/2 - stth)
			i += 1.0
		i = 0.0
		#for i in range(0, int(self.steps * 1 / self.stepsMultiplier)):#time vertical lines
		while i < (self.steps * 1 / self.stepsMultiplier):
			if self.steps == 1.0:
				safer = 0
			else:
				safer = int(i * self.stepsMultiplier * (self.dcw - self.bordx) / (self.steps-1))
			opos = (self.bordx / 2) + safer
			if opos <= (self.dcw - self.bordx / 2):
				dc.DrawLine(opos, self.bordy/2 , opos, self.dch - (self.bordy/2))
			i += 1.0
		
		#Pitch drawing
		for i in self.semitones:
			if (i == 0) or abs(i) == 12 or abs(i) == 24:
				dc.SetPen(wx.Pen('RED', 1, wx.SOLID))
				dc.SetTextForeground((255,0,0))
			else:
				dc.SetPen(wx.Pen('DIM GRAY', 1, wx.DOT))
				dc.SetTextForeground((0,0,0))
			vpos = self.dch - (self.bordy / 2) - int((i+self.pirange) * (self.dch - self.bordy) / (self.pirange * 2))
			dc.DrawLine(self.bordx/2 , vpos, self.dcw - (self.bordx/2), vpos)
			txt = str(i)
			tw, th = dc.GetTextExtent(txt)
			dc.DrawText(txt, self.bordx/2 - tw, vpos - th/2)
		
		
	def DrawPoints(self, dc):
		"""draw the points on the screen"""
		txtH = 9
		dc.SetFont(wx.Font(txtH - 1, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
		dc.SetPen(wx.Pen('BLUE', 1, wx.SOLID))
		for point in self.points:
			if point[0] > 0:#valid id
				if self.startOnDc <= point[1] <= self.startOnDc + self.steps:
					px, py = self.valuesToScreen((point[1], point[2]))
					dc.DrawCircle(px, py, self.pradius)
					dc.DrawLine(px, py, px + self.plength, py)
					dc.DrawLine(px, py, px, py - self.plength)
					dc.DrawText(str(point[0]),  px + self.pradius, py - txtH)
					#verbose
					if self.pointsVerbose == 1:
						strid = "ID "+ str(point[0])
						strqu = "qual "+ str(point[3])
						strfe = "feedback "+ str(point[4])
						strlf = "lowest F "+ str(point[5])
						strhf = "highest F "+ str(point[6])
						strpa = "pan "+ str(point[7])
						strvol = "volume "+ str(point[8])
						dc.DrawText(strid,  px + self.plength, py - 3 *txtH)
						dc.DrawText(strqu,  px + self.plength, py - 2 * txtH)
						dc.DrawText(strfe,  px + self.plength, py - txtH)
						dc.DrawText(strlf + " " + strhf,  px + self.plength, py)
						dc.DrawText(strpa,  px + self.plength, py + txtH)
						dc.DrawText(strvol,  px + self.plength, py + 2 * txtH)


	def drawRecycle(self, dc):
		"""draw the recycle indication and update input panel"""
		#if self.recycle[0] > 0:
		if self.recycle > 0:
			dc.SetPen(wx.Pen('BLUE', 3, wx.SOLID))
			#xpos=self.valuesToScreen((self.recycle[0], 0))[0]
			xpos=self.valuesToScreen((self.recycle, 0))[0]
			dc.DrawLine(xpos, self.bordy/2 , xpos, self.dch - (self.bordy/2))
		
		
	def openDelay(self, evt):
		'''update delay frame'''
		pos= evt.GetPositionTuple()
		for point in self.points:
			px, py = self.valuesToScreen((point[1], point[2]))
			if (((px - self.pradius) < pos[0] < (px + self.pradius)) and ((py - self.pradius) < pos[1] < (py + self.pradius))):
				index = self.points.index(point)
				if self.points[index][0] > 0:#negative index is no more valid istance
					#in csound code each delay store the control parameters
					#in a ftable that is 100 + ID number
					titleID = "Delay ID %i" % self.points[index][0]
					#print self.points[index][0]
					tableN = int(100 + round(self.points[index][0]))
					print tableN
					self.GetParent().GetParent().singledlyP.setTable(tableN)
					"""
					newframe = delayGUI.DelayFrame(self, -1, title=titleID, cSound=self.cSound, table=tableN)
					self.openDelayFrames.append(newframe)
					newframe.Show()
					"""




	def onChange(self, evt):
		'''when changing effect chain (all delays in grid panel) delete all the open effect windows
		not used yet'''
		for effectFrame in self.openEffectFrames:
			effectFrame.Destroy()
			#print "KILL EFFECT"
