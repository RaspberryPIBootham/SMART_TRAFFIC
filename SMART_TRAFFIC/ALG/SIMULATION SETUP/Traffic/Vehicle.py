import time

class Vehicle:
	def __init__(self,mID,mTimeEntered,mMaxSpeed,mLDist,mTimeLimit,mIDist,mPrevPos,mPrevSpeed,mMinGap):
		self.VID=mID
		self.TimeEnteredZone=mTimeEntered
		self.MaxSpeed=mMaxSpeed
		self.LDist=mLDist
		self.IDist=mIDist
		self.TimeLimit=mTimeLimit
		self.PosnAtLastCalc=0
		self.TimeAtLastCalc=mTimeEntered
		self.SpeedAlreadyControlled=False
		self.PlotIt=1
		if mMaxSpeed==0 or mLDist/mMaxSpeed<0:
			self.TimeToExit=0
			self.TimeToEnter=0
			self.Speed=0
		else:
			self.TimeToEnter=(mLDist/mMaxSpeed)+mTimeEntered
			if mTimeLimit>0 and self.TimeToEnter<mTimeLimit:
				self.TimeToEnter=mTimeLimit
				self.Speed=mLDist/(mTimeLimit-mTimeEntered)
			else:
				self.Speed=mMaxSpeed
			print("Speed (m/s) ",self.Speed)
			self.TimeToExit=((mLDist+mIDist)/self.Speed)+mTimeEntered
			if self.Speed-mPrevSpeed>0 and mPrevPos-((self.Speed-mPrevSpeed)*(self.TimeToEnter-mTimeEntered))<mMinGap:
				self.Speed=(mLDist-mMinGap)/(self.TimeToEnter-mTimeEntered)
				self.TimeToEnter=(mLDist/self.Speed)+mTimeEntered
				self.TimeToExit=((mLDist+mIDist)/self.Speed)+mTimeEntered
			elif self.Speed-mPrevSpeed<=0 and mPrevPos>0 and mPrevPos<mMinGap:
				#self.Speed=(mLDist-mMinGap)/(self.TimeToEnter-mTimeEntered)
				self.Speed=self.Speed*(mPrevPos/mMinGap)
				self.TimeToEnter=(mLDist/self.Speed)+mTimeEntered
				self.TimeToExit=((mLDist+mIDist)/self.Speed)+mTimeEntered	
	def GetIteration(self):
		return self.PlotIt
	def IncrementIteration(self):
		self.PlotIt+=1			
	def GetTimeToEnter(self):
		return self.TimeToEnter
	def GetTimeToExit(self):
		return self.TimeToExit
	def SetSpeed(self,mSpeed,mAccel):
		self.Speed=mSpeed
		self.Accl=mAccel
	def ReSetSpeed(self,mSpeed,mAccel,mTime):
		self.PosnAtLastCalc=self.CurrentPosition(mTime)
		self.TimeAtLastCalc=mTime
		if self.SpeedAlreadyControlled==True and self.Speed>2:
			self.Speed-=2
			#print("speed reduced")
		else:
			self.Speed=mSpeed
		self.Accl=mAccel
		self.SpeedAlreadyControlled=True
	def ReCalcSpeed(self):
		self.Speed=0
	def GetSpeed(self):
		return self.Speed
	def GetVehicleID(self):
		return self.VID
	def CurrentPosition(self):
		return self.Speed*(time.perf_counter()-self.TimeAtLastCalc)+self.PosnAtLastCalc
	def CurrentPosition(self,mTime):
		#print ("Speed  ",self.Speed)
		#print ("Time  ",mTime)
		#print ("TimeAtLastCalc  ",self.TimeAtLastCalc)
		#print ("PosnAtLastCalc  ",self.PosnAtLastCalc)
		return self.Speed*(mTime-self.TimeAtLastCalc)+self.PosnAtLastCalc
	def EnteringInt(mLDist):
		check=0
		while mLDist >	CurrentPosition():
			check+=1
		return True
	def Delay(self,mDelay,mTime,mTLimit):
		
		RemainingDist=self.LDist-self.CurrentPosition(mTime)
		RemainingTotalDist=self.LDist+self.IDist-self.CurrentPosition(mTime)
		self.PosnAtLastCalc=self.CurrentPosition(mTime)
		self.TimeLimit=mTLimit#####
		print("Vehicle ID ",self.VID)
		print("Prev Speed (m/s) ",self.Speed)
		print("Remaining Dist ",RemainingDist)
		self.TimeAtLastCalc=mTime
		if RemainingDist>0 and self.Speed>0:
			self.TimeToEnter=(RemainingDist/self.MaxSpeed)+mTime
			print("time to enter ",self.TimeToEnter)
			if self.TimeLimit>0 and self.TimeToEnter<mTLimit:
				self.TimeToEnter=mTLimit
				self.Speed=RemainingDist/(mTLimit-mTime)
			else:
				self.Speed=self.MaxSpeed
			self.TimeToExit=(RemainingTotalDist/self.Speed)+mTime

			print("New Speed (m/s) ",self.Speed)
			print("Time To Enter ",self.TimeToEnter)
			print("Time To Exit ",self.TimeToExit)
			return self.TimeToEnter#was self.TimeToExit
		return -1
	def AssessDelay(self,mDelay,mTime,mTLimit):
		print("assess delay - vehicles")
		tRemainingDist=self.LDist-self.CurrentPosition(mTime)
		tRemainingTotalDist=self.LDist+self.IDist-self.CurrentPosition(mTime)
		#self.PosnAtLastCalc=self.CurrentPosition(mTime)
		tTimeLimit=mTLimit#####
		print("Vehicle ID ",self.VID)
		print("Prev Speed (m/s) ",self.Speed)
		print("Remaining Dist ",tRemainingDist)
		#self.TimeAtLastCalc=mTime
		if tRemainingDist>0 and self.Speed>0:
			tTimeToEnter=(tRemainingDist/self.MaxSpeed)+mTime
			print("vehicle time to enter ",self.TimeToEnter,"TLimit ",mTLimit)
			if tTimeLimit>0 and tTimeToEnter<mTLimit:
				tTimeToEnter=mTLimit
				tSpeed=tRemainingDist/(mTLimit-mTime)
			else:
				tSpeed=self.MaxSpeed
			tTimeToExit=(tRemainingTotalDist/tSpeed)+mTime

			print("New Speed (m/s) ",tSpeed)
			print("Time To Enter ",tTimeToEnter)
			print("Time To Exit ",tTimeToExit)
			if self.Speed>0:
				return tSpeed/self.Speed,tTimeToEnter
			else:
				return -1,tTimeToEnter
		return -1,-1

