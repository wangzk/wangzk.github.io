#!/usr/bin/python3
"""
Calculate symmetry-breaking conditions for a given undirected unlabeled query graph.
Author: Zhaokang Wang
Date: 2021-11-25
Email: wangzhaokang@nuaa.edu.cn
Input: 
  The program receives a single argument which is the file path to the edge list of the query graph. The edge list is a CSV file with the header of "src,dst". Each line in the CSV file is an edge of the query graph. The query graph should be undirected. Each edge should appear only once.
Output: 
  The program outputs the symmetry-breaking conditions generated for the given query graph.
"""

import networkx as nx
import pandas as pd
import sys
import itertools

def load_graph(file_path):
    """Load the query graph from the edge list CSV file."""
    df = pd.read_csv(file_path, header=0)
    G = nx.Graph()
    for i in range(len(df)):
        src = df.iloc[i]['src']
        dst = df.iloc[i]['dst']
        # For each edge, we always store the vertex with smaller IDs as the source vertex in the underlying storage
        G.add_edge(min(src, dst), max(src, dst))
    return G

def get_vertex_permutation_mappings(G:nx.Graph):
    """Get permutation mappings of vertices.

    Calculate all the possible permutations of the vertex set for a given graph.

    Args:
        G: The query graph.

    Returns:
        A list of permutation mappings. Each permutation mapping is a dict with the keys as the original vertex IDs and the values as the mapped vertex IDs under the permutation.
    """
    vertex_list = list(G.nodes())
    perm_mappings = list()
    for perm  in itertools.permutations(vertex_list):
        mapping = dict()
        for i in range(len(vertex_list)):
            mapping[vertex_list[i]] = perm[i]
        perm_mappings.append(mapping)
    return perm_mappings

def get_mapped_graph(G:nx.Graph, mapping:map)->nx.Graph:
    """Get a new graph under a vertex permutation mapping.

    Args:
        G: Original query graph.
        mapping: a dict which maps each vertex IDs to a new vertex ID.

    Returns:
        New graph with the mapped vertex.
    """
    mG = nx.Graph()
    for e in G.edges():
        src = e[0]
        dst = e[1]
        newSrc = min(mapping[src], mapping[dst])
        newDst = max(mapping[src], mapping[dst])
        # We store each edge with the smaller ID as the source vertex.
        mG.add_edge(newSrc, newDst)
    return mG

def is_automorphism(G1:nx.Graph, G2:nx.Graph) -> bool:
    """Judges whether two graph is automorphism. For the same graph under two automorphism mappings, if they are isomorphic to each other, the edge set should be the same.
    """
    g1_edge = set([(min(e[0], e[1]), max(e[0], e[1])) for e in G1.edges()])
    g2_edge = set([(min(e[0], e[1]), max(e[0], e[1])) for e in G2.edges()])
    return g1_edge == g2_edge

def get_automorphisms(G:nx.Graph):
    """Get all the automorphism mappings for a given graph.

    Args:
        G: Undirected query graph.

    Returns:
        a list of automorphism mappings. Each mapping is a dict that maps original vertex IDs to its corresponding IDs.
    """
    perm_mappings = get_vertex_permutation_mappings(G)
    automorphisms = list()
    for p in perm_mappings:
        mG = get_mapped_graph(G, p)
        if is_automorphism(G, mG):
            automorphisms.append(p)
    return automorphisms
    
def union_find(lis):
    """Use union-find set to find equivalence classes.

    Args:
        lis: a list of equivalent relations. Each element in the list is a tuple with two vertex IDs. The tuple indicates that the two vertices are in the same equivalence class.
    
    Returns:
        A list of equivalent classes. Each element in the list is another list. Each element stores the vertex IDs in the same equivalent class.
    """
    lis = map(set, lis)
    unions = []
    for item in lis:
        temp = []
        for s in unions:
            if not s.isdisjoint(item):
                item = s.union(item)
            else:
                temp.append(s)
        temp.append(item)
        unions = temp
    return unions

def calc_orbits(automorphisms:list) -> list:
    """Calculate all the orbits for a group of automorphisms.
    
    Args:
        automorphisms: a list of automorphisms. Each element is a dict representing the automorphism mapping.

    Returns:
        A list of orbits. Each list is a set of vertices in the same orbit.
    """
    equivalent_relations = set()
    for vid in automorphisms[0].keys():
        for a in automorphisms:
            equivalent_relations.add((vid, a[vid]))
    orbits = union_find(equivalent_relations)
    return orbits

def get_symmetry_breaking_conditions_for_largest_orbit(automorphisms:list):
    """Calculate the symmetry-breaking conditions for the largest orbit.

    Args:
        automorphisms: the automorphisms under consideration

    Returns:
        conditions: The symmetry-breaking conditions added for the largest orbit in the current automorphisms.
        automorphisms: The updated automorphisms by filtering out the mappings related to the largest orbit.
    """
    orbits = calc_orbits(automorphisms)
    max_orbit_len = len(max(orbits, key=lambda s: len(s)))
    orbits_to_eliminate = list(filter(lambda s: len(s) == max_orbit_len, orbits))
    orbit_to_eliminate = min(orbits_to_eliminate, key=lambda s: min(s))
    core_vertex = min(orbit_to_eliminate)
    other_vertices = orbit_to_eliminate - {core_vertex}
    conditions = list()
    for v in other_vertices:
        conditions.append((core_vertex, v))
    automorphisms = list(filter(lambda m: m[core_vertex] == core_vertex, automorphisms))
    return conditions, automorphisms

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage: path_to_csv_edge_list_file")
        exit(1)
    g = load_graph(sys.argv[1])
    # calculate all the automorphisms in the query graph
    automorphisms = get_automorphisms(g)
    print("Number of automorphisms in the given query graph:", len(automorphisms))
    symmetry_breaking_conditions = list()
    while (len(automorphisms) > 1):
        new_conditions, new_auto = get_symmetry_breaking_conditions_for_largest_orbit( automorphisms)
        symmetry_breaking_conditions = symmetry_breaking_conditions + new_conditions
        automorphisms = new_auto
    print("Symmetry-breaking conditions of the query graph:")
    for cond in symmetry_breaking_conditions:
        print("v{} < v{}".format(cond[0], cond[1]))
    exit(0)