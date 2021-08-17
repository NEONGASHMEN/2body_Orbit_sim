import math
import cnsts
import fns
import matplotlib.pyplot as grafik
import numpy as npy

no_of_sats = int(input("How many satellites needed: "))

r_periG_s = []
inc_s = []
e_s = []
prd_s = []
name_s = []

for i in range(0,no_of_sats):
	ip0 = input("Satellite name: ")
	name_s.append(ip0)
	ip1 = float(input("Perigee altitude of " + ip0 + " (kms): "))
	r_periG_s.append(ip1*1000 + cnsts.radEarth)
	ip2 = float(input("Orbit inclination of " + ip0 + " (deg): "))
	inc_s.append(ip2*math.pi/180)
	ip3 = float(input("Orbit eccentricity of " + ip0 + " (0-1): "))
	e_s.append(ip3)
	prd_s.append(round(fns.period(r_periG_s[i]/(1 - e_s[i]))))

	
ip4 = float(input("Duration of simulation in orbital time(hrs) "))
tfinal = int(ip4*60*60)
step = 1
output = [None]*no_of_sats
print()
print()

for i in range(0,no_of_sats):
	r_periG = r_periG_s[i]
	inc = inc_s[i]
	e = e_s[i]
	name = name_s[i]	
	prd = prd_s[i]	
	
	stateout = [None]*prd
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

writeData = output.copy()
if cnsts.dataOut == 1:
	fns.writeOut(writeData,name_s)
del writeData		

[Xdata_erth,Ydata_erth,Zdata_erth] = fns.mkEarth()

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










