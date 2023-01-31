# Markov Chain representation
import random

# Define the graph in terms of vertices

class Vertex(object):
    def __init__(self, value): # value willl be the word
        self.value = value
        self.adjacent = {} # dict with nodes that have an edge from this vertex
        self.neighbors = []
        self.neighbors_weights = []

    def add_edge_to(self, vertex, weight=0):
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1  # if exists in dict, add 1 otherwise set to 0 + 1 

    # initializes probability map
    def get_probability_map(self):
        for (vertex, weight) in self.adjacent.items():
            self.neighbors.append(vertex)
            self.neighbors_weights.append(weight)
            

    def next_word(self):
        # randomly select next word based on weights
        return random.choices(self.neighbors, weights=self.neighbors_weights)[0]

class Graph(object):
    def __init__(self):
        self.vertices = {}

    def get_vertex_values(self):
        # what are the values of all the vertices?
        # in other words, return all possible words
        return set(self.vertices.keys())

    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    def get_vertex(self, value):
        # if value isn't in the graph
        if value not in self.vertices:
            self.add_vertex(value)
        return self.vertices[value] # get the Vertex object

    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()
        

    def generate_probability_mappings(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()