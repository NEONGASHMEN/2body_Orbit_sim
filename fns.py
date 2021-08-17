import math
import cnsts
import numpy as np

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

def writeOut(writeData,name_s):
	for i in range(0,len(writeData)):
		outNm = str(name_s[i] + ".txt")		
		out = open(outNm,'w')
		out.write("x\t\t\ty\t\t\tz\t\t\tVx\t\t\tVy\t\t\tVz\r")
		for j in range(0,len(writeData[i])):
			out.write(str(writeData[i][j]))
			out.write("\r")
		out.close()
	
