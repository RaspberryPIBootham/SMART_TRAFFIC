class TurnData:
	def __init__(self,mMaxTime):
		self.Start=0
		self.End=0
		self.MaxTime=mMaxTime
		self.Lanes=list()
		self.Slots=list()
	def AddLane(self,mLaneNum):
		self.Lanes.append(mLaneNum)
	def AddSlot(self,mSlotNum):
		self.Slots.append(mSlotNum)
	def GetLaneNums(self):
		return self.Lanes
	def GetSlotNums(self):
		return self.Slots
	def TimeOut(self,mTime):
		if mTime-self.Start>self.MaxTime:
			return True
		return False
	def LanesAvailable(self):
		if len(self.Lanes)>0:
			return True
		else:
			return False
	def LanesAssigned(self,mLaneNum):
		if len(self.Lanes)>0:
			for x in self.Lanes:
				if x==mLaneNum:
					return True
		
		return False
	def SetTime(self,mType,mTime):
		if mType==0:
			self.Start=mTime
			print("Turn start time ",self.Start)
		else:
			if self.End<mTime:
				self.End=mTime
			print("Turn End time ",self.End)
	def IncTime(self,mTime,mTime2):
		self.Start+=mTime
		self.End=mTime2
	def GetTime(self,mType):
		if mType==0:
			return self.Start
		else:
			return self.End
	def AssessCloseness(self,mLanes,mTime,mThreshold1,mThreshold2,mTimeAtInter,mImpact):
		print("Assessing closeness")
		if len(self.Lanes)>0:
			count=0
			for x in self.Lanes:
				print("x ",x)
				print("slot ",self.Slots[count])
				if mLanes[x].AssessTheClosenessOfFirstCar(self.Slots[count],mTime,mThreshold1,mThreshold2,mTimeAtInter,mImpact)==True:
					return True
				count+=1
		return False

