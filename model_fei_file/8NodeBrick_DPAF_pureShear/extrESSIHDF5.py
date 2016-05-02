#!/usr/bin/python
import h5py
import matplotlib.pylab as plt
import sys
import numpy as np
file1name=sys.argv[1]
file2name=sys.argv[2]
# for thefile in files:
# finput = h5py.File(thefile)


# Read from initial state
file1 = h5py.File(file1name)
totalstrain0 = file1["/Model/Elements/Outputs"][0:6,-2]
plaststrain0 = file1["/Model/Elements/Outputs"][6:12,-2]
stress0 = file1["/Model/Elements/Outputs"][12:18,-2]

# Read from the shear loading
file2 = h5py.File(file2name)
times = file2["time"][:]
totalstrain = file2["/Model/Elements/Outputs"][0:6,:-1]
plaststrain = file2["/Model/Elements/Outputs"][6:12,:-1]
stress = file2["/Model/Elements/Outputs"][12:18,:-1]
num_loadstep=totalstrain.shape[1]
tstrain=np.zeros((6,num_loadstep+1))
pstrain=np.zeros((6,num_loadstep+1))
tstress=np.zeros((6,num_loadstep+1))
dtstrain=np.zeros((6,num_loadstep))
dpstrain=np.zeros((6,num_loadstep))
dtstress=np.zeros((6,num_loadstep))
for x in xrange(0,6):
	tstrain[x]=np.insert(totalstrain[x],0,totalstrain0[x])
	pstrain[x]=np.insert(plaststrain[x],0,plaststrain0[x])
	tstress[x]=np.insert(stress[x],0,stress0[x])

# tau_plot=abs(tstress[0,:]-tstress[1,:])/2
# tstrain_plot=abs(tstrain[0,:]-tstrain[1,:])/2
tau_plot=(tstress[0,:]-tstress[1,:])/2
tstrain_plot=(tstrain[0,:]-tstrain[1,:])/2

mytau=np.delete(tau_plot,0)
mystrain=np.delete(tstrain_plot,0)

# Plot the stress-strain figure. Add labels and titles.
plt.figure()
plt.plot(mystrain,mytau)
plt.grid()
plt.xlabel("Strain ")
plt.ylabel("Stress ")
plt.savefig("stress-strain.pdf",  bbox_inches='tight')
plt.show()


# plot the G/Gmax
# extract the up part only
upsize=0
while 1:
	s1=tau_plot[upsize]
	s2=tau_plot[upsize+1]
	# s3=tau_plot[upsize+2]
	upsize=upsize+1
	if s2<s1:
		break

# num_step=len(d_tstrain)
theG=np.zeros(upsize)
GGmax=np.zeros(upsize)
for x in xrange(0,upsize):
	theG[x]=mytau[x]/mystrain[x]

Gmax=theG[0]

for x in xrange(0,upsize):
	GGmax[x]=theG[x]/Gmax


# mystrain=np.delete(tstrain_plot,0)
plt.figure()
plt.semilogx(mystrain[:upsize] ,GGmax)
plt.grid()
plt.xlabel("Strain ")
plt.ylabel("G/Gmax ")
plt.savefig("G-Gmax.pdf",  bbox_inches='tight')
plt.show()












# --------------------------------------------
# backup
# --------------------------------------------
# disp0 = file2["/Model/Elements/Generalized_Displacements"][8,:-1]

# Configure the figure filename, according to the input filename.
# outfig=file2name.replace("_","-")
# outfigname=outfig.replace("h5.feioutput","pdf")





# calculate strain and stress increment first
# for x in xrange(0,num_loadstep):
# 	dtstress[:,x]=tstress[:,x+1]-tstress[:,x]
# 	dtstrain[:,x]=tstrain[:,x+1]-tstrain[:,x]
# 	dpstrain[:,x]=pstrain[:,x+1]-pstrain[:,x]


# d_tau=abs(dtstress[0,:]-dtstress[1,:])/2
# d_tstrain=abs(dtstrain[0,:]-dtstrain[1,:])/2
# d_pstrain=abs(dpstrain[0,:]-dpstrain[1,:])/2
# d_tau=(dtstress[0,:]-dtstress[1,:])/2
# d_tstrain=(dtstrain[0,:]-dtstrain[1,:])/2
# d_pstrain=(dpstrain[0,:]-dpstrain[1,:])/2