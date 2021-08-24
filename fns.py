import math
import cnsts
import numpy as np
import linecache

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
	
	drvtiv = [vel[0],vel[1],vel[2],acc[0],acc[1],acc[2]]
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
	color = linecache.getline(path,cursor)
	color = color.strip()
	color = color[15:]
	
	return [name,r_periG,ecc,inc,color]

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




