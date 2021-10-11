import math
import cnsts
import fns
import matplotlib.pyplot as grafik
import numpy as npy
from vpython import *
import linecache

fns.printBanner()

no_of_sats = linecache.getline("./In/satData.txt",11)
no_of_sats = no_of_sats.strip()
no_of_sats = int(no_of_sats[17:])

r_periG_s = [None]*no_of_sats
inc_s = [None]*no_of_sats
e_s = [None]*no_of_sats
prd_s = []
name_s = [None]*no_of_sats
color_s = [None]*no_of_sats
res_s = [None]*no_of_sats

end = 0
i = 0
ipFile = open("./In/satData.txt",'r')
while i==0:
	end = end + 1
	lin = ipFile.readline()
	lin = lin.strip()
	if lin == "EOF":
		i = 1

cursor_srt = 15
blockSize = 8
for i in range(0,no_of_sats):
	cursor = cursor_srt	
	[name_s[i],r_periG_s[i],e_s[i],inc_s[i],res_s[i]] = fns.grabData("./In/satData.txt",cursor)
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
radData = [None]*no_of_sats
omegaData = [None]*no_of_sats
print()
print()

for i in range(0,no_of_sats):
	r_periG = r_periG_s[i]
	inc = inc_s[i]
	e = e_s[i]
	name = name_s[i]	
	secnds = tfinal
	w = res_s[i]	
	
	stateout = [None]*secnds
	crdnts = [None]*secnds
	vels = [None]*secnds
	rads = [None]*secnds
	omegas = [None]*secnds
	rp = [r_periG,0,0]
	rpMod = fns.norm(rp)
	a = r_periG/(1 - e)
	velMod_p = fns.velocityMod(rpMod,a)
	vel_p = [0,velMod_p*math.cos(inc),velMod_p*math.sin(inc)]
	
	state = [rp[0],rp[1],rp[2],vel_p[0],vel_p[1],vel_p[2],0,0,0,w[0],w[1],w[2]]
	
	for z in range(0,secnds,step):
		tempstate = state.copy()		
		k = [None]*len(state)		
		stateout[z] = state.copy()
		crdnts[z] = state[0:3].copy()
		vels[z] = state[3:6].copy()
		rads[z] = state[6:9].copy()
		omegas[z] = state[9:12].copy()
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
		
			
			
		perc = (z/secnds)*100
		print("Percentage completed: ",perc,"% ",end="\r",flush = True)
		

	output[i] = stateout.copy()
	crdntData[i] = crdnts.copy()
	velData[i] = vels.copy()
	radData[i] = rads.copy()
	omegaData[i] = omegas.copy()

print("\r")

if (ip1 == 'y') or (ip1 == 'Y'):
	fns.writeOut(crdntData,name_s,"crdnts")
	fns.writeOut(velData,name_s,"vel")
	fns.writeOut(radData,name_s,"ang")
	fns.writeOut(omegaData,name_s,"omega")
	print("\rData written in ./Out/")

txt2shw = ""
satclrTxt = ""
for i in range(0,no_of_sats):
	txt2shw = txt2shw + '\n\t'+'<b style="color:'+cnsts.color_s[i]+'">'+(cnsts.color_s[i]).capitalize()+'</b>'+'  :  '+name_s[i]
	satclrTxt = satclrTxt + "\n" + name_s[i] + " : " + (cnsts.color_s[i]).capitalize()
	
scene1 = canvas(title=' SIMULATION',width=1900,height=1000,align='left')

fns.popUp(grafik,1,satclrTxt,no_of_sats)
		
if cnsts.shwErth == 1:
	erth = sphere(pos=vector(0,0,0),radius=cnsts.radEarth/1000,texture=textures.earth)

arrow(pos=vector(0,0,0),axis=vector(10000,0,0),shaftwidth=30,color = color.cyan)
arrow(pos=vector(0,0,0),axis=vector(0,10000,0),shaftwidth=30,color = color.green)
arrow(pos=vector(0,0,0),axis=vector(0,0,10000),shaftwidth=30,color = color.orange)
arrow(pos=vector(0,0,0),axis=vector(-10000,0,0),shaftwidth=30,color = color.cyan)
arrow(pos=vector(0,0,0),axis=vector(0,-10000,0),shaftwidth=30,color = color.green)
arrow(pos=vector(0,0,0),axis=vector(0,0,-10000),shaftwidth=30,color = color.orange)

satObj = [None]*no_of_sats
clrSat = fns.colorConv(cnsts.color_s)
for i in range(0,no_of_sats):
	satObj[i] = box(pos=vector(0,0,0),length=100,height=100,width=100,color = clrSat[i],make_trail=True,trail_type="points",interval=5,retain=(int(prd_s[i]/5)))


for i in range(0,tfinal,cnsts.simStep):
	for j in range(0,no_of_sats):
		satObj[j].pos = vector(crdntData[j][i][0]/1000,crdntData[j][i][1]/1000,crdntData[j][i][2]/1000)
		rate(cnsts.simSpeed)


grafik.show()



