#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import random
import operator
import sys
from utility import *
from diffusion_models import *
from MinimumMonitorSetConstruction import *
from efficientAlgorithm import eAlgorithm

G_read = read_graph_netx(sys.argv[1])

number_of_sources = int(sys.argv[2])

sources,target = select_ss_r(G_read,number_of_sources)
print "Number of Sources =",len(sources)
print "SOURCES =",sources
print "TARGET =",target

G_contracted = contractGraph(G_read,sources)

G_m_test_contracted = G_contracted.copy()

n_d = N_delta(G_contracted,'super')
delta=1

B = set(n_d)
m1 = MMSC(G_contracted,B,delta,0.1,'super',target,verbose=True)
print "\nMMSC\nMonitor set =",m1,"\nNumber of monitors =",len(m1)
print "Num vicini delta =",delta,",",len(n_d)

G_cascade = G_m_test_contracted.copy()
total_nodes = 0
for x in range(100):
	ic = independent_cascade(G_cascade,['super'],m1)
	Infected_set = set()
	for sublist in ic:
		Infected_set = Infected_set.union(sublist)
	total_nodes+=len(Infected_set)
c_nodes = total_nodes/100

print "\nAVG 100 CASCADE: Number of Infected = [",c_nodes,"]\n"

m2,inf = eAlgorithm(G_m_test_contracted,target,c_nodes)
print "\nALGO\nMonitor set =",m2,"\nNumber of monitors =",len(m2)
print "Max number of infected nodes =",inf