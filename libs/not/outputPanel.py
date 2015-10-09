import wx


class OutputPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(OutputPanel, self).__init__(*a, **k)#super the subclass
		self.SetBackgroundColour((100, 0, 200))
		