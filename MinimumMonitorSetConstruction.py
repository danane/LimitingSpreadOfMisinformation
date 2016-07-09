#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import random
import operator
import sys
from utility import *

def N_delta(G,sup_source):
	N = set()
	for neigh in G.neighbors(sup_source):
		if neigh != sup_source:
			N.add(neigh)
	return N

def N_delta2(G,sup_source):
	s = set()
	for neigh in G.neighbors(sup_source):
		s.add(neigh)
		for nn in G.neighbors(neigh):
			s.add(nn)
	s.discard(sup_source)
	return s

def bfs_lab(G,src):
	queue = [src]

	distance = dict()
	for i in G.nodes():
		distance[i] = -1

	distance[src] = 0
	while queue!=[]:
		c = queue.pop(0)
		for i in G.neighbors(c):
			if distance[i]==-1:
				queue.append(i)
				distance[i]=distance[c]+1
	return distance


def comp_mis_prob_from_C(graph,C,dst):
	prod_ext = 1
	for j in range(1,dst+1):
		prod_int = 1
		for (u,v) in C[j]:
			prod_int = prod_int*(1-graph[u][v]['capacity'])
		prod_ext = prod_ext*(1-prod_int)
	return prod_ext

def mis_det_prob(graph,src,trg,conn):
	bfs_curr = bfs_lab(graph,src)

	if bfs_curr[trg]==-1:
		return 0

	dst = bfs_curr[trg]

	at_distance = dict()

	for u in bfs_curr.keys():
		ht = bfs_curr[u]
		if ht in at_distance:
			at_distance[ht].append(u)
		else:
			if ht != -1:
				at_distance[ht] = [u]

	C = dict()
	for j in range(1,dst+1):
		C[j] = []
		for u in at_distance[j-1]:
			for v in graph.neighbors(u):
				if (v,trg) in conn:
					if conn[(v,trg)]!=None:
						C[j].append((u,v))
				else:
					try:
						sp = nx.shortest_path(graph,v, trg)
						conn[(v,trg)]=sp
						C[j].append((u,v))
					except nx.NetworkXNoPath:
						conn[(v,trg)]=None

	m_prob = comp_mis_prob_from_C(graph,C,dst)
	return m_prob

def update_conns(graph,node_selected,conn):
	for (s,t) in conn.keys():
		cst = conn[(s,t)]
		if cst!=None:
			if node_selected in cst:
				del conn[(s,t)]


def MMSC(G,B,delta,tau,o,r,verbose=False):
	conn = dict()
	A = set()
	prob_mis = dict()

	c_s_t = bfs_lab(G,o)
	if c_s_t[r]<delta:
		print "Error target in delta distance"
		raise SystemExit

	tau_A = mis_det_prob(G,o,r,conn)

	while tau_A > tau:
		for i in B:
			p_oi = mis_det_prob(G,o,i,conn)
			p_ir = mis_det_prob(G,i,r,conn)
			prob_mis[i] = p_oi*p_ir

		selected = max(prob_mis.iteritems(), key=operator.itemgetter(1))[0]
		B.remove(selected)

		A.add(selected)
		G.remove_node(selected)

		update_conns(G,selected,conn)

		prob_mis = dict()

		tau_A = mis_det_prob(G,o,r,conn)

	return A