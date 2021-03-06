def CompTimeStampRelative(AcqStartedLine,OriginLine):
	ColonIndex = AcqStartedLine.find(':')
	if AcqStartedLine[ColonIndex-2].isdigit():
		Hours = int(AcqStartedLine[ColonIndex-2:ColonIndex])
	else:
		Hours = int(AcqStartedLine[ColonIndex-1])
	Minutes = int(AcqStartedLine[ColonIndex+1:ColonIndex+3])
	AcqTime = Hours*60*60 + Minutes*60
	ColonIndex = OriginLine.find(':')
	if AcqStartedLine[ColonIndex-2].isdigit():
		Hours = int(OriginLine[ColonIndex-2:ColonIndex])
	else:
		Hours = int(OriginLine[ColonIndex-1])
	Minutes = int(OriginLine[ColonIndex+1:ColonIndex+3])
	OriginTime = Hours*60*60 + Minutes*60
	return OriginTime-AcqTime

def acqSysFormat(CurrAcqLine): # форматирование строки со значением AcquisitionSystem в поле EventSource не с пустым значением FileSizeBytes
	CurrAcqLine = CurrAcqLine[10:]
	TempLineForTime = '\t'+CurrAcqLine[CurrAcqLine.find(":")-15:CurrAcqLine.find(":")+4]
	TempLineFileNumber = CurrAcqLine[CurrAcqLine.find("AcquisitionSystem"):CurrAcqLine.find('\t',CurrAcqLine.find("AcquisitionSystem"))+3]
	TempLineForInflow = CurrAcqLine[CurrAcqLine.find("Inflow",CurrAcqLine.find("AcquisitionSystem")):CurrAcqLine.find(".sgy")+4]
	if TempLineFileNumber[len(TempLineFileNumber)-1] != '\t':
		TempLineFileNumber += '\t'
	CurrAcqLine = TempLineForTime + TempLineFileNumber + TempLineForInflow
	return CurrAcqLine

def userLineFormat(CurrUsrLine): # форматирование строки со значением User в поле EventSource
	usrLine = CurrUsrLine[CurrUsrLine.find("User")-36:-17]
	if usrLine[0] != '\t':
		usrLine = '\t'+usrLine
	usrLine = usrLine[:20]+usrLine[usrLine.find("User"):]
	return usrLine

with open(r"Example_file.log","r") as datafile:
	lines = datafile.readlines()
AcqStartedArr = []
for i in range(len(lines)):
	if "Acquisition Started" in lines[i]:
		AcqStartedArr.append(i)
AcqStartedArr.append(-1)
outputfile = open('result.txt','w')
outputfile.write('TimeStampRelative'+'\t'+'RunNumber'+'\t'+'TimeStampLocal'+'\t'+'EventSource'+'\t'+'FileNumber'+'\t'+'EventMessage'+'\n')
j = 0
k = 0
for i in range(len(lines)):
	if i == AcqStartedArr[k]:
		k+=1
		if i != AcqStartedArr[0]:
			j+=1
			continue
	if "AcquisitionSystem" in lines[i] and "Acquisition Started" not in lines[i]:
		AcqSys = i
	if "User" in lines[i] and i != len(lines)-1:
		if "User" in lines[i+1]:
			continue
		else:
			outputfile.write(str(CompTimeStampRelative(lines[AcqStartedArr[j]],lines[AcqSys]))+'\t'*2)

			outputfile.write(acqSysFormat(lines[AcqSys])+'\n')

			outputfile.write(str(CompTimeStampRelative(lines[AcqStartedArr[j]],lines[i]))+'\t'*2)

			outputfile.write(userLineFormat(lines[i])+'\n')

			if "Acquisition Started" in lines[i+1]:
				outputfile.write(str(CompTimeStampRelative(lines[i+1],lines[i+2]))+'\t'*2)
				outputfile.write(acqSysFormat(lines[i+2])+'\n')
			else:
				outputfile.write(str(CompTimeStampRelative(lines[AcqStartedArr[j]],lines[i+1]))+'\t'*2)
				outputfile.write(acqSysFormat(lines[i+1])+'\n')

outputfile.close()