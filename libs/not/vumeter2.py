import wx


class VuMeter(wx.Panel):
	def __init__(self, *a, **k):
		self.dcw =  k.pop('dcw', None)
		self.dch = k.pop('dch', None)
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		self.channel = k.pop('cSound_chan', None)
		self.refreshVal = k.pop('refresh', None)
		super(VuMeter, self).__init__(*a, **k)#super the subclass
		#mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.decibels = 0.0
		
		#timer to update Value
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(self.refreshVal)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timerRefresh)
		
		self.bord = 10
		self.InitBuffer()
		self.Bind(wx.EVT_PAINT, self.OnPaint)#paint event
		
		
	def OnTimer(self,evt):
		"""get the db value"""
		self.decibels = self.cSound.GetChannel(self.channel)
		print self.decibels
		#generate an PAINT EVENT
		#wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
		#self.GetEventHandler().ProcessEvent(wx.PaintEvent( ))
		#dc = wx.BufferedPaintDC(self, self.buffer)
		dc = wx.BufferedPaintDC(wx.ClientDC(self))
		self.DrawIt(dc)


		
	def InitBuffer(self):
		"""initialize drawing buffer"""
		self.buffer = wx.EmptyBitmap(self.dcw, self.dch)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		#print dc.GetSize() 
		dc.SetBackgroundMode(wx.TRANSPARENT)
		self.DrawIt(dc)
		

	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self, self.buffer)
		self.DrawIt(dc)

	
		

	def DrawIt(self, dc):
		"""Drawing procedure"""
		dc.SetDeviceOrigin(0, 0)
		dc.SetBackgroundMode(wx.TRANSPARENT)
		dc.Clear()
		dc.DrawRectangle(self.bord, self.bord, self.dcw-2* self.bord, self.dch-2* self.bord)
		
		#dc.DrawRectangle(self.bord, self.bord + int(self.decibels / (self.dch-2 * self.bord)), self.dcw-2 * self.bord, self.dch-2 * self.bord)
		txtH = 9
		dc.SetFont(wx.Font(txtH - 1, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
		dc.SetPen(wx.Pen('BLUE', 1, wx.SOLID))
		dc.DrawText(str(self.decibels),  10, 10)
		#self.Refresh()

		
