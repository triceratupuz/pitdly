import wx
import csnd6


class TxtCtrlNum(wx.TextCtrl):
	def __init__(self, *a, **k):
		"""
		A subclass of TextCtrl allowing float numbers only control
		
		LAST UPDATE 25/08/2015
		
		Features:
		
		Allows values to be modified by keyboard input number,
		mouse wheel and mouse drag (double-click and hold)
		
		
		Minimum and maximum boudaries values
		(min_val, max_val)
		
		Selectable initial value at __init__
		(init_val)
		
		Selectable number of fractional part digits
		(fractionWidth)
		
		Keyboard input needs return key to confirm the value,
		while the value is not yet confirmed text is in another 
		customizable colour
		(colWaitConf)
		
		Value increment and decrement with mouse wheel with 
		adjustable sensitivity as percentage of the range
		(mwhs)
		
		Mouse movement vertical or horizontal to change
		the value
		(mousev)
		
		Value increment and decrement with mouse movement 
		adjustable sensitivity as percentage of the range
		(mmhs)
		
		
		MUST!!!!!!
		style=wx.TE_PROCESS_ENTER|wx.TE_RICH2
		
		"""
		self.min_val =  k.pop('min_val', None)
		if self.min_val == None:
			self.min_val = 0
		self.max_val =  k.pop('max_val', None)
		if self.max_val == None:
			self.max_val = 1
		self.init_val =  k.pop('init_val', None)
		if self.init_val == None:
			self.init_val = self.min_val
		self.fractionWidth = k.pop('fractionWidth', None)
		if self.fractionWidth == None:
			self.fractionWidth = 3
		self.colWaitConf = k.pop('colWaitConf', None)
		if self.colWaitConf  == None:
			self.colWaitConf = 'red'
		self.mwhs = k.pop('mwhs', None)
		if self.mwhs  == None:
			self.mwhs = 0.001
		self.mousev = k.pop('mousev', None)#default vertical = 1 horixontal =0
		if self.mousev == None:
			self.mousev = 1
		self.mmhs = k.pop('mmhs', None)
		if self.mmhs  == None:
			self.mmhs = 0.01
		super(TxtCtrlNum, self).__init__(*a, **k)#super the subclass
		#read the normal colour
		self.foregroundcolour= self.GetForegroundColour()
		#prepare the value according rounding
		self.rounder()
		self.ChangeValue(self.init_valStr)
		self.oldvalue = self.init_val
		
		
		self.edita = 1
		#bind the input of a value with the check
		self.Bind(wx.EVT_KEY_DOWN, self.checkValueKey)#needs style wx.TE_PROCESS_ENTER
		#mouse events
		self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)
		self.mouseUsage = 0
		self.initpos = (0,0)
		self.initvalM = 0
		self.Bind(wx.EVT_MOTION, self.mouseMove)
		self.Bind(wx.EVT_LEFT_DCLICK, self.onLClick)
		self.Bind(wx.EVT_LEFT_UP, self.onLRelease)
		
	def mouseMove(self, evt):
		"""handles mouse movements to modify value"""
		if self.HasCapture() and self.mouseUsage == 1:
			actpos = evt.GetPositionTuple()
			#mouse movements here
			if self.mousev == 1:
				#vertical mouse movement
				move = self.initpos[1] - actpos[1]
			else:
				move = actpos[0] - self.initpos[0]
			#print move
			self.init_val = self.initvalM + move * (self.max_val - self.min_val) * self.mmhs
			self.rangechk()
			self.ChangeValue(self.init_valStr)
			self.oldvalue = self.init_val
			self.edita = 1
		evt.Skip()
		
	def onLClick(self, evt):
		"""Activate mouse movement listening"""
		#set initial position and movement
		self.initpos=evt.GetPositionTuple()
		self.initvalM = self.init_val
		self.CaptureMouse()
		self.mouseUsage = 1


	def onLRelease(self, evt):
		"""Quit mouse movement listening"""
		if self.HasCapture():
			self.ReleaseMouse()
		self.mouseUsage = 0


	def rounder(self):
		"""round the mumber and create the string to visualize
		according to fractionWidth"""
		self.init_val = round(self.init_val, self.fractionWidth)
		self.init_valStr = ("%."+str(self.fractionWidth) +"f") % self.init_val


	def rangechk(self):
		"""bound current value within min and max values"""
		if self.init_val > self.max_val:
			self.init_val = self.max_val
		elif self.init_val < self.min_val:
			self.init_val = self.min_val
		self.rounder()


	def SetValueC(self, value):
		if self.edita == 1:
			"""to set value of the widget from outside"""
			self.init_val = value
			self.rangechk()
			self.ChangeValue(self.init_valStr)
			self.oldvalue = self.init_val

	def SetValue(self, value):
		"""to set value of the widget"""
		self.init_val = value
		self.rangechk()
		self.ChangeValue(self.init_valStr)
		self.oldvalue = self.init_val
		

	def checkValueKey(self, evt):
		"""keyboard input"""
		if self.mouseUsage == 0:
			self.edita = 0
			self.SetForegroundColour(self.colWaitConf)
			keycode = evt.GetKeyCode()
			if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER: 
				try:
					self.init_val = float(self.GetValue())
					self.rangechk()
					self.ChangeValue(self.init_valStr)
					self.oldvalue = self.init_val
				except ValueError:
					self.init_val = self.oldvalue
					self.ChangeValue(self.init_valStr)
				self.SetForegroundColour(self.foregroundcolour)
				self.edita = 1
			#print "key edita = %i value = %f" % (self.edita, self.init_val)
		evt.Skip()


	def onMouseWheel(self, evt):
		"""mouse wheel input""" 
		self.edita = 0
		#print evt.GetWheelDelta()
		wheel_rotation = evt.GetWheelRotation() / 120.0
		self.init_val = wheel_rotation * (self.max_val - self.min_val) * self.mwhs + self.init_val
		self.rangechk()
		self.ChangeValue(self.init_valStr)
		self.oldvalue = self.init_val
		self.edita = 1
		#print self.init_val
		evt.Skip()




class TxtCtrlNumCs(TxtCtrlNum):
	"""transmit to a Csound Channel"""
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		self.channel = k.pop('channel', None)
		super(TxtCtrlNumCs, self).__init__(*a, **k)#super the subclass

	def mouseMove(self, evt):
		"""
		Handles mouse movements to modify value
		Added csound send to the original class
		non need to Bind since binding is in the parent class
		"""
		if self.HasCapture() and self.mouseUsage == 1:
			actpos = evt.GetPositionTuple()
			#mouse movements here
			if self.mousev == 1:
				#vertical mouse movement
				move = self.initpos[1] - actpos[1]
			else:
				move = actpos[0] - self.initpos[0]
			#print move
			self.init_val = self.initvalM + move * (self.max_val - self.min_val) * self.mmhs
			self.rangechk()
			self.ChangeValue(self.init_valStr)
			self.oldvalue = self.init_val
			self.edita = 1
			self.cSound.SetChannel(self.channel, self.init_val)
		evt.Skip()


	def checkValueKey(self, evt):
		"""keyboard input 
		Added csound send to the original class
		non need to Bind since binding is in the parent class
		"""
		self.edita = 0
		self.SetForegroundColour(self.colWaitConf)
		keycode = evt.GetKeyCode()
		if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER: 
			try:
				self.init_val = float(self.GetValue())
				self.rangechk()
				self.ChangeValue(self.init_valStr)
				self.oldvalue = self.init_val
			except ValueError:
				self.init_val = self.oldvalue
				self.ChangeValue(self.init_valStr)
			self.SetForegroundColour(self.foregroundcolour)
			self.edita = 1
		#print "key edita = %i value = %f" % (self.edita, self.init_val)
		self.cSound.SetChannel(self.channel, self.init_val)
		evt.Skip()
		
		
	def onMouseWheel(self, evt):
		"""mouse wheel input
		Added csound send to the original class
		non need to Bind since binding is in the parent class
		"""
		self.edita = 0
		#print evt.GetWheelDelta()
		wheel_rotation = evt.GetWheelRotation() / 120.0
		self.init_val = wheel_rotation * (self.max_val - self.min_val) * self.mwhs + self.init_val
		self.rangechk()
		self.ChangeValue(self.init_valStr)
		self.oldvalue = self.init_val
		self.edita = 1
		#print self.init_val
		self.cSound.SetChannel(self.channel, self.init_val)
		evt.Skip()




class TxtCtrlNumTs(TxtCtrlNum):
	"""transmit to a Csound ftable index"""
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		#self.cSound_perf = k.pop('cSound_perf', None)
		self.indxN = k.pop('indxn', None)
		self.tabN = k.pop('ftable', None)
		super(TxtCtrlNumTs, self).__init__(*a, **k)#super the subclass

	def mouseMove(self, evt):
		"""
		Handles mouse movements to modify value
		Added csound send to the original class
		non need to Bind since binding is in the parent class
		"""
		if self.HasCapture() and self.mouseUsage == 1:
			actpos = evt.GetPositionTuple()
			#mouse movements here
			if self.mousev == 1:
				#vertical mouse movement
				move = self.initpos[1] - actpos[1]
			else:
				move = actpos[0] - self.initpos[0]
			#print move
			self.init_val = self.initvalM + move * (self.max_val - self.min_val) * self.mmhs
			self.rangechk()
			self.ChangeValue(self.init_valStr)
			self.oldvalue = self.init_val
			self.edita = 1
			self.cSound.TableSet(self.tabN, self.indxN, self.init_val)
		evt.Skip()


	def checkValueKey(self, evt):
		"""keyboard input 
		Added csound send to the original class
		non need to Bind since binding is in the parent class
		"""
		self.edita = 0
		self.SetForegroundColour(self.colWaitConf)
		keycode = evt.GetKeyCode()
		if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER: 
			try:
				self.init_val = float(self.GetValue())
				self.rangechk()
				self.ChangeValue(self.init_valStr)
				self.oldvalue = self.init_val
			except ValueError:
				self.init_val = self.oldvalue
				self.ChangeValue(self.init_valStr)
			self.SetForegroundColour(self.foregroundcolour)
			self.edita = 1
		#print "key edita = %i value = %f" % (self.edita, self.init_val)
		#self.cSound.SetChannel(self.channel, self.init_val)
		self.cSound.TableSet(self.tabN, self.indxN, self.init_val)
		evt.Skip()
		
		
	def onMouseWheel(self, evt):
		"""mouse wheeel input
		Added csound send to the original class
		non need to Bind since binding is in the parent class
		"""
		self.edita = 0
		#print evt.GetWheelDelta()
		wheel_rotation = evt.GetWheelRotation() / 120.0
		self.init_val = wheel_rotation * (self.max_val - self.min_val) * self.mwhs + self.init_val
		self.rangechk()
		self.ChangeValue(self.init_valStr)
		self.oldvalue = self.init_val
		self.edita = 1
		#print self.init_val
		self.cSound.TableSet(self.tabN, self.indxN, self.init_val)
		evt.Skip()






#example
if __name__ == '__main__':
	class MyFrame(wx.Frame):
		def __init__(self, parent, id):
			wx.Frame.__init__(self, parent, id, 'Test', size = (180, 100))
			panel = wx.Panel(self)
			"""
			input = TxtCtrlNum(panel, -1, size=(70,20),
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,#NEEDED FOR CONFIRMATION and colour change
				min_val = 0.2,#min_val range value
				max_val = 3.9,#max_val range value
				init_val = 0.5,#init_val value
				fractionWidth = 5,#number of decimals
				colWaitConf="red", #background colour while waiting for confirmation
				mwhs=0.01) #mouse wheel sensitivity
			"""
			input = TxtCtrlNum(panel, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = -0.5)
	app = wx.App(redirect = False)
	frame = MyFrame(parent = None, id = -1)
	frame.Show()
	app.MainLoop()