from datetime import datetime

class Slot:
	def __init__(self,mID,mLaneNum,mMaxVehicles,mTurn,mMaxTime,mCurrentTime):
		self.ID=mID
		self.LaneNum=mLaneNum
		self.Vehicles=list()
		self.MaxVehicles=mMaxVehicles
		self.Turn=mTurn
		self.MaxTime=mMaxTime
		self.FirstCarEntered=mCurrentTime
		self.LastCarEnterTime=0
	def AddVehicle(self,mVehicle):
		self.Vehicles.append(mVehicle)
		print("Vehicle ",mVehicle.GetVehicleID()," was added into Slot " ,self.ID," on Lane ",self.LaneNum)
		self.LastCarEnterTime=mVehicle.GetTimeToEnter()
		print("time entered the intersection ",self.LastCarEnterTime)
		print("time exited the intersection  ",mVehicle.GetTimeToExit())
		return mVehicle.GetTimeToExit()
	def GetLastCarEnterTime(self):
		return self.LastCarEnterTime
	def FirstCarPosition(self,mTime):
		#print("assessing closeness - posn")
		if len(self.Vehicles) >0:
			print("assessing closeness - posn",self.Vehicles[0].CurrentPosition(mTime))
			return self.Vehicles[0].CurrentPosition(mTime)
		else:
			return -1
	def FirstCarCrossingTime(self):
		if len(self.Vehicles) >0:
			print("assessing closeness - crossing time",self.Vehicles[0].GetTimeToEnter())
			return self.Vehicles[0].GetTimeToEnter()
		else:
			return -1
	def GetLastCarPosition(self,mTime):
		if len(self.Vehicles) >0:
			return self.Vehicles[len(self.Vehicles)-1].CurrentPosition(mTime)
		else:
			return -1
	def GetLastCarSpeed(self):
		if len(self.Vehicles) >0:
			return self.Vehicles[len(self.Vehicles)-1].GetSpeed()
		else:
			return -1
	def GetID(self):
		return self.ID
	#def TimeLimitReached(self,mTime):
		#return False
	def IsFull(self):
		if len(self.Vehicles) == self.MaxVehicles:
			print("slot full")
			return True
		return False
	def TimeOut(self,mTime):
		print("time now ",mTime," first car ",self.FirstCarEntered)
		if mTime-self.FirstCarEntered>self.MaxTime:
			print("Slot time out")
			return True
		return False
	def IsEmpty(self):
		if len(self.Vehicles) == 0:
			return True
		return False
	def GetTheFistVehicle(self):
		if len(self.Vehicles) > 0:
			return self.Vehicles.pop(0)
		return None
	def CompareIDs(self,mID):
		if(self.ID==mID):
			return True
		else:
			return False
	def DelayVehicles(self,mDelay,mTime,mTLimit,mTimeGapBetnCars):
		print("delaying inside the slot")
		for Vehicle in self.Vehicles:
			TimeToExit=Vehicle.Delay(mDelay,mTime,mTLimit)
			if TimeToExit>=0 and Vehicle.GetTimeToEnter()>self.LastCarEnterTime:
				self.LastCarEnterTime=Vehicle.GetTimeToEnter()
				print ("Last Car Enter Time",self.LastCarEnterTime)
			if TimeToExit>=0:
				mTLimit=TimeToExit+mTimeGapBetnCars
		return mTLimit-mTimeGapBetnCars
	def CalcDelayImpact(self,mDelay,mTime,mTLimit,mTimeGapBetnCars):
		TotalImpact=0
		print("calc delay impact - slots")
		for Vehicle in self.Vehicles:
			Impact,TimeToExit=Vehicle.AssessDelay(mDelay,mTime,mTLimit)
			if Impact>0:
				TotalImpact+=Impact	
			if TimeToExit>=0:
				mTLimit=TimeToExit+mTimeGapBetnCars
		if(len(self.Vehicles)>0):
			return TotalImpact/len(self.Vehicles)
		return -1
	#def SetTimeToEnter(self
