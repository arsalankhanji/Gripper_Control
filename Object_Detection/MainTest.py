
import multiprocessing
from multiprocessing import Value, Array, Lock
from FunctionTest_Folder import functionTest as FT

classes = Array('f',3) # creating shared variable to access detected classes
frameRate = Value('f',1)


P1 = multiprocessing.Process(target=FT.functionCall , args=(frameRate,classes) )
P1.start()

while True:
	print(classes[:])
	print(type(classes))
	print(frameRate.value)
