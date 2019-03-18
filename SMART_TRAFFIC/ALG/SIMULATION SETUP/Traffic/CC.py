from Traffic.Lane import Lane
from Traffic.TurnData import TurnData
import threading
from datetime import datetime
from graphics import *
import time
import random

class CC:
	def __init__(self):
		self.NumVehicles=0
		self.Lanes=dict()
		
		self.Turns=dict()#where is the assignment?
		self.ActiveLanesIndex=0
		self.ActiveTurnIndex=0
		self.LastAssignedTurnIndex=0
		self.NumTurnIndicesDeleted=0
		self.Start=datetime.now()
		self.TimeGapBetnTurns=1.0#time gap between two turns
		self.TimeGapBetnCars=2.0#time gap between two cars
		self.MaxTimeForATurn=6.0#maximum time length for a turn
		#self.Threshold2=
		self.Threshold1=2#maximum time before crossing to trigger a new turn
		self.Is_FCFS_ON=False
	def SetUpLanes(self,NumLanes,mLaneOrder):
		for mL in range(NumLanes):
			self.Lanes[mL]=Lane(mL,4,7,100,1900,300)#mLaneNum,mMaxVehicles,mMaxTimem,mMaxSpeed,mLDist,mIDist---- may need adjusting
		self.LaneOrder=mLaneOrder
		for x in range(len(mLaneOrder)):
			for y in range(len(mLaneOrder[x])):
				self.Lanes[mLaneOrder[x][y]].SetPosnInLaneOrder(x)

	def GetTurnEndTime(self,mPrevIndex):
		while(mPrevIndex >= 0):
			if self.Turns[mPrevIndex].LanesAvailable() == True:
				return self.Turns[mPrevIndex].GetTime(1)
			else:
				mPrevIndex-=1
		return -1

	def DelayVehicles(self,mPos,mDelay,mTime,mTLimit):
		LaneNums=self.Turns[mPos].GetLaneNums()
		SlotIDs=self.Turns[mPos].GetSlotNums()
		LatestEndTime=0
		print("Delay")
		#print(len(LaneNums))
		#print(len(SlotIDs))
		ind=0
		for ln in LaneNums:
			sl=SlotIDs[ind]
			ind+=1
			print("sl ",sl,"ln ",ln,"mDelay ",mDelay)
			SlotEndTime=self.Lanes[ln].AdjustSpeeds(sl,mDelay,mTime,mTLimit,self.TimeGapBetnCars)#,mTime
			if SlotEndTime>LatestEndTime:
				LatestEndTime=SlotEndTime
		return LatestEndTime
	def AssessDelayImpact(self,mPos,mDelay,mTime,mTLimit):
		print("delay impact delay = ",mDelay," mTLimit=  ",mTLimit)
		
		LaneNums=self.Turns[mPos].GetLaneNums()
		SlotIDs=self.Turns[mPos].GetSlotNums()
		HighestImpact=0
		ind=0
		for ln in LaneNums:
			sl=SlotIDs[ind]
			ind+=1
			print("delay impact step 2")
			Impact=self.Lanes[ln].MeasureDelayImpact(sl,mDelay,mTime,mTLimit,self.TimeGapBetnCars)
			if Impact>HighestImpact:
				HighestImpact=Impact
		return HighestImpact

	def AddTurns(self,mPos):
		temp=self.LastAssignedTurnIndex+1
		for i in range(temp,mPos+1):#fill the turns data queue
			#print (i)
			self.Turns[i]=TurnData(self.MaxTimeForATurn)
			self.LastAssignedTurnIndex+=1


	def AssessDelayTime(self,mCase,mLaneNum,mTime,mLaneOrder,mPos,mMinGap,mDistC,mMaxSpeed):
		
		TimeAtInter=-1
		if mCase==3:
			print("assess mCase3")
			if mPos>0:
				EndT=self.GetTurnEndTime(mPos-1)
				if EndT>0:
					TimeAtInter=self.Lanes[mLaneNum].GetExpectedTimeAtInter(self.NumVehicles,mLaneNum,mTime,mLaneOrder,mPos,True,EndT+self.TimeGapBetnTurns,mMinGap)
				else:
					TimeAtInter=self.Lanes[mLaneNum].GetExpectedTimeAtInter(self.NumVehicles,mLaneNum,mTime,mLaneOrder,mPos,True,mTime+(mDistC/mMaxSpeed),mMinGap)
					
			else:
				EndT=0
				TimeAtInter=self.Lanes[mLaneNum].GetExpectedTimeAtInter(self.NumVehicles,mLaneNum,mTime,mLaneOrder,mPos,True,mTime+(mDistC/mMaxSpeed),mMinGap)
			print("chk pt 1 ",TimeAtInter,"mPos ",mPos)
			DTLimit=TimeAtInter+self.TimeGapBetnTurns
			print("DTLimit  ",DTLimit)
			if self.Turns[mPos+1].LanesAvailable()==True:
				if EndT>0:
					HI=self.AssessDelayImpact(mPos+1,TimeAtInter-EndT,mTime,DTLimit)
				else:
					HI=self.AssessDelayImpact(mPos+1,TimeAtInter,mTime,TimeAtInter)###############??TimeAtInter
			return self.Turns[mPos+1].AssessCloseness(self.Lanes,mTime,self.Threshold1,self.Threshold2,TimeAtInter,HI)

		elif mCase==4:
			print("assess mCase4")
			TimeAtInter=self.Lanes[mLaneNum].GetExpectedTimeAtInter(self.NumVehicles,mLaneNum,mTime,mLaneOrder,mPos,True,self.Turns[mPos].GetTime(0),mMinGap)
			print("chk pt 0 ",TimeAtInter)
			PrevTime=self.Turns[mPos].GetTime(1)
			print("Prev ",PrevTime)
			DTLimit=TimeAtInter+self.TimeGapBetnTurns
			print("chk pt 0.1 ",mPos,"  ",self.LastAssignedTurnIndex)
			HI=1.0
			if TimeAtInter>PrevTime:
				print("chk pt 0.15 ")
				if self.Turns[mPos+1].LanesAvailable()==True:
					print("chk pt 0.2 ")
					HI=self.AssessDelayImpact(mPos+1,TimeAtInter-PrevTime,mTime,DTLimit)
				
			print("chk pt 1 ",TimeAtInter,"  ",HI)
			return self.Turns[mPos+1].AssessCloseness(self.Lanes,mTime,self.Threshold1,self.Threshold2,TimeAtInter,HI)
		
	def IncrementTheTurns(self,mLaneOrder):
		temp=len(mLaneOrder)-(self.LastAssignedTurnIndex%len(mLaneOrder))
		#print("inc the TURNS ",self.LastAssignedTurnIndex," ",temp)
		for i in range(0,temp):#fill the turns data queue
			self.LastAssignedTurnIndex+=1
			#print("INDEX ",self.LastAssignedTurnIndex)				
			self.Turns[self.LastAssignedTurnIndex]=TurnData(self.MaxTimeForATurn)

	def AddNewVehicle(self,mLaneNum,mTime,mLaneOrder,mDistC,mDistI,mMaxSpeed,mMinGap):
		print("** New vehicle detected on Lane Number", mLaneNum)
		self.Threshold2=mDistC*0.75
		#can this logic work if Turns data queue is being cleared
		if mLaneNum in self.Lanes and self.Lanes[mLaneNum]:
			###check whether a new turn needed?
			###if yes then what is the turn index(pos)?
			pos=len(mLaneOrder)*(self.LastAssignedTurnIndex//len(mLaneOrder))+self.Lanes[mLaneNum].GetPosnInLaneOrder()
			#print (pos)
			#print (self.LastAssignedTurnIndex%len(mLaneOrder))
			#print (self.Lanes[mLaneNum].GetPosnInLaneOrder())
			if len(self.Turns)==0:
				self.Turns[0]=TurnData(self.MaxTimeForATurn)
			####check the indexing here ##########
			print("mTime ",mTime)
			if self.LastAssignedTurnIndex%len(mLaneOrder)<self.Lanes[mLaneNum].GetPosnInLaneOrder():#add items to the Turns --how about the empty turns
				print("p2")
				temp=self.LastAssignedTurnIndex%len(mLaneOrder)
				for i in range(temp,self.Lanes[mLaneNum].GetPosnInLaneOrder()):#fill the turns data queue
					self.LastAssignedTurnIndex+=1
					print("INDEX ",self.LastAssignedTurnIndex)				
					self.Turns[self.LastAssignedTurnIndex]=TurnData(self.MaxTimeForATurn)
					
				self.Turns[self.LastAssignedTurnIndex].AddLane(mLaneNum)#self.LastAssignedTurnIndex//len(mLaneOrder)+self.Lanes[mLaneNum].GetPosnInLaneOrder()	
				
				if self.LastAssignedTurnIndex>0:
					EndT=self.GetTurnEndTime(self.LastAssignedTurnIndex-1)
					if EndT>0:
						self.Turns[self.LastAssignedTurnIndex].SetTime(0,EndT+self.TimeGapBetnTurns)
						TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,True,EndT+self.TimeGapBetnTurns,mMinGap)
						self.Turns[self.LastAssignedTurnIndex].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())
					else:
						self.Turns[self.LastAssignedTurnIndex].SetTime(0,mTime+(mDistC/mMaxSpeed))
						TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,True,mTime+(mDistC/mMaxSpeed),mMinGap)
						self.Turns[self.LastAssignedTurnIndex].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())
					self.Turns[self.LastAssignedTurnIndex].SetTime(1,TimeAtInter)	
			elif (pos>=self.LastAssignedTurnIndex or (pos+1<=self.LastAssignedTurnIndex and self.Turns[pos+1].LanesAvailable() == True and self.AssessDelayTime(3,mLaneNum,mTime,mLaneOrder,pos,mMinGap,mDistC,mMaxSpeed)==False)) and self.Turns[pos].LanesAvailable() == False:#no added lanes 
				print("p3")
				self.Turns[pos].AddLane(mLaneNum)#
				if pos>0:
					print("p3.1")
					EndT=self.GetTurnEndTime(pos-1)
					if EndT>0:
						self.Turns[pos].SetTime(0,EndT+self.TimeGapBetnTurns)#lastassigned-1 can this be always right???
						TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,True,EndT+self.TimeGapBetnTurns,mMinGap)
						self.Turns[pos].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())
					else:
						self.Turns[pos].SetTime(0,mTime+(mDistC/mMaxSpeed))
						TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,True,mTime+(mDistC/mMaxSpeed),mMinGap)
						self.Turns[pos].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())
				else:
					print("p3.2")
					print("mDistC ",mDistC)
					print("mMaxSpeed  ",mMaxSpeed)
					EndT=0	
					self.Turns[pos].SetTime(0,mTime+(mDistC/mMaxSpeed))#######re think - is this always possible???
					TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,True,mTime+(mDistC/mMaxSpeed),mMinGap)
					self.Turns[pos].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())
				 
				self.Turns[pos].SetTime(1,TimeAtInter)
				DTLimit=TimeAtInter+self.TimeGapBetnTurns
				print("set delay ",self.LastAssignedTurnIndex,"pos ",pos)
				for pos1 in range(pos+1,self.LastAssignedTurnIndex+1):
					if self.Turns[pos1].LanesAvailable()==True:
						print("delay XXXX")
						if EndT>0:
							print("delay")
							print("time at inter ",TimeAtInter,"EndT ",EndT)
							DTLimit=self.DelayVehicles(pos1,TimeAtInter-EndT,mTime,DTLimit)#######
							self.Turns[pos1].IncTime(TimeAtInter-EndT,DTLimit)#######
						else:
							print("delay")
							print("time at inter",TimeAtInter)
							DTLimit=self.DelayVehicles(pos1,TimeAtInter,mTime,TimeAtInter)########
							self.Turns[pos1].IncTime(TimeAtInter,DTLimit)####
						DTLimit+=self.TimeGapBetnTurns								

			elif (pos>=self.LastAssignedTurnIndex or (pos+1<=self.LastAssignedTurnIndex and self.Turns[pos+1].LanesAvailable() == True and self.AssessDelayTime(4,mLaneNum,mTime,mLaneOrder,pos,mMinGap,mDistC,mMaxSpeed)==False)) and self.Turns[pos].TimeOut(mTime)==False and self.Turns[pos].LanesAssigned(mLaneNum) == False:#there are added lanes, but not this one
				print("p4")
				self.Turns[pos].AddLane(mLaneNum)#
				print("start time limit ",self.Turns[pos].GetTime(0))
				TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,True,self.Turns[pos].GetTime(0),mMinGap)
				self.Turns[pos].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())
				PrevTime=self.Turns[pos].GetTime(1)
				self.Turns[pos].SetTime(1,TimeAtInter)
				DTLimit=TimeAtInter+self.TimeGapBetnTurns
				if TimeAtInter>PrevTime:
					for pos1 in range(pos+1,self.LastAssignedTurnIndex+1):
						if self.Turns[pos1].LanesAvailable()==True:
							DTLimit=self.DelayVehicles(pos1,TimeAtInter-PrevTime,mTime,DTLimit)########
							self.Turns[pos1].IncTime(TimeAtInter-PrevTime,DTLimit)##########
							DTLimit+=self.TimeGapBetnTurns	
						
			elif (pos+1<=self.LastAssignedTurnIndex and self.Turns[pos+1].LanesAvailable() == True and (self.AssessDelayTime(3,mLaneNum,mTime,mLaneOrder,pos,mMinGap,mDistC,mMaxSpeed)==True or self.AssessDelayTime(4,mLaneNum,mTime,mLaneOrder,pos,mMinGap,mDistC,mMaxSpeed)==True)) or self.Turns[pos].TimeOut(mTime)==True or self.Lanes[mLaneNum].NewSlotNeeded(mLaneNum,mTime):#need to allocate a new turn for this slot
				print("p5")
				pos+=len(mLaneOrder)
				#print(pos)
				self.AddTurns(pos)
				self.Turns[pos].AddLane(mLaneNum)
				if pos>0:
					EndT=self.GetTurnEndTime(pos-1)
					if EndT>0:
						self.Turns[pos].SetTime(0,EndT+self.TimeGapBetnTurns)
						TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,True,EndT+self.TimeGapBetnTurns,mMinGap)
						self.Turns[pos].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())
						self.Turns[pos].SetTime(1,TimeAtInter)

			else:
				print("p6")
				print("last car entering ",self.Lanes[mLaneNum].GetTimeLastCarEnteringIntersection())
				TimeAtInter=self.Lanes[mLaneNum].AddVehicle(self.NumVehicles,mLaneNum,mTime,mLaneOrder,pos,False,self.Lanes[mLaneNum].GetTimeLastCarEnteringIntersection()+self.TimeGapBetnCars,mMinGap)#How can I get the enter time for the car in front???lane should keep the latest time given to enter....
				self.Turns[pos].AddSlot(self.Lanes[mLaneNum].GetTheLastSlotID())				
				PrevTime=self.Turns[pos].GetTime(1)
				if PrevTime < 	TimeAtInter:			
					self.Turns[pos].SetTime(1,TimeAtInter)
					DTLimit=TimeAtInter+self.TimeGapBetnTurns
					for pos1 in range(pos+1,self.LastAssignedTurnIndex+1):
						if self.Turns[pos1].LanesAvailable()==True:
							DTLimit=self.DelayVehicles(pos1,TimeAtInter-PrevTime,mTime,DTLimit)##########
							self.Turns[pos1].IncTime(TimeAtInter-PrevTime,DTLimit) #########			
							DTLimit+=self.TimeGapBetnTurns
			
			##Turns[pos].SetTimeToEnter(self.Lanes[mLaneNum].GetTimeToEnter())######################
			self.NumVehicles+=1
			if self.Is_FCFS_ON==True:
				self.IncrementTheTurns(mLaneOrder)
			#######if NewTurn:
				##########NextTurn()
	def NextActiveLane(self):
		self.ActiveTurnIndex+=1
		if self.ActiveLanesIndex<len(self.LaneOrder)-1:
			self.ActiveLanesIndex+=1
		else:
			self.ActiveLanesIndex=0
		
		return self.ActiveLanesIndex
	def NextTurn(self):
		self.LastAssignedTurnIndex+=1
		return self.LastAssignedTurnIndex
	def CurrentActiveLane(self):
		return self.ActiveLanesIndex
	def ServeLanes(self,mLDist):
		if len(self.LaneOrder) > 0 and len(self.Lanes) > 0:
			Index=0			
			for j in range(mLaneOrder[Index]):
				self.Lanes[j].ServiceTheLane(mLDist)			
			Index=NextActiveLane()

	def PlotPositions(self,X0,Y0,X1,Y1,X2,Y2,X3,Y3,mDistC,mDistI,mGap):
		WIDTH, HEIGHT = 800, 800
		
		
		#r1= Rectangle(Point(0, 2200), Point(1900, 1900))
		#r1.draw(win)
		#r1.setFill('black')
		
		win = GraphWin('BOOTHAM SMART TRAFFIC CONTROLLER - AI', WIDTH, HEIGHT)
		win.setCoords(0, 0, 4100, 4100)
		win.setBackground("white")
		it=0
		s = Rectangle(Point(1900, 1900), Point(2200, 2200))
						
		s.draw(win)
		s.setFill('yellow')
		l1 = Line(Point(0,1900), Point(1900,1900))
		l1.setWidth(3)
		l1.draw(win)
		l1.setFill('red')

		l2 = Line(Point(1900,0), Point(1900,1900))
		l2.setWidth(3)
		l2.draw(win)
		l2.setFill('red')

		l3 = Line(Point(0,2200), Point(1900,2200))
		l3.setWidth(3)
		l3.draw(win)
		l3.setFill('red')

		l4 = Line(Point(1900,2200), Point(1900,4100))
		l4.setWidth(3)
		l4.draw(win)
		l4.setFill('red')

		l5 = Line(Point(2200,0), Point(2200,1900))
		l5.setWidth(3)
		l5.draw(win)
		l5.setFill('red')

		l6 = Line(Point(2200,1900), Point(4100,1900))
		l6.setWidth(3)
		l6.draw(win)
		l6.setFill('red')

		l7 = Line(Point(2200,2200), Point(4100,2200))
		l7.setWidth(3)
		l7.draw(win)
		l7.setFill('red')

		l8 = Line(Point(2200,2200), Point(2200,4100))
		l8.setWidth(3)
		l8.draw(win)
		l8.setFill('red')
		prev_time=time.perf_counter()
		delay_add_vehicle=0
		LaneOrder=[[0,1],[2,3]]
		NumLanes=4
		self.SetUpLanes(NumLanes,LaneOrder)
		while True:
			it+=1
			mTime=time.perf_counter()
			
			if it==1 or mTime-prev_time>=delay_add_vehicle:
				self.AddNewVehicle(random.randint(0,NumLanes-1),mTime,LaneOrder,1900,300,100,100)
				#print("vehicle added")				
				delay_add_vehicle=random.randint(1,8)
				prev_time=mTime
				#print("moving to plot")
				
			for mLaneNum in range(len(self.Lanes)):
				#print("Lane Num ",mLaneNum)
				for mSlot in self.Lanes[mLaneNum].Slots:
					prev_posn=0
					#print("Slot ID ",mSlot.GetID())
					for mVehicle in mSlot.Vehicles:
						#if mVehicle.CurrentPosition(mTime)<1900:
						#print("Vehicle ID ",mVehicle.GetVehicleID())
						#print("Posn ",mVehicle.CurrentPosition(mTime))
						if mLaneNum==0:

							xposn=X0+mVehicle.CurrentPosition(mTime)
							yposn=Y0
							if mVehicle.GetIteration()==1:
								mVehicle.s = Rectangle(Point(xposn, yposn), Point(xposn+100, yposn+50))
								mVehicle.s.draw(win)
								mVehicle.s.setFill('blue')
								mVehicle.IncrementIteration()
							else:
								mVehicle.s.move(xposn-mVehicle.xposn,yposn-mVehicle.yposn)
							mVehicle.xposn=xposn
							mVehicle.yposn=yposn
							
						elif mLaneNum==1:
							xposn=X1-mVehicle.CurrentPosition(mTime)
							yposn=Y1
							if mVehicle.GetIteration()==1:
								mVehicle.s = Rectangle(Point(xposn, yposn), Point(xposn+100, yposn+50))
								mVehicle.s.draw(win)
								mVehicle.s.setFill('blue')
								mVehicle.IncrementIteration()
							else:
								mVehicle.s.move(xposn-mVehicle.xposn,yposn-mVehicle.yposn)
							mVehicle.xposn=xposn
							mVehicle.yposn=yposn
						elif mLaneNum==2:
							xposn=X2
							yposn=Y2-mVehicle.CurrentPosition(mTime)
							if mVehicle.GetIteration()==1:
								mVehicle.s = Rectangle(Point(xposn, yposn), Point(xposn+50, yposn+100))
								mVehicle.s.draw(win)
								mVehicle.s.setFill('blue')
								mVehicle.IncrementIteration()
							else:
								mVehicle.s.move(xposn-mVehicle.xposn,yposn-mVehicle.yposn)
							mVehicle.xposn=xposn
							mVehicle.yposn=yposn
						else:
							xposn=X3
							yposn=Y3+mVehicle.CurrentPosition(mTime)
							if mVehicle.GetIteration()==1:
								mVehicle.s = Rectangle(Point(xposn, yposn), Point(xposn+50, yposn+100))
								mVehicle.s.draw(win)
								mVehicle.s.setFill('blue')
								mVehicle.IncrementIteration()
							else:
								mVehicle.s.move(xposn-mVehicle.xposn,yposn-mVehicle.yposn)
							mVehicle.xposn=xposn
							mVehicle.yposn=yposn
						#print("pass")
						if prev_posn>0 and prev_posn-mVehicle.CurrentPosition(mTime)<mGap and mVehicle.CurrentPosition(mTime)>=mDistC+mDistI:
							#print("reset called")
							mVehicle.ReSetSpeed(prev_speed,0,mTime)						
						prev_posn=mVehicle.CurrentPosition(mTime)
						prev_speed=mVehicle.GetSpeed()
						
						#if(xposn==1900):
						#	print("Lane Num ",mLaneNum,"Slot Num ",mSlot.GetID(),"Vehicle Num  ",mVehicle.GetVehicleID(),"Posn  ",posn)
						#else:
							#print("Exited")

				
		win.close()
