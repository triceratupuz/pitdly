import wx
import pickle
#import floatspinmouse

class PresetPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(PresetPanel, self).__init__(*a, **k)#super the subclass
		self.initColour = (100, 100, 100)
		self.SetBackgroundColour(self.initColour)
		
		siz=wx.Size(70,-1)#size of floatspin
		
		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#PresetNumber
		self.currentpreset = 1
		self.presetNumber = wx.SpinCtrl(self, value='1', size=siz)
		self.presetNumber.SetRange(1, 127)
		self.presetNumber.Bind(wx.EVT_SPINCTRL, self.pnDo)
		
		#Load Button
		self.loadbtn = wx.Button(self, label='Load', size = siz)
		self.loadbtn.Bind(wx.EVT_BUTTON, self.loadDo)
		
		#Save Button
		self.savebtn = wx.Button(self, label='Save', size = siz)
		self.savebtn.Bind(wx.EVT_BUTTON, self.saveDo)
		
		#PresetName
		fontpname = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
		self.pnamet = wx.StaticText(self, -1, "Preset Name", style= wx.ALIGN_RIGHT)
		self.pname = wx.TextCtrl(self, -1, size = wx.Size(300,-1), style=wx.TE_RICH)
		self.pname.SetFont(fontpname)
		
		self.mainSizer.Add(self.presetNumber, 0,flag=wx.EXPAND)
		self.mainSizer.Add(self.loadbtn, 0,flag=wx.EXPAND)
		self.mainSizer.Add(self.savebtn, 0,flag=wx.EXPAND)
		self.mainSizer.Add(self.pnamet, -1,flag=wx.EXPAND)
		self.mainSizer.Add(self.pname, 0,flag=wx.EXPAND)
		self.SetSizer(self.mainSizer)
		self.mainSizer.Fit(self)



	def pnDo(self, evt):
		'''background in red to call for furter action'''
		if self.presetNumber.GetValue() <> self.currentpreset:
			self.SetBackgroundColour((250, 0, 0))
		else:
			self.SetBackgroundColour(self.initColour)
		self.Refresh()
		
		
	def loadDo(self, evt):
		'''load parameters stored in a file'''
		#Turnoff all the sctive delays
		for delay in self.GetParent().matrixSeqP.gridPan.points:
			if delay[0] >= 0.0:
				index = self.GetParent().matrixSeqP.gridPan.points.index(delay)
				self.cSound.InputMessage('i %f 0 -1' %(-30 - self.GetParent().matrixSeqP.gridPan.points[index][0] * 0.001))
		#Begin
		self.SetBackgroundColour(self.initColour)
		self.Refresh()
		#print "Load"
		file = "save/save.%03d" % self.presetNumber.GetValue()
		storedList = pickle.load( open( file, "rb" ) )
		#setting values
		self.pname.SetValue(storedList[0])
		#Monostereo
		self.GetParent().matrixSeqP.inPanel.monoStereo.SetValue(storedList[1])
		if storedList[1]:
			val_ms = 1
		else:
			val_ms = 0
		self.cSound.TableSet(99, 0, val_ms)
		#
		self.GetParent().matrixSeqP.inPanel.gain.SetValue(storedList[2])
		self.cSound.TableSet(99, 11, storedList[2])#to csound table
		#
		self.GetParent().matrixSeqP.gainI.SetValue(storedList[3])
		self.cSound.TableSet(99, 7, storedList[3])#to csound table
		#
		self.GetParent().matrixSeqP.gainD.SetValue(storedList[4])
		self.cSound.TableSet(99, 8, storedList[4])#to csound table
		#
		self.GetParent().matrixSeqP.gainR.SetValue(storedList[5])
		self.cSound.TableSet(99, 9, storedList[5])#to csound table
		#
		self.GetParent().matrixSeqP.limit.SetValue(storedList[6])
		if storedList[6]:
			val_lim = 1
		else:
			val_lim = 0
		self.cSound.TableSet(99, 10, val_lim)
		#display recycle (also on/off indicator)
		if storedList[7] <= 0:#if not valid recycle time value
			self.GetParent().matrixSeqP.inPanel.Recycle.SetLabel('Off')
			self.GetParent().matrixSeqP.inPanel.time.SetLabel('0')
			self.cSound.InputMessage('i -40 0.0 -1')
			#deactivate instrument in csound (to do)
		else:#if valid recycle time value
			self.GetParent().matrixSeqP.inPanel.Recycle.SetLabel('ON')
			self.GetParent().matrixSeqP.inPanel.time.SetLabel(str(storedList[7]))
			self.cSound.TableSet(99, 1, storedList[7])
			self.cSound.InputMessage('i 40 0.02 -1')
		#display recycle feed
		self.GetParent().matrixSeqP.inPanel.feed.SetValue(storedList[8])
		self.cSound.TableSet(99, 2, storedList[8])#to csound table
		#recycle time for grid panel 
		self.GetParent().matrixSeqP.gridPan.recycle = storedList[7]
		#
		self.GetParent().matrixSeqP.gridPan.points = storedList[9]
		#Csound operation
		for evento in storedList[9]:
			ftable = 'f %i 0 16 -2 %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f' % (evento[0] + 100, evento[0], evento[1], evento[2], evento[3], 
																													evento[4], evento[5], evento[6], evento[7], evento[8], evento[9], 
																													evento[10], evento[11], evento[12], evento[13], evento[14])
			instr = 'i %f 0.02 -1' % (30.0 + evento[0] * 0.001)
			self.cSound.InputMessage(ftable + '\n' + instr)
		#redraw grid
		self.GetParent().matrixSeqP.gridPan.Refresh()#Causes freezing and crash?
		#print "refresh done"
		#csound Istruments management necessary?
		#self.GetParent().matrixSeqP.gridPan.Update()#?
		#recycle HP
		self.GetParent().matrixSeqP.inPanel.recycleHP.SetValue(storedList[10])
		self.cSound.TableSet(99, 5, storedList[10])#to csound table
		#recycle HP
		self.GetParent().matrixSeqP.inPanel.recycleLP.SetValue(storedList[11])
		self.cSound.TableSet(99, 6, storedList[11])#to csound table
		#recycle direct in
		self.GetParent().matrixSeqP.inPanel.recycleLP.SetValue(storedList[12])
		self.cSound.TableSet(99, 3, storedList[12])#to csound table


	def saveDo(self, evt):
		'''save parameters in a file'''
		self.SetBackgroundColour(self.initColour)
		self.Refresh()
		#print "Save"
		#store values in a list 
		storedList = [self.pname.GetValue(),#presetname 
						self.GetParent().matrixSeqP.inPanel.monoStereo.GetValue(),#monostereoInputPanel
						self.GetParent().matrixSeqP.inPanel.gain.GetValue(),
						self.GetParent().matrixSeqP.gainI.GetValue(),#gainIDlyPanel
						self.GetParent().matrixSeqP.gainD.GetValue(),
						self.GetParent().matrixSeqP.gainR.GetValue(),
						self.GetParent().matrixSeqP.limit.GetValue(),
						self.GetParent().matrixSeqP.gridPan.recycle,#recycle
						self.GetParent().matrixSeqP.inPanel.feed.GetValue(),
						self.GetParent().matrixSeqP.gridPan.points,
						self.GetParent().matrixSeqP.inPanel.recycleHP.GetValue(),
						self.GetParent().matrixSeqP.inPanel.recycleLP.GetValue(),
						self.GetParent().matrixSeqP.inPanel.recycleIn.GetValue()]
		#print storedList
		#grid pan points
		#self.cSound.TableGet(self.tabN, 4)
		for item in storedList[9]:
			if item[0] > 0:
				ftab = item[0] + 100
				indx = 4
				while indx < 15:
					item[indx] = self.cSound.TableGet(ftab, indx)
					indx += 1
				
		file = "save/save.%03d" % self.presetNumber.GetValue()
		pickle.dump( storedList, open( file, "wb" ) )#put stored list in pickle dump
		