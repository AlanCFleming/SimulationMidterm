#!/usr/bin/python3
import simpy
import numpy


###########################################
#Author: Alan Fleming
#Email: alanfleming1998@gmail.com
#Description: This is a script to simulate a 2 line 2 pump gas station. 
#Asummuptions: every simulation time represent 1 minute and the simulation will run for 1020 simulation time units.
#              The customer will grab either of the slots in their line if they are open. IE, if the second pump in line has a car and the first doesnt, waiting cars will drive around to the car to access the open pump.
#              Each new customer will join the opposite line than the last.
#              Phyisical pumps 1 and 2 will be split into pump1, pump2, pump3, and pump4 to represent dual sided pumps.
#              Pump1 and pump3 are the sides of one pump while pump2 and pump4 are the sides of the other.
###########################################


#process to make cars
def cargen(env, pump1, pump2, pump3, pump4, line1, line2):
    print("starting gen")
    yield env.timeout(1)
    c = car(env, 0, pump1, pump2, line1)
    env.process(c)

#process to run cars through carwash
def car(env, number, pump1, pump2, line):
    print("%d arrives at gas station at %d" % (number, env.now))
    yield env.timeout(1)



#seed the random number
numpy.random.seed(2020)
##settup and run the simpulation

#make the enviroment
env = simpy.Environment()

#setup the resources
line1 = simpy.Resource(env,capacity=1)
line2 = simpy.Resource(env,capacity=1)
pump1 = simpy.Resource(env,capacity=1)
pump2 = simpy.Resource(env,capacity=1)
pump3 = simpy.Resource(env,capacity=1)
pump4 = simpy.Resource(env,capacity=1)

#setup the process
env.process(cargen(env, pump1, pump2, pump3, pump4, line1, line2))

#run the sim
env.run()
