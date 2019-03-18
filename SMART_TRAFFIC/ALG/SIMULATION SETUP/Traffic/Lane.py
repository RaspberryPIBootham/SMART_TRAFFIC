from Traffic.Vehicle import Vehicle
from Traffic.Slot import Slot

class Lane:
	def __init__(self,mLaneNum,mMaxVehicles,mMaxTime,mMaxSpeed,mLDist,mIDist):
		self.Slots=list()
		self.LaneNum=mLaneNum
		self.mMaxVehiclesPerSlot=mMaxVehicles
		self.NumSlotsCreated=0
		self.LastAsignedTurn=-1
		self.MaxTimeForSlot=mMaxTime
		self.MaxSpeeed=mMaxSpeed
		self.LengthControlZone=mLDist
		self.LengthInterSection=mIDist
		self.TimeLastCarEnteringIntersection=0
	def SetPosnInLaneOrder(self,mNum):
		self.LaneOrderPos=mNum
	def GetPosnInLaneOrder(self):
		return self.LaneOrderPos
	def AddSlot(self,mSlot):
		self.NumSlotsCreated+=1
		self.Slots.append(mSlot)
	def IsEmpty(self):
		if len(self.Slots) == 0:
			return True
		return False
	def GetTheFistSlot(self):
		if len(self.Slots) > 0:
			return self.Slots.pop(0)
		return None
	def SetLastTurn(self,TNum):
		self.LastTurnNum=TNum
	def GetLastTurn(self):
		return self.LastTurnNum
	def NewSlotNeeded(self,mLaneNum,mTime):
		if len(self.Slots)==0 or self.Slots[len(self.Slots)-1].IsFull() or self.Slots[len(self.Slots)-1].TimeOut(mTime):##
			print("new slot needed")
			return True
		else:
			return False
	def GetExpectedTimeAtInter(self,NumVehicles,mLaneNum,mTime,mLaneOrder,mTurn,mNewTurn,mTimeLimit,mMinGap):
		if len(self.Slots)>0:		
			mVh=Vehicle(NumVehicles,mTime,self.MaxSpeeed,self.LengthControlZone,mTimeLimit,self.LengthInterSection,self.Slots[len(self.Slots)-1].GetLastCarPosition(mTime),self.Slots[len(self.Slots)-1].GetLastCarSpeed(),mMinGap)
		else:		
			mVh=Vehicle(NumVehicles,mTime,self.MaxSpeeed,self.LengthControlZone,mTimeLimit,self.LengthInterSection,-1,-1,mMinGap)
		################return mVh.GetTimeToEnter()
		return mVh.GetTimeToExit()

	def AddVehicle(self,NumVehicles,mLaneNum,mTime,mLaneOrder,mTurn,mNewTurn,mTimeLimit,mMinGap):#

		if len(self.Slots)>0:		
			self.mVh=Vehicle(NumVehicles,mTime,self.MaxSpeeed,self.LengthControlZone,mTimeLimit,self.LengthInterSection,self.Slots[len(self.Slots)-1].GetLastCarPosition(mTime),self.Slots[len(self.Slots)-1].GetLastCarSpeed(),mMinGap)
		else:		
			self.mVh=Vehicle(NumVehicles,mTime,self.MaxSpeeed,self.LengthControlZone,mTimeLimit,self.LengthInterSection,-1,-1,mMinGap)
		#NewTurn=False
		#if self.LastAsignedTurn==-1:##add time constraint
			#NewTurn=False###
		#elif len(self.Slots)==0 or self.Slots[len(self.Slots)-1].IsFull():
			#self.LastAsignedTurn+=len(mLaneOrder)#what will happen if the lane has been empty for a while...need to look at the other lanes with the same posn in the laneorder list - given that ==-1 situation may be able to resolve in a similar manner
		TimeAtInter=-1
		self.LastAsignedTurn=mTurn
		if mNewTurn==True or len(self.Slots)==0 or self.Slots[len(self.Slots)-1].IsFull() or self.Slots[len(self.Slots)-1].TimeOut(mTime):
			self.mSL=Slot(self.NumSlotsCreated,self.LaneNum,self.mMaxVehiclesPerSlot,self.LastAsignedTurn,self.MaxTimeForSlot,mTime)
			TimeAtInter=self.mSL.AddVehicle(self.mVh)#self.MaxSpeeed,self.LengthControlZone,mTimeLimit###mTime+
			self.TimeLastCarEnteringIntersection=self.mSL.GetLastCarEnterTime()##mTime+
			self.Slots.append(self.mSL)
			self.NumSlotsCreated+=1
		else:
			TimeAtInter=self.Slots[len(self.Slots)-1].AddVehicle(self.mVh)#,self.MaxSpeeed,self.LengthControlZone,mTimeLimit###mTime+
			self.TimeLastCarEnteringIntersection=self.Slots[len(self.Slots)-1].GetLastCarEnterTime()###mTime+
		return TimeAtInter
	def GetTheLastSlotID(self):
		if len(self.Slots)>0:
			return self.Slots[len(self.Slots)-1].GetID()
		else:
			return -1
	def GetTimeLastCarEnteringIntersection(self):
		if len(self.Slots)>0:
			return self.Slots[len(self.Slots)-1].GetLastCarEnterTime()
		else:
			return 0
	def ServeTheFirstVehicle(self):
		if len(self.Slots) > 0 and not self.Slots[0].IsEmpty():
			return self.Slots[0].GetTheFirstVehicle()
		return None
	def ServiceTheLane(self,mLDist):
		while len(self.Slots) > 0 and not self.Slots[0].IsEmpty():
			self.Slots[0].GetTheFirstVehicle().EnteringInt(mLDist)
			print ("Vehicle enetering the inter-section")
		if len(self.Slots) > 0:
			self.Slots.pop(0)	
	def AdjustSpeeds(self,mSlotID,mDelay,mTime,mTLimit,mTimeGapBetnCars):
		Found=False
		sIndex=0
		SlotEndTime=0
		while Found==False and sIndex<len(self.Slots):
			if self.Slots[sIndex].CompareIDs(mSlotID)==True:
				Found=True
				SlotEndTime=self.Slots[sIndex].DelayVehicles(mDelay,mTime,mTLimit,mTimeGapBetnCars)
			sIndex+=1
		return SlotEndTime
	
	def MeasureDelayImpact(self,mSlotID,mDelay,mTime,mTLimit,mTimeGapBetnCars):
		print("measure delay impact - lanes")
		Found=False
		sIndex=0
		Impact=0
		while Found==False and sIndex<len(self.Slots):
			if self.Slots[sIndex].CompareIDs(mSlotID)==True:
				Found=True
				Impact=self.Slots[sIndex].CalcDelayImpact(mDelay,mTime,mTLimit,mTimeGapBetnCars)
			sIndex+=1
		return Impact

	def AssessTheClosenessOfFirstCar(self,mSlotNum,mTime,mThreshold1,mThreshold2,mTimeAtInter,mImpact):
		#print("assessing closeness - slot num",mSlotNum)
		print("Impact  ",mImpact)
		if len(self.Slots)>0 and self.Slots[mSlotNum].FirstCarCrossingTime()<mTimeAtInter:
			print("ret true 0")
			return True
		elif mImpact<0.6:
			print("ret true 0.1")
			return True
		elif len(self.Slots)>0 and self.Slots[mSlotNum].FirstCarCrossingTime()<mTime:
			print("ret true 1")
			return True
		elif len(self.Slots)>0 and self.Slots[mSlotNum].FirstCarPosition(mTime)>0 and self.Slots[mSlotNum].FirstCarPosition(mTime)>mThreshold2:
			print("ret true 2")
			return True
		elif len(self.Slots)>0 and self.Slots[mSlotNum].FirstCarCrossingTime()-mTime<mThreshold1:
			print("ret true 3")
			return True
		print("ret false")
		return False
