import math
import cnsts
import fns
import matplotlib.pyplot as grafik
import numpy as npy
from vpython import *
import linecache

fns.printBanner()

no_of_sats = linecache.getline("./In/satData.txt",10)
no_of_sats = no_of_sats.strip()
no_of_sats = int(no_of_sats[17:])

r_periG_s = [None]*no_of_sats
inc_s = [None]*no_of_sats
e_s = [None]*no_of_sats
prd_s = []
name_s = [None]*no_of_sats
color_s = [None]*no_of_sats

end = 0
i = 0
ipFile = open("./In/satData.txt",'r')
while i==0:
	end = end + 1
	lin = ipFile.readline()
	lin = lin.strip()
	if lin == "EOF":
		i = 1

cursor_srt = 14
blockSize = 8
for i in range(0,no_of_sats):
	cursor = cursor_srt	
	[name_s[i],r_periG_s[i],e_s[i],inc_s[i],color_s[i]] = fns.grabData("./In/satData.txt",cursor)
	cursor_srt = cursor_srt + blockSize

for i in range(0,no_of_sats):
	prd_s.append(round(fns.period(r_periG_s[i]/(1 - e_s[i]))))
	

ip1 = input("Do you want data output ?(N/y) ")
print()	
ip2 = float(input("Duration of simulation in orbital time(hrs) "))
tfinal = int(ip2*60*60)
step = 1
output = [None]*no_of_sats
crdntData = [None]*no_of_sats
velData = [None]*no_of_sats
print()
print()

for i in range(0,no_of_sats):
	r_periG = r_periG_s[i]
	inc = inc_s[i]
	e = e_s[i]
	name = name_s[i]	
	prd = prd_s[i]	
	
	stateout = [None]*prd
	crdnts = [None]*prd
	vels = [None]*prd
	rp = [r_periG,0,0]
	rpMod = fns.norm(rp)
	a = r_periG/(1 - e)
	velMod_p = fns.velocityMod(rpMod,a)
	vel_p = [0,velMod_p*math.cos(inc),velMod_p*math.sin(inc)]
	
	state = [rp[0],rp[1],rp[2],vel_p[0],vel_p[1],vel_p[2]]
	
	for z in range(0,prd,step):
		tempstate = state.copy()		
		k = [None]*len(state)		
		stateout[z] = state.copy()
		crdnts[z] = state[0:3].copy()
		vels[z] = state[3:6].copy()
		k1 = fns.prop(state)
		for l in range(0,len(state)):
			tempstate[l] = state[l] + (k1[l]*step/2)
		k2 = fns.prop(tempstate)
		for l in range(0,len(state)):
			tempstate[l] = state[l] + (k2[l]*step/2)		
		k3 = fns.prop(tempstate)
		for l in range(0,len(state)):
			tempstate[l] = state[l] + (k3[l]*step)
		k4 = fns.prop(tempstate)
		for l in range(0,len(state)):
			k[l] = (1/6)*(k1[l] + 2*k2[l] + 2*k3[l] + k4[l])
		for l in range(0,len(state)):
			state[l] = state[l] + k[l]*step
		
			
			
		perc = (z/prd)*100
		print("Percentage completed: ",perc,"% ",end="\r",flush = True)
		

	output[i] = stateout.copy()
	crdntData[i] = crdnts.copy()
	velData[i] = vels.copy()

print("\r")

if (ip1 == 'y') or (ip1 == 'Y'):
	fns.writeOut(crdntData,name_s,"crdnts")
	fns.writeOut(velData,name_s,"vel")
		


scene = canvas(title='\t\t\tSIMULATION\t\t\t',width=1900,height=1000)

curveArr = [None]*no_of_sats
for i in range(0,no_of_sats):
	curveArr[i] = curve()
	for j in range(0,len(crdntData[i])):
		curveArr[i].append(vector(crdntData[i][j][0]/1000,crdntData[i][j][1]/1000,crdntData[i][j][2]/1000))
		
if cnsts.shwErth == 1:
	erth = sphere(pos=vector(0,0,0),radius=cnsts.radEarth/1000,color=color.blue)

arrow(pos=vector(0,0,0),axis=vector(10000,0,0),shaftwidth=30,color = color.cyan)
arrow(pos=vector(0,0,0),axis=vector(0,10000,0),shaftwidth=30,color = color.green)
arrow(pos=vector(0,0,0),axis=vector(0,0,10000),shaftwidth=30,color = color.orange)
arrow(pos=vector(0,0,0),axis=vector(-10000,0,0),shaftwidth=30,color = color.cyan)
arrow(pos=vector(0,0,0),axis=vector(0,-10000,0),shaftwidth=30,color = color.green)
arrow(pos=vector(0,0,0),axis=vector(0,0,-10000),shaftwidth=30,color = color.orange)

satObj = [None]*no_of_sats
clrSat = [None]*no_of_sats
for i in range(0,no_of_sats):
	if color_s[i] == "red":
		clrSat[i] = vector(255,0,0)
	elif color_s[i] == "green":
		clrSat[i] = vector(0,255,0)
	elif color_s[i] == "blue":
		clrSat[i] = vector(0,0,255)
	else:
		clrSat[i] = vector(255,255,255)
	satObj[i] = sphere(pos=vector(0,0,0),radius=100,color = clrSat[i])

for i in range(0,tfinal,cnsts.simStep):
	for j in range(0,no_of_sats):
		if i > len(crdntData[j])-1:
			crdntData[j] = crdntData[j] + crdntData[j]
		satObj[j].pos = vector(crdntData[j][i][0]/1000,crdntData[j][i][1]/1000,crdntData[j][i][2]/1000)
		rate(cnsts.simSpeed)	



'''
fig = grafik.figure()
mainPlt = fig.add_subplot(projection ='3d')

if cnsts.shwErth == 1:
	mainPlt.plot_surface(Xdata_erth,Ydata_erth,Zdata_erth,color='#89CFF0',alpha=0.8,zorder=50)

mainPlt.scatter(0,0,0,color='black',zorder=0)

axisDist = (cnsts.radEarth/1000) + 2000
mainPlt.plot([-axisDist,axisDist],[0,0],[0,0],label='X')
mainPlt.plot([0,0],[-axisDist,axisDist],[0,0],label='Y')
mainPlt.plot([0,0],[0,0],[-axisDist,axisDist],label='Z')


for j in range(0,no_of_sats):

	Xdata_orb = []
	Ydata_orb = []
	Zdata_orb = []
	for i in range(0,prd_s[j]):
		Xdata_orb.append(output[j][i][0]/1000)
		Ydata_orb.append(output[j][i][1]/1000)
		Zdata_orb.append(output[j][i][2]/1000)
	
	
	mainPlt.plot3D(Xdata_orb,Ydata_orb,Zdata_orb,zorder=20,color=cnsts.satColor[j],label=name_s[j])

pltCltn = [None]*no_of_sats
pltMat = output.copy()
mainPlt.legend()

for i in range(0,tfinal,cnsts.simSpeed):
	
	for j in range(0,no_of_sats):
		if i > len(pltMat[j])-1:
			pltMat[j] = pltMat[j] + pltMat[j]
		pltCltn[j] = mainPlt.scatter(pltMat[j][i][0]/1000,pltMat[j][i][1]/1000,pltMat[j][i][2]/1000,color=cnsts.satColor[j],zorder=10)

	grafik.pause(0.00000001)
	for j in range(0,no_of_sats):
		pltCltn[j].remove()

del pltCltn


grafik.show()
'''









