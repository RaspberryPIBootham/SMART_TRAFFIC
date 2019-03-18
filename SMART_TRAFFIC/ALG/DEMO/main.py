from Traffic.CC import CC
import time
import _thread as thread
mCC=CC()
#LaneOrder=[[0,1],[2,3]]
#mCC.SetUpLanes(4,LaneOrder)

def AddVehicles(self,mVal):
	
	print("starting")
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(1,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(2)
	mCC.AddNewVehicle(3,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(2,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(2)
	mCC.AddNewVehicle(1,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(3,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(2,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(2)
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(2)
	mCC.AddNewVehicle(1,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(2,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(3,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(1,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)
	mCC.AddNewVehicle(2,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(3,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(2)
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(1,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(2,time.perf_counter(),LaneOrder,1900,300,100,100)
	mCC.AddNewVehicle(3,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(3,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(1,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(2,time.perf_counter(),LaneOrder,1900,300,100,100)
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(1,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(2)
	mCC.AddNewVehicle(3,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(2,time.perf_counter(),LaneOrder,1900,300,100,100)
	time.sleep(1)
	mCC.AddNewVehicle(0,time.perf_counter(),LaneOrder,1900,300,100,100)

def Plot(self):
	#mCC.PlotPositions(0,2100,4100,2000,2100,4100,2000,0,1900,300,120)
	mCC.StartDemo(10)








try:
	print("start")
	#AddVehicles(0,5)
	#thread.start_new_thread(AddVehicles,(0,5))
	#time.sleep(0)
	#thread.start_new_thread(Plot(0))
	Plot(10)
	print("end")
except:
   	print ("Error")


while 1:
   pass



#print("***********")
#time.sleep(200)
#mCC.PlotPositions(time.perf_counter(),10,10,10,10,10,10,10,10)
#print("***********")
#time.sleep(250)
#mCC.PlotPositions(time.perf_counter(),10,10,10,10,10,10,10,10)
