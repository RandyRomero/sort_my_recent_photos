#!python3 

import copy, os, shutil, sys, collections, re

########################check if folder for work exist#################

if os.path.exists(os.path.join('D:/', 'PythonPhoto', 'sortedPhotos')):
	#mind the syntax: it is 'D:/', neither 'd', nor 'D:', nor "D:/"
	logFile = open('D:\\PythonPhoto\\sortedPhotos\\logFile.txt', 'w')
	logFile.write('Program started. Log file created\n\n')
else:
	print(os.path.join('D:', 'PythonPhoto', 'sortedPhotos') + ' doesn\'t exist')
	logFile.write(os.path.join('D:', 'PythonPhoto', 'sortedPhotos') 
		+ ' doesn\'t exist')
	sys.exit()

if os.path.join('D:/', 'PythonPhoto', 'unsortedPhotos'):
	unsortedPhotos = ('D:\\PythonPhoto\\unsortedPhotos')
else:
	print(os.path.join('D:', 'PythonPhoto', 'sortedPhotos') + ' doesn\'t exist')
	logFile.write(os.path.join('D:', 'PythonPhoto', 'sortedPhotos') 
		+ ' doesn\'t exist')
	sys.exit()

sortedPhotos = ('D:\\PythonPhoto\\sortedPhotos')
logFile.write('Path to main folders created\n\n')

################################## sizes ###############################	

def sizes(files):
	
	totalSize = 0
	for file in files:
		size = os.path.getsize(os.path.join(unsortedPhotos, file))
		totalSize += size
	return totalSize / 1024 / 1024

######################### log files by extention #########################	

def printLogFilesByExt(ilk, listFiles):
	logFile.write('\nTotal amount of ' + ilk +' files is ' + 
		str(len(listFiles)))	
	print('Total amount of ' + ilk + ' files is ' 
		+ str(len(listFiles)))
	print('Total size of ' + ilk + ' files is ' + #where is log of total size?
		str('%0.2f' % sizes(listFiles)) + ' MB\n')
	logFile.write('\nList of ' + ilk + ' files:\n')	
	if len(listFiles) < 1:
		logFile.write('empty\n')
	else:
		for file in listFiles:
			logFile.write(file + '\n')

############################# Sort by Date ##############################

def sortByDate(extLists):

	#First we need to know home many years we have. That's why we 
	#send files through regex - to get all possible years and store them
	#to list

	yearList = []

	logFile.write('Compile regex for dates in files...\n\n')
	dateRegex = re.compile(r''' 
		^((?:201[0-9]))- 		#year - Group 1
		((?:0|1)(?:\d))-		#month - Group 2
		((?:[0-3])(?:\d))		#day - Group 3
		.*$ 					#all other symbols after
		
		''', 
		re.VERBOSE)

	for k, v in extLists.items(): 
		if k == 'PNG' or k == 'already sorted': #k is name of list
				continue
		for item in v: #v is list of files
			mo = dateRegex.search(item)
			if mo != None:
				yearNum = mo.group(1) #return year from file name
				if yearNum not in yearList:
					yearList.append(yearNum) 

	#now we need a dictionary in order to get specific group of month
	#by passing a year
	yearDict = collections.OrderedDict([])

	january, february, march, april = ([] for i in range(4))
	may, june, july, august = ([] for i in range(4))
	september, october, november, december = ([] for i in range(4))
	#declare 12 empty lists fo each month

	twelveMonth = collections.OrderedDict([])
	twelveMonth['01'] = january
	twelveMonth['02'] = february
	twelveMonth['03'] = march
	twelveMonth['04'] = april
	twelveMonth['05'] = may
	twelveMonth['06'] = june
	twelveMonth['07'] = july
	twelveMonth['08'] = august
	twelveMonth['09'] = september
	twelveMonth['10'] = october
	twelveMonth['11'] = november
	twelveMonth['12'] = december

	mismatchedFiles = [] #for files that not match regex

	for year in yearList: 
		yearDict['{}'.format(year)] = copy.deepcopy(twelveMonth)
	#create dictionary key for every necessary year and tie its with
	#value that's a new DEEPCOPY of twelveMonth. Without deepcopy we get
	#same lists of files in every year 

	for k, v in extLists.items(): 
		if k == 'PNG' or k == 'already sorted': #k is name of extention
				continue
		for item in v: #v is list of files
			mo = dateRegex.search(item)
			if mo != None:
				yearDict[mo.group(1)][mo.group(2)].append(item)
				#add file to corresponding location, 
				#e.g.: year 2016 month january
				logFile.write('\nFile ' + item + ' was added to ' + 
					'yearDict[' + mo.group(1) + '][' + mo.group(2) + ']')
			else:
				mismatchedFiles.append(item)

	monthToPrint = {'01': 'January',
					'02': 'February',
					'03': 'March',
					'04': 'April',
					'05': 'May',
					'06': 'June',
					'07': 'July',
					'08': 'August',
					'09': 'September',
					'10': 'October',
					'11': 'November',
					'12': 'December'}	

	print('\nSorted out by date:')
	for yearDictKey, yearDictValue in yearDict.items():
		for monthDictKey, monthDictValue in yearDictValue.items():
			if len(monthDictValue) != 0:
				print(str(len(monthDictValue)) + 
					' file was created in ' + monthToPrint[monthDictKey] + 
					' of ' + yearDictKey + '.')
				logFile.write('\n\n' + str(len(monthDictValue)) + 
				' file was created in ' + monthToPrint[monthDictKey] + ' of ' 
				+ yearDictKey + ': \n')
			for file in monthDictValue:
				logFile.write(file + '\n')
			#log list of photo by month and year

	if len(mismatchedFiles) > 0:
		logFile.write('\n\nHere are ' + str(len(mismatchedFiles)) + 
			' mismatched files. They won\'t be copied anywhere:\n')
		print('\nHere are ' + str(len(mismatchedFiles)) + 
			' mismatched files. They won\'t be copied anywhere:')
		for file in mismatchedFiles:
			print(file)
			logFile.write(file + '\n')
			#message about mismatch files
	
	return len(mismatchedFiles), yearDict	

############################### sortByExtEngine  ##########################			

def sortByExtEngine():
	logFile.write('Getting list with names of files in ' + unsortedPhotos + 
		'\n\n')
	files = os.listdir(unsortedPhotos)

	allUnsortedFiles = len(files)

	logFile.write('There are ' + str(allUnsortedFiles) + ' files in ' 
		+ unsortedPhotos + '\n\n')
	print('\nHere are ' + str(allUnsortedFiles) + ' unsorted files.')

	###figuring out total size of all unsorted files###

	logFile.write('Call sizes()\n\n')
	logFile.write('Start to figuring out total size of unsorted files\n\n')
	totalSize = sizes(files)
	logFile.write('Total size of ' + str(allUnsortedFiles) + ' files is ' 
		+ str("%0.2f" % totalSize) + ' MB\n\n')
	print('\nTotal size of ' + str(allUnsortedFiles) + ' files is ' 
		+ str("%0.2f" % totalSize) + ' MB\n')

	######sort out files by extentions######
	
	jpgList, pngList, videoList, otherList = ([] for i in range(4))
	#the way to declare multiple lists

	logFile.write('Start to sort files by extension...\n\n')
	for item in os.listdir(unsortedPhotos):
		elif item.endswith('.PNG') or item.endswith('.png'):
			pngList.append(item)
		elif (item.endswith('.JPG') or item.endswith('.jpg') 
			or item.endswith('.JPEG')):
			jpgList.append(item)
		elif item.endswith('.MP4') or item.endswith('.3GP'):
			videoList.append(item)
		else:
			otherList.append(item)
			print(item)

	extLists = collections.OrderedDict([('JPG', jpgList), 
										('PNG', pngList), 
										('video', videoList), 
										('other', otherList)])
	#use OrderedDict to preserve insertion order. Python 3.6 default dict can
	#do it from box but I want to keep compatibility with older versions

	for k,v in extLists.items():
		 printLogFilesByExt(k,v)
	#prints and logs to file list and amount of files by their extention


					

	return extLists, allUnsortedFiles, len(alreadySorted)

######################## Check already sorted files  ####################

	def checkAlreadySortedFiles():
		
	

	#### message about already sorted files ###

	# if len(alreadySorted) > 0: 
	# 	print('Warning: ' + str(len(alreadySorted)) + ' already sorted files.')
	# 	logFile.write('Warning: ' + str(len(alreadySorted)) + 
	# 		' already sorted files.\n')
	# 	logFile.write('Here is list of already sorted files: \n')
	# 	for item in alreadySorted:
	# 		logFile.write(item + '\n')

################################## copy PNG  ############################

def copyPng(listOfPng):
	logFile.write('Copy PNG files...\n')
	print('Copy PNG files...\n')

	alreadyExist = 0
	wasCopied = 0
	
	if os.path.exists(os.path.join(sortedPhotos, 'PNG')):
		print('\nWarning: folder PNG in destionation folder already exists')
	else:	
		os.mkdir(os.path.join(sortedPhotos, 'PNG'))

	for item in listOfPng:
		if os.path.exists(os.path.join(sortedPhotos, 'PNG', item)):
			logFile.write('Error: ' + item + ' already in destination folder\n')
			alreadyExist += 1 #count skipped files
			continue
		else:
			shutil.copy2(os.path.join(unsortedPhotos, item), 
				os.path.join(sortedPhotos, 'PNG', item)) #copy file
			logFile.write(os.path.join(unsortedPhotos, item) + 
				' copy to ' + os.path.join(sortedPhotos, 'PNG', item) + '\n')
			#log which and where to file was copied
			renameEngine(unsortedPhotos, item) #rename file as [sorted]
			wasCopied += 1 #count how many files were copied
			

	if wasCopied > 0:
		logFile.write(str(wasCopied) + ' PNG files were copied\n')
		print('\n' + str(wasCopied) + ' PNG files were copied')
		if alreadyExist == 1:
			print('There is 1 skipped file')
			logFile.write('\nThere is 1 skipped file')
		elif alreadyExist > 1:
			print(str(alreadyExist) + ' PNG files were skipped')
			logFile.write(str(alreadyExist) + ' PNG files were skipped\n')
		elif alreadyExist == 0:
			print('There is no skipped file')	
			logFile.write('There are no skipped files\n')	
	else:
		print('All files (' + str(alreadyExist) + ' from ' 
			+ str(len(listOfPng)) + ') already exist in destination folder')
		logFile.write('\nAll files(' + str(alreadyExist) + ' from ' + 
			str(len(listOfPng)) + ') already exist in destination folder')

#############################  copyEngine  ##############################

def copyEngine(filesByDate):
	logFile.write('\ncopyEngine started')
	print('Copy engine doesn\'t exist yet :)')

	

#############################  First menu ###############################


logFile.write('Start to analize for your files? (y/n)\n\n')

while True:
	start = input('\nStart to analize your files? (y/n)\nYour answer is: ')
	if start == 'y':
		logFile.write('Got "y". Call sortByExtEngine()\n\n')
		sbeeResult = sortByExtEngine()
		mismatchedFiles, filesByDate = sortByDate(sbeeResult[0])
		break
	elif start == 'n':
		logFile.write('Got "n". Exit script.\n\n')
		print('Goodbye')
		sys.exit()
	else:
		logFile.write('Got wrong input. Ask again...\n\n')
		print('Input error. You should type in y or n')	
		continue

##################### Menu to ask user to start copying ##################

logFile.write('\n\n' + str(sbeeResult[1] - mismatchedFiles - sbeeResult[2]) + 
	' files are ready to copy. Start? (y/n)\n\n')

while True:
	start = input('\n\n' + str(sbeeResult[1] - mismatchedFiles - 
		sbeeResult[2]) + 
		' files are ready to copy. Start? (y/n)\nYour answer is: ')
	if start == 'y':
		logFile.write('Got "y". Call copyEngine()\n\n')
		if len(sbeeResult[0]['PNG']) > 0:
			copyPng(sbeeResult[0]['PNG']) #pass pngList to copyPng
		copyEngine(filesByDate)
		break
	elif start == 'n':
		logFile.write('Got "n". Exit script.\n\n')
		print('Goodbye')
		sys.exit()
	else:
		logFile.write('Got wrong input. Ask again...\n\n')
		print('Input error. You should type in y or n.')	
		continue

logFile.write('\nProgram has reached end. Closing logFile.')
logFile.close()



#TODO compare of sorted and unsorted in order to figure out
#if sorting went without missing any file

#TODO delete unsortedFiles by users submit after checking that unsorted 
#sorted files are equal in total quatity and size


# ^((?:201[0-9]))-((?:0|1)(?:[0-9]))-((?:[0-3])(?:[0-9])).*$