
class PlotLine:
    def __init__(self):
        self.data = None
        self.index = 0
        self.data_line = None
        self.pen = None
        self.name = None
        self.ishidden = False
        self.ChannelNum = None
        self.moved = False
        self.isstopped = False
        self.maxmiumTime=0
        self.minimumAmplitude=0
        self.maxmiumAmplitude=0
        self.timeMean=0
        self.amplitudeMean=0
        self.StatisticalData=[]
        # self.timer