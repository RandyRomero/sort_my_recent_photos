#!python3 

import os, shutil, sys, collections


logFile = open('D:\\PythonPhoto\\sortedPhotos\\logFile.txt', 'w')
logFile.write('Program started. Log file created\n\n')

unsortedPhotos = ('D:\\PythonPhoto\\unsortedPhotos')
sortedPhotos = ('D:\\PythonPhoto\\sortedPhotos')
logFile.write('Path to main folders created\n\n')

################################## sizes ###############################	

def sizes(files):
	logFile.write('Start to figuring out total size of unsorted files\n\n')

	totalSize = 0
	for file in files:
		size = os.path.getsize(os.path.join(unsortedPhotos, file))
		totalSize += size
	totalSize = totalSize / 1024 / 1024

	logFile.write('Total size of ' + str(len(files)) + ' files is ' 
		+ str("%0.2f" % totalSize) + ' MB\n\n')
	print('\nTotal size of ' + str(len(files)) + ' files is ' 
		+ str("%0.2f" % totalSize) + ' MB\n')

def printLogFilesByExt(ilk, listFiles):
	logFile.write('The total amount of ' + ilk +' files is ' + 
		str(len(listFiles)) + '\n')	
	print('The total amount of ' + ilk + ' files is ' 
		+ str(len(listFiles)) + '\n')
	logFile.write('\nList of ' + ilk + ' files:\n')	
	if len(listFiles) < 1:
		logFile.write('empty\n')
	else:
		for file in listFiles:
			logFile.write(file + '\n')

############################### sortEngine  ##############################			

def sortEngine():
	logFile.write('Getting list with names of files in ' + unsortedPhotos + 
		'\n\n')
	files = os.listdir(unsortedPhotos)

	logFile.write('Print that in ' + unsortedPhotos + ' are ' 
		+ str(len(files)) + ' files\n\n')
	print('\nHere are ' + str(len(files)) + ' unsorted files.')
	
	logFile.write('Call sizes()\n\n')
	sizes(files)


	jpgList, pngList, videoList, otherList = ([] for i in range(4))
	#the way to declare multiple lists

	logFile.write('Start to sort files by extension...\n\n')
	for item in os.listdir(unsortedPhotos):
		if item.endswith('.PNG') or item.endswith('.png'):
			pngList.append(item)
		elif (item.endswith('.JPG') or item.endswith('.jpg') 
			or item.endswith('.JPEG')):
			jpgList.append(item)
		elif item.endswith('.MP4') or item.endswith('.3GP'):
			videoList.append(item)
		else:
			otherList.append(item)
			print(item)

	extLists = collections.OrderedDict([('JPG', jpgList), ('PNG', pngList), 
		('video', videoList), ('other', otherList)])
	#use OrderedDict to preserve insertion order. Python 3.6 default dict can
	#do it from box but I want to keep compatibility with older versions

	for k,v in extLists.items():
		 printLogFilesByExt(k,v)
	#prints and logs to file list and amount of files by their extention	 


########################  Begining of the program  #######################

start = input('\nStart to look for your photos? (y/n) Your answer is: ')
logFile.write('Start to look for your photos? (y/n)\n\n')

while True:
	if start == 'y':
		logFile.write('Got "y". Call sortEngine()\n\n')
		sortEngine()
		break
	elif start == 'n':
		logFile.write('Got "n". Exit script.\n\n')
		print('Goodbye')
		sys.exit()
	else:
		logFile.write('Got wrong input. Ask again...\n\n')
		print('Input error. You should type in y or n')	
		continue

logFile.write('\nProgram has reached end. Closing logFile.')
logFile.close()		


