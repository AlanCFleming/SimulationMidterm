#!/usr/bin/python3
import random
import simpy
import numpy


###########################################
#Author: Alan Fleming
#Email: alanfleming1998@gmail.com
#Description: This is a script to simulate a 2 line 2 pump gas station. 
#Asummuptions: every simulation time represent 1 minute and the simulation will run for 1020 simulation time units.
#              The customer will grab either of the slots in their line if they are open. IE, if the second pump in line has a car and the first doesnt, waiting cars will drive around to the car to access the open pump.
#              Each new customer will join a random line when they arrive.
#              pump1 represents the pumps for one line, pump2 the other
###########################################


#process to make cars
def cargen(env, pumps, lines):
    print("starting gen")
    number = 0
    while(True):
        #select pump, line, and wait for a new car
        pump = random.randrange(0,2,1)
        line = random.randrange(0,2,1)
        t = random.expovariate(1.0/5)
        #print(pump,line,t)
        yield env.timeout(t)
        #make and run a new car
        c = car(env, number, pumps[pump], lines[line])
        env.process(c)
        number = number+1

#process to run cars through carwash
def car(env, number, pumps, line):
    print("%d arrives at gas station at %d" % (number, env.now))
    #have the car grab a spot in line
    myLine = line.request()
    yield myLine

    #grab an open pump and release the top spot in line
    myPump = pumps.request()
    yield myPump
    line.release(myLine)
    #wait for a random amount of time determined by a log normal distribution of mean=5, shape=0.5, and scale of 1.5 to release the pump
    t = random.lognormvariate(5,0.5)*1.5
    yield env.timeout(t)
    pumps.release(myPump)
    print("%d leaves at gas station at %d" % (number, env.now))






#seed the random number
random.seed(2019)


##reminders for random numbers
#arival random number => random.expovariate(1.0/mean)
#pump random number => random.lognormvariate(mean,shape)*scale

##settup and run the simpulation

#make the enviroment
env = simpy.Environment()

#setup the resources
line1 = simpy.Resource(env,capacity=1)
line2 = simpy.Resource(env,capacity=1)
lines = [line1,line2]

pump1 = simpy.Resource(env,capacity=2)
pump2 = simpy.Resource(env,capacity=2)
pumps = [pump1,pump2]

#setup the process
env.process(cargen(env, pumps, lines))

#run the sim for 1020 time units
env.run(until = 1020)
