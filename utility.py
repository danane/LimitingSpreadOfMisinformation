#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
from networkx import *
from collections import deque
import sys
import operator
import random

def read_graph_netx(nomefile):
	graph=nx.read_edgelist(nomefile,create_using=nx.DiGraph())
	for (u,v) in graph.edges():
		graph[u][v]['capacity'] = random.random()
	return graph

def contractGraph(graph,nodes):
	super_out = dict()
	super_in = dict()
	in_edges = []
	out_edges = []

	for x in nodes:
		for out_node in graph.neighbors(x):
			if out_node not in nodes:
				out_edges.append((out_node,graph[x][out_node]['capacity']))

		for in_node in graph.predecessors(x):
			if in_node not in nodes:
				in_edges.append((in_node,graph[in_node][x]['capacity']))


	for rem_node in nodes:
		graph.remove_node(rem_node)

	for (node,cap) in out_edges:
		if node in super_out.keys():
			super_out[node].append((node,cap))
		else:
			super_out[node] = [(node,cap)]

	for (node,cap) in in_edges:
		if node in super_in.keys():
			super_in[node].append((node,cap))
		else:
			super_in[node] = [(node,cap)]


	for key in super_out.keys():
		if len(super_out[key])>1:
			prod = 1
			for (u,c) in super_out[key]:
				prod = prod*(1-c)
			newcap = 1-prod
			graph.add_edge('super',key,capacity=newcap)
		else:
			graph.add_edge('super',key,capacity=super_out[key][0][1])

	for key in super_in.keys():
		if len(super_in[key])>1:
			prod = 1
			for (u,c) in super_in[key]:
				prod = prod*(1-c)
			newcap = 1-prod
			graph.add_edge(key,'super',capacity=newcap)
		else:
			graph.add_edge(key,'super',capacity=super_in[key][0][1])

	return graph



def select_ss_r(G,ns):
	in_degree = dict()

	for x in G.nodes():
		in_degree[x] = len(G.predecessors(x))

	avg_in_l = list(in_degree.values())
	avg_in_value = sum(avg_in_l)/len(avg_in_l)

	out_degree = dict()
	for x in G.nodes():
		out_degree[x] = len(G.neighbors(x))

	avg_out_l = list(out_degree.values())
	avg_out_value = sum(avg_out_l)/len(avg_out_l)

	deg = dict()
	for x in G.nodes():
		deg[x] = in_degree[x]+out_degree[x]

	sorted_in = sorted(deg.items(), key=operator.itemgetter(1),reverse=True)

	PS = set()

	si = sorted_in[:ns]

	for c in si:
		for pred in G.predecessors(c[0]):
			if out_degree[pred]<avg_out_value:
				PS.add(pred)

	PLID = set()


	for key in in_degree.keys():
		if in_degree[key]>0 and in_degree[key]<avg_in_value:
			PLID.add(key)

	sources = random.sample(PS,ns)
	target = random.choice(list(PLID))

	return sources,target