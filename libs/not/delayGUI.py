import wx
import csnd6
import txtctrlnum

class DelayFrame(wx.Frame):
	"""Main frame"""
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.tabN = k.pop('table', None)#the ftable associated to this delay unit
		super(DelayFrame, self).__init__(*a, **k)#super the subclass
		"""
		print 'DelayFrame'
		print self.tabN 
		print type(self.tabN)#ok
		"""
		#font = wx.Font(13, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		sizer = wx.GridBagSizer(vgap=10, hgap=5)
		#etext = wx.StaticText(self, 0, label='EFFECTTTT')
		#etext.SetFont(font)
		#time_index = 1
		timeT = wx.StaticText(self, -1, "Time", style= wx.ALIGN_LEFT)
		self.timeV= str(self.cSound.TableGet(self.tabN, 1))
		self.time = wx.StaticText(self, -1, self.timeV, style= wx.ALIGN_LEFT)
		
		#semit_index = 2
		semitT = wx.StaticText(self, -1, "Semitones", style= wx.ALIGN_LEFT)
		self.semitV= str(self.cSound.TableGet(self.tabN, 2))
		self.semit = wx.StaticText(self, -1, self.semitV, style= wx.ALIGN_LEFT)		
		
		#semit_index = 3
		qualityT = wx.StaticText(self, -1, "Quality", style= wx.ALIGN_LEFT)
		self.quality = txtctrlnum.TxtCtrlNumTs(self, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = 0.0,
				max_val = 1.0,
				init_val = 0.0,
				cSound = self.cSound,
				ftable = self.tabN,
				indxn = 3)
		self.quality.SetValue(self.cSound.TableGet(self.tabN, 3))		
			
		
		#feed_index = 4
		feedT = wx.StaticText(self, -1, "Feedback", style= wx.ALIGN_LEFT)
		self.feed = txtctrlnum.TxtCtrlNumTs(self, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = 0.0,
				max_val = 1.0,
				init_val = 0.0,
				cSound = self.cSound,
				ftable = self.tabN,
				indxn = 4)
		self.feed.SetValue(self.cSound.TableGet(self.tabN, 4))
		
		#lf_index = 5
		lfT = wx.StaticText(self, -1, "Low Frequency", style= wx.ALIGN_LEFT)
		self.lf = txtctrlnum.TxtCtrlNumTs(self, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = 20.0,
				max_val = 15000.0,
				init_val = 20.0,
				cSound = self.cSound,
				ftable = self.tabN,
				indxn = 5)
		self.lf.SetValue(self.cSound.TableGet(self.tabN, 5))
		
		#hf_index = 6
		hfT = wx.StaticText(self, -1, "High Frequency", style= wx.ALIGN_LEFT)
		self.hf = txtctrlnum.TxtCtrlNumTs(self, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = 20.0,
				max_val = 15000.0,
				init_val = 15000.0,
				cSound = self.cSound,
				ftable = self.tabN,
				indxn = 6)
		self.hf.SetValue(self.cSound.TableGet(self.tabN, 6))
		
		#pan_index = 7
		panT = wx.StaticText(self, -1, "Pan", style= wx.ALIGN_LEFT)
		self.pan = txtctrlnum.TxtCtrlNumTs(self, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = 0.0,
				max_val = 1.0,
				init_val = 0.5,
				cSound = self.cSound,
				ftable = self.tabN,
				indxn = 7)
		self.pan.SetValue(self.cSound.TableGet(self.tabN, 7))
		
		#vol_index = 8
		volT = wx.StaticText(self, -1, "Volume", style= wx.ALIGN_LEFT)
		self.vol = txtctrlnum.TxtCtrlNumTs(self, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = 0.0,
				max_val = 10.0,
				init_val = 1.0,
				cSound = self.cSound,
				ftable = self.tabN,
				indxn = 8)
		self.vol.SetValue(self.cSound.TableGet(self.tabN, 8))		
		
		sizer.Add(timeT, pos=(0,0))
		sizer.Add(self.time, pos=(0,1))
		sizer.Add(semitT, pos=(1,0))
		sizer.Add(self.semit, pos=(1,1))
		sizer.Add(qualityT, pos=(2,0))
		sizer.Add(self.quality, pos=(2,1))
		sizer.Add(feedT, pos=(3,0))
		sizer.Add(self.feed, pos=(3,1))
		sizer.Add(lfT, pos=(4,0))
		sizer.Add(self.lf, pos=(4,1))
		sizer.Add(hfT, pos=(5,0))
		sizer.Add(self.hf, pos=(5,1))
		sizer.Add(panT, pos=(6,0))
		sizer.Add(self.pan, pos=(6,1))	
		sizer.Add(volT, pos=(7,0))
		sizer.Add(self.vol, pos=(7,1))
		
		self.SetSizer(sizer)
		sizer.Fit(self)
		
		self.Bind(wx.EVT_CLOSE, self.on_close)



	def receiveValue(self, evt):
		"""receive from csound ftable"""
		#self.SetValue(readFromTable(self.cSound, self.tabN, self.indexIn))
		pass
		
		
	def on_close(self, evt):
		'''remove itself from the parent list of open istances
		then destroy itself'''
		for item in self.GetParent().openDelayFrames:
			if item == self:
				self.GetParent().openDelayFrames.remove(item)
		self.Destroy()