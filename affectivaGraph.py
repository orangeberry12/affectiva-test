import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

"""
open file and return dictionary of data from affectiva
"""
def openFile(filepath):
	with open(filepath) as file:
		alldata = json.load(file)
	return alldata["events"]


"""
Grab arousal measurements and time stamps.
"""
def separateData(alldata):
	#time, arousal
	sepData = {"x":[], "y":[]}

	for event in alldata:
		if "speech" in event:
			arousal = event["speech"]["v-id-1"]["arousal"]
			start_time = event["start_time"]
			end_time = event["stop_time"]

			# sepData["y"]+=[arousal,arousal]
			# sepData["x"]+=[start_time,end_time]
			sepData["x"].append(start_time)
			sepData["y"].append(arousal)
	return sepData


"""
moving average
sampling frequency 0.3 seconds
speech event 1.2 seconds.
TODO: start time
"""
def movingAverage(sepData, window, step):
	avgData = {"time":[], "arousal":[]}
	# print("end of sep data: ", sepData["x"][len(sepData["x"])-1])
	# print("len: ", len(sepData["x"]))
	currentTime = 0
	while currentTime < sepData["x"][len(sepData["x"])-1]:
		start_window = currentTime-window/2
		end_window = currentTime+window/2
		windowData=[]
		for i in range(len(sepData["x"])):
			time = sepData["x"][i]
			if time<=end_window and time>=start_window:
				windowData.append(sepData["y"][i])
		if len(windowData)>0:
			avgArousal=sum(windowData)/len(windowData)
		else:
			avgArousal=0

		avgData["time"].append(currentTime)
		avgData["arousal"].append(avgArousal)

		currentTime+=step

	return avgData


"""
get range [start, end] of times from text analysis
"""
def getTimeRangeFromText(filepath):
	textData = openFile(filepath)
	start_time=float(textData[0]["start_time"])
	end_time=float(textData[len(textData)]["end_time"])
	return (start_time, end_time)


"""
graphs arousal data
TODO: grab timescale from text analysis
TODO: show unprocessed data?
"""
def graphAffectFromFile(filepath):
	affectivaData = openFile(filepath)
	arousalData = separateData(affectivaData)
	smallStep = movingAverage(arousalData, 1.2, 0.3)
	# nstep = movingAverage(arousalData,2.4,0.3)
	avgData = movingAverage(arousalData, 1.5, 0.3)

	
	fig, ax = plt.subplots()
	plt.xlim(0,600) # this will need to be changed to the length of the convo
	plt.ylim(0,100)
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.set_facecolor("#202020")
	ax.set_ylabel("vocal arousal")
	for i in range(1,6):
		ax.axhline(i*20, color = "#DADADA", linewidth = "0.25", linestyle="-", zorder = 1)

	# plt.scatter(arousalData["x"], arousalData["y"])
	# ax.plot(arousalData["x"],arousalData["y"], color="#b5b5b5")
	# plt.plot(smallStep["time"], smallStep["arousal"], color = "#a35dc6")
	ax.plot(avgData["time"], avgData["arousal"], color = "#5bb79d", linewidth=1)
	plt.show()
	return



graphAffectFromFile("test_GivingBadNewspt1.json")
