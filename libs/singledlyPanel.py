import wx
import floatspinmouse

class SingleDlyPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(SingleDlyPanel, self).__init__(*a, **k)#super the subclass
		self.mainSizer = wx.GridBagSizer(vgap=5, hgap=5)
		self.tabN = 100
		
		siz=wx.Size(70,-1)#size of floatspin
		
		idT = wx.StaticText(self, -1, "ID:", style= wx.ALIGN_RIGHT)
		self.idV= "0"
		self.id = wx.StaticText(self, -1, self.idV, style= wx.ALIGN_LEFT, size=(20,20))
		
		#time_index = 1
		timeT = wx.StaticText(self, -1, "Time:", style= wx.ALIGN_RIGHT)
		#self.timeV= str(self.cSound.TableGet(self.tabN, 1))
		self.timeV= "0"
		self.time = wx.StaticText(self, -1, self.timeV, style= wx.ALIGN_LEFT, size=(50,20))
		
		#semit_index = 2
		semitT = wx.StaticText(self, -1, "Semitones:", style= wx.ALIGN_RIGHT)
		#self.semitV= str(self.cSound.TableGet(self.tabN, 2))
		self.semitV = "0"
		self.semit = wx.StaticText(self, -1, self.semitV, style= wx.ALIGN_LEFT, size=(50,20))		
		
		#feed_index = 4
		feedT = wx.StaticText(self, -1, "Feedback", style= wx.ALIGN_RIGHT)
		self.feed = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 1.0,
																			increment=0.001,
																			value = 0.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 4)
		self.feed.SetValue(self.cSound.TableGet(self.tabN, 4))
		
		
		#lf_index = 5
		lfT = wx.StaticText(self, -1, "LF", style= wx.ALIGN_RIGHT)
		self.lf = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=1,
																			min_val = 20.0,
																			max_val = 15000.0,
																			increment=1.0,
																			value = 0.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 5)
		self.lf.SetValue(self.cSound.TableGet(self.tabN, 5))
		
		
		
		#hf_index = 6
		hfT = wx.StaticText(self, -1, "HF", style= wx.ALIGN_RIGHT)
		self.hf = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=1,
																			min_val = 20.0,
																			max_val = 15000.0,
																			increment=1.0,
																			value = 15000.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 6)
		self.hf.SetValue(self.cSound.TableGet(self.tabN, 6))
		
		#pan_index = 7
		panT = wx.StaticText(self, -1, "Pan", style= wx.ALIGN_RIGHT)
		self.pan = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 1.0,
																			increment=0.001,
																			value = 0.5,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 7)
		self.pan.SetValue(self.cSound.TableGet(self.tabN, 7))
		
		#reso_index = 8
		resoT = wx.StaticText(self, -1, "Resonance", style= wx.ALIGN_RIGHT)
		self.reso = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 2.0,
																			increment=0.01,
																			value = 0.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 8)
		self.reso.SetValue(self.cSound.TableGet(self.tabN, 8))
		
		
		
		#envfollow_index = 14 
		self.envfollowOpt = {"off": 0, "d-u":1, "u-d":2}
		self.envfollowOptNames = self.envfollowOpt.keys()
		envfollowT = wx.StaticText(self, -1, "Env Follow", style= wx.ALIGN_RIGHT)
		self.envfollow = wx.ComboBox(self, -1, choices=self.envfollowOptNames, size=wx.Size(60, 20))
		self.Bind(wx.EVT_COMBOBOX, self.envFollowDirection, self.envfollow)
		self.envfollow.SetValue("off")
		#self.feed.SetValue(self.cSound.TableGet(self.tabN, 14))
		
		
		#dist_index = 9
		distT = wx.StaticText(self, -1, "Distortion", style= wx.ALIGN_RIGHT)
		self.dist = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 1.0,
																			increment=0.01,
																			value = 0.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 9)
		self.dist.SetValue(self.cSound.TableGet(self.tabN, 9))
		
		
		#Routing
		#In direct index 10
		volinT = wx.StaticText(self, -1, "Vol In", style= wx.ALIGN_RIGHT)
		self.volin = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.01,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 10)
		self.volin.SetValue(self.cSound.TableGet(self.tabN, 10))		
		#In recycle delay index 11
		volinrT = wx.StaticText(self, -1, "Vol from\nRecycle", style= wx.ALIGN_RIGHT)
		self.volinr = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.01,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 11)
		self.volinr.SetValue(self.cSound.TableGet(self.tabN, 11))				
			
		#Out to output
		#vol_index = 12
		volT = wx.StaticText(self, -1, "Vol Out", style= wx.ALIGN_RIGHT)
		self.vol = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.01,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 12)
		self.vol.SetValue(self.cSound.TableGet(self.tabN, 12))
		
		#Out to recycler index 13
		volrT = wx.StaticText(self, -1, "Vol to\nRecycle", style= wx.ALIGN_RIGHT)
		self.volr = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.01,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = self.tabN,
																			indxn = 13)
		self.volr.SetValue(self.cSound.TableGet(self.tabN, 13))
		
		
		
		
		#Display
		self.mainSizer.Add(idT, (0,0))
		self.mainSizer.Add(self.id, (0,1))
		self.mainSizer.Add(timeT, (0,2))
		self.mainSizer.Add(self.time, (0,3))
		self.mainSizer.Add(semitT, (0,4))
		self.mainSizer.Add(self.semit, (0,5))
		self.mainSizer.Add(feedT, (0,6))
		self.mainSizer.Add(self.feed, (0,7))
		self.mainSizer.Add(lfT, (0,8))
		self.mainSizer.Add(self.lf, (0,9))
		self.mainSizer.Add(hfT, (0,10))
		self.mainSizer.Add(self.hf, (0,11))
		self.mainSizer.Add(panT, (0,12))
		self.mainSizer.Add(self.pan, (0,13))
		self.mainSizer.Add(resoT, (0,14))
		self.mainSizer.Add(self.reso, (0,15))
		self.mainSizer.Add(distT, (0,16))
		self.mainSizer.Add(self.dist, (0,17))
		self.mainSizer.Add(envfollowT, (0,18))
		self.mainSizer.Add(self.envfollow, (0,19))
		self.mainSizer.Add(volinT, (1,10))
		self.mainSizer.Add(self.volin, (1,11))
		self.mainSizer.Add(volinrT, (1,12))
		self.mainSizer.Add(self.volinr, (1,13))
		self.mainSizer.Add(volrT, (1,14))
		self.mainSizer.Add(self.volr, (1,15))
		self.mainSizer.Add(volT, (1,16))
		self.mainSizer.Add(self.vol, (1,17))
		self.SetSizer(self.mainSizer)
		self.mainSizer.Fit(self)
		

	def setTable(self, tabNew):
		"""update the values when called from external object"""
		self.tabN = tabNew
		self.id.SetLabel(str(self.tabN - 100))
		self.time.SetLabel("%.3f" % (self.cSound.TableGet(self.tabN, 1)))
		self.semit.SetLabel("%.3f" % (self.cSound.TableGet(self.tabN, 2)))
		self.feed.tabN = self.tabN
		self.feed.SetValue(self.cSound.TableGet(self.tabN, 4))
		self.lf.tabN = self.tabN
		self.lf.SetValue(self.cSound.TableGet(self.tabN, 5))
		self.hf.tabN = self.tabN
		self.hf.SetValue(self.cSound.TableGet(self.tabN, 6))
		self.pan.tabN = self.tabN
		self.pan.SetValue(self.cSound.TableGet(self.tabN, 7))
		self.reso.tabN = self.tabN		
		self.reso.SetValue(self.cSound.TableGet(self.tabN, 8))
		self.dist.tabN = self.tabN
		self.dist.SetValue(self.cSound.TableGet(self.tabN, 9))
		
		self.volin.tabN = self.tabN
		self.volin.SetValue(self.cSound.TableGet(self.tabN, 10))	
		self.volinr.tabN = self.tabN
		self.volinr.SetValue(self.cSound.TableGet(self.tabN, 11))	
		
		self.vol.tabN = self.tabN		
		self.vol.SetValue(self.cSound.TableGet(self.tabN, 12))	
		self.volr.tabN = self.tabN		
		self.volr.SetValue(self.cSound.TableGet(self.tabN, 13))
		#
		#envfollowkey = self.envfollowOpt.keys()[self.envfollowOpt.values().index(self.cSound.TableGet(self.tabN, 14))]
		envfollowkey = self.envfollowOpt.keys()[self.envfollowOpt.values().index(self.cSound.TableGet(tabNew, 14))]
		self.envfollow.SetValue(envfollowkey)
		#self.mainSizer.Layout()
		self.Layout()  #Either works

	def envFollowDirection(self, evt):
		"set the envelope follower direction"
		mode = self.envfollowOpt[self.envfollowOptNames[self.envfollow.GetSelection()]]
		print mode
		print self.tabN
		self.cSound.TableSet(self.tabN, 14, mode)

	def emitVal(self, evt, index):
		print index
		print self.feed.GetValue()
