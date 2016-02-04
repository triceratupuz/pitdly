import wx
import wx.lib.agw.floatspin
import csnd6

'''
Subclassing of
http://wxpython.org/Phoenix/docs/html/lib.agw.floatspin.html to add:
- mouse movement control
- csound comunication

NOTE:
Needs at least explicit declaration of following wx.lib.agw.floatspin.FloatSpin arguments 
parent=, id=,digits=,min_val=, max_val=, increment=,value=
at istantiation

Rev 20160204
'''



class Fsm(wx.lib.agw.floatspin.FloatSpin):
	def __init__(self, *args, **kwargs):
		'''Needs explicit declaration of wx.lib.agw.floatspin.FloatSpin
		'''
		#mouse movement
		#default vertical = 1 horixontal =0
		self.mousev = kwargs.pop('mousev', None)
		if self.mousev is None: self.mousev = 1
		#incremet related to mouse movement
		self.increment_m = kwargs.pop('increment_m', None)
		if self.increment_m  == None: self.increment_m = 0.01
		'''
		if kwargs.__contains__('mousev'):
			self._interval_m = kwargs['mousev']
			kwargs.__delitem__('mousev')
		if kwargs.__contains__('interval_m'):
			self._interval_m = kwargs['interval_m']
			kwargs.__delitem__('interval_m')
		'''
		super(Fsm, self).__init__(*args, **kwargs)
		
		self._textctrl.Bind(wx.EVT_LEFT_DCLICK, self.onLClick_double)
		self.Bind(wx.EVT_LEFT_UP, self.onLRelease)
		self.Bind(wx.EVT_MOTION, self.mouseMove)
		self.Bind(wx.lib.agw.floatspin.EVT_FLOATSPIN, self.emitValue)

	def onLClick_double(self, evt):
		'''self.tap_ - Double click and hold to mouse movement'''
		if self.mousev:
			myCursor= wx.StockCursor(wx.CURSOR_SIZENS)
		else:
			myCursor= wx.StockCursor(wx.CURSOR_SIZEWE)
		self.SetCursor(myCursor)
		#set initial position and movement
		self.initpos = evt.GetPositionTuple()
		self.initvalMouse = self.GetValue()
		self.CaptureMouse()
		evt.Skip

	def onLRelease(self, evt):
		'''self.tap_ - release mouse capture'''
		if self.HasCapture():
			myCursor= wx.StockCursor(wx.CURSOR_ARROW)
			self.SetCursor(myCursor)
			self.ReleaseMouse()
		evt.Skip

	def mouseMove(self, evt):
		#print "wx.EVT_MOTION"
		if self.HasCapture():
			actpos = evt.GetPositionTuple()
			#mouse movements here
			if self.mousev == 1:
				move = self.initpos[1] - actpos[1]
			else:
				move = actpos[0] - self.initpos[0]
			#print move
			min = self.GetMin()
			max = self.GetMax()
			val = self.initvalMouse + move * (max - min) * self.increment_m
			if val < min: val = min#to overcome internal value checking
			if val > max: val = max#to overcome internal value checking
			self.SetValue(val)
			self.emitValue(evt)
		evt.Skip()
		
	def emitValue(self, evt):
		pass



class FsmCs(Fsm):
    '''transmit value to a csound software channel and execute passed function'''
    def __init__(self, *args, **kwargs):
        self.cSound = kwargs.pop('cSound', None)
        self.channel = kwargs.pop('channel', None)
        super(FsmCs, self).__init__(*args, **kwargs)

    def emitValue(self, evt):
        '''transmission'''
        self.cSound.SetChannel(self.channel, self.GetValue())



class FsmCsF(Fsm):
    '''transmit value to a csound software channel
    and perform a function'''
    def __init__(self, *args, **kwargs):
        self.cSound = kwargs.pop('cSound', None)
        self.channel = kwargs.pop('channel', None)
        self.funct = kwargs.pop('funct', None)
        super(FsmCsF, self).__init__(*args, **kwargs)

    def emitValue(self, evt):
        '''transmission'''
        self.cSound.SetChannel(self.channel, self.GetValue())
        self.funct()



class FsmTs(Fsm):
    '''transmit value to a csound table'''
    def __init__(self, *args, **kwargs):
        self.cSound = kwargs.pop('cSound', None)
        self.indxN = kwargs.pop('indxn', None)
        self.tabN = kwargs.pop('ftable', None)
        super(FsmTs, self).__init__(*args, **kwargs)

    def emitValue(self, evt):
        '''transmission'''
        self.cSound.TableSet(self.tabN, self.indxN, self.GetValue())
 



class FsmTsF(Fsm):
    '''transmit value to a csound table
    and perform a function'''
    def __init__(self, *args, **kwargs):
        self.cSound = kwargs.pop('cSound', None)
        self.indxN = k.pop('indxn', None)
        self.tabN = k.pop('ftable', None)
        self.funct = kwargs.pop('funct', None)
        super(FsmTsF, self).__init__(*args, **kwargs)

    def emitValue(self, evt):
        '''transmission'''
        self.cSound.TableSet(self.tabN, self.indxN, self.GetValue())
        self.funct()
        



if __name__ == '__main__':
    class MyFrame(wx.Frame):
        def __init__(self, parent, id):
            wx.Frame.__init__(self, parent, id, 'Test', size = (180, 100))
            panel = wx.Panel(self)
            #input = FloatSpinMouse(panel, -1)
            #input = FloatSpinMouse(parent=panel, id=-1,digits= 3,min_val=0.0, max_val= 12.0)
            input = Fsm(parent=panel, id=-1,digits= 3,min_val=0.0, max_val= 2.103, increment= 0.05,increment_m= 0.001)
            input.SetValue(0.66)
            font = wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
            input.SetFont(font)
    app = wx.App(redirect=False)
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()