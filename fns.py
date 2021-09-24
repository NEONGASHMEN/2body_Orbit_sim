import math
import cnsts
import numpy as np
import linecache
from vpython import vector

def velocityMod(rMod,a):
	return math.sqrt(cnsts.muEarth*((2/rMod) - (1/a)))

def norm(vctr):
	rtn = math.sqrt(vctr[0]**2 + vctr[1]**2 + vctr[2]**2)
	return rtn

def prop(state):
	r = [state[0],state[1],state[2]]
	rMod = norm(r)
	rhat = [r[0]/rMod,r[1]/rMod,r[2]/rMod]
	vel = [state[3],state[4],state[5]]
	acc = []

	for j in range(0,3):
		
		acc.append((-1)*(cnsts.muEarth/(rMod*rMod))*rhat[j])
	
	w = [state[9],state[10],state[11]]
	wdot = [0,0,0]
	drvtiv = [vel[0],vel[1],vel[2],acc[0],acc[1],acc[2],w[0],w[1],w[2],wdot[0],wdot[1],wdot[2]]
	return drvtiv
	
def period(a):
	return 2*math.pi*math.sqrt((a**3)/cnsts.muEarth)

def mkEarth():
	u = np.linspace(0, 2 * np.pi, 100)
	v = np.linspace(0, np.pi, 100)
	x = 6378 * np.outer(np.cos(u), np.sin(v))
	y = 6378 * np.outer(np.sin(u), np.sin(v))
	z = 6378 * np.outer(np.ones(np.size(u)), np.cos(v))
	return [x,y,z]

def writeOut(writeData,name_s,title):
	for i in range(0,len(writeData)):
		outNm = str("./Out/" + name_s[i] + "_" + title + ".txt")		
		out = open(outNm,'w')
		for j in range(0,len(writeData[i])):
			out.write(str(writeData[i][j]))
			out.write("\r")
		out.close()

def popUp(grafik,n,txt,no):
	grafik.figure(n,figsize=(3,n-0.5))
	grafik.xlim([0,10])
	grafik.ylim([0,10])
	grafik.text(0,0,txt,fontsize=13)
	grafik.grid(False)
	grafik.axis('off')
	grafik.pause(0.001)
	grafik.show(block=False)
	
def grabData(path,cursor):
	name = 	linecache.getline(path,cursor)
	name = name.strip()
	name = name[21:]
	cursor = cursor + 1
	r_periG = linecache.getline(path,cursor)
	r_periG = r_periG.strip()
	r_periG = r_periG[20:]
	r_periG = float(r_periG)*1000 + cnsts.radEarth
	cursor = cursor + 1
	ecc = linecache.getline(path,cursor)
	ecc = ecc.strip()
	ecc = ecc[17:]
	ecc = float(ecc)
	cursor = cursor + 1
	inc = linecache.getline(path,cursor)
	inc = inc.strip()
	inc = inc[16:]
	inc = float(inc)*(math.pi/180)
	cursor = cursor + 1
	omega = linecache.getline(path,cursor)
	omega = omega.strip()
	omegaX = omega[14:19]
	omegaY = omega[20:25]
	omegaZ = omega[26:31]
	if omegaX.replace(" ","") == "":
		omegaX = "10.00"
	if omegaY.replace(" ","") == "":
		omegaY = "10.00"
	if omegaZ.replace(" ","") == "":
		omegaZ = "10.00"
	omega = [float(omegaX)*(math.pi/180),float(omegaY)*(math.pi/180),float(omegaZ)*(math.pi/180)]
	
	return [name,r_periG,ecc,inc,omega]

def colorConv(color_s):
	clrSat = [None]*len(color_s)
	for i in range(0,len(color_s)):
		if color_s[i] == "red":
			clrSat[i] = vector(255,0,0)
		elif color_s[i] == "green":
			clrSat[i] = vector(0,255,0)
		elif color_s[i] == "blue":
			clrSat[i] = vector(0,0,255)
		else:
			clrSat[i] = vector(255,255,255)
	return clrSat
	
def printBanner():
	
	print("\r")
	print("\r")
	print("        GGGGGGGGGGGGG                    SSSSSSSSSSSSSSS IIIIIIIIIIMMMMMMMM               MMMMMMMM")
	print("     GGG::::::::::::G                  SS:::::::::::::::SI::::::::IM:::::::M             M:::::::M")
	print("   GG:::::::::::::::G                 S:::::SSSSSS::::::SI::::::::IM::::::::M           M::::::::M")
	print("  G:::::GGGGGGGG::::G                 S:::::S     SSSSSSSII::::::IIM:::::::::M         M:::::::::M")
	print(" G:::::G       GGGGGG                 S:::::S              I::::I  M::::::::::M       M::::::::::M")
	print("G:::::G                               S:::::S              I::::I  M:::::::::::M     M:::::::::::M")
	print("G:::::G                                S::::SSSS           I::::I  M:::::::M::::M   M::::M:::::::M")
	print("G:::::G    GGGGGGGGGG ---------------   SS::::::SSSSS      I::::I  M::::::M M::::M M::::M M::::::M")
	print("G:::::G    G::::::::G -:::::::::::::-     SSS::::::::SS    I::::I  M::::::M  M::::M::::M  M::::::M")
	print("G:::::G    GGGGG::::G ---------------        SSSSSS::::S   I::::I  M::::::M   M:::::::M   M::::::M")
	print("G:::::G        G::::G                             S:::::S  I::::I  M::::::M    M:::::M    M::::::M")
	print(" G:::::G       G::::G                             S:::::S  I::::I  M::::::M     MMMMM     M::::::M")
	print("  G:::::GGGGGGGG::::G                 SSSSSSS     S:::::SII::::::IIM::::::M               M::::::M")
	print("   GG:::::::::::::::G                 S::::::SSSSSS:::::SI::::::::IM::::::M               M::::::M")
	print("     GGG::::::GGG:::G                 S:::::::::::::::SS I::::::::IM::::::M               M::::::M")
	print("        GGGGGG   GGGG                  SSSSSSSSSSSSSSS   IIIIIIIIIIMMMMMMMM               MMMMMMMM")
	print("\r")                                                                                                 
	print("\r")                                                                                          




