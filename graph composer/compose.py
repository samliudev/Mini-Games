import os
import re
import string
import random

from graph import Graph, Vertex

def get_words_from_text(text_path):
    with open(text_path, 'rb') as f:
        text = f.read().decode('utf-8')

        # remove [text in here]
        text = re.sub(r'\[(.+)\]', ' ', text) # if one or more character in brackets, replace with space

        text = ' '.join(text.split()) # this is saying turn whitespace into just spaces
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation)) # replaces all punctuation with empty space
    
    words = text.split()
    return words

def make_graph(words):
    g = Graph()
    previous_word = None

    # for each word, check that word is in the graph, if not then add it
    for word in words:
        word_vertex = g.get_vertex(word)
    # if there was a previous word, then add an edge if it does not already exist
        if previous_word:
            previous_word.increment_edge(word_vertex)
    # otherwise increment weight by 1
    # set our word to the previous word and iterate
        previous_word = word_vertex

    # remember that we want to generate the probability mappings before composing
    # this is a great place to do it before we return the graph object
    g.generate_probability_mappings()
    
    return g

def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words)) # pick a random word to start
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition

def main(artist):
    # 1: get words from text
    # words = get_words_from_text('texts/hp_sorcerer_stone.txt')
    
    # for song lyrics
    words = []
    for song_file in os.listdir(f'songs/{artist}'):
        if song_file == '.DS_Store':
            continue
        song_words = get_words_from_text(f'songs/{artist}/{song_file}')
        words.extend(song_words)

    # 2: make a graph using those words
    g = make_graph(words)
    # 3: get the next word for x number of words (defined by user)
    # 4: show the user
    composition = compose(g, words, 100)
    return ' '.join(composition) # returns a string with words separated by spaces

if __name__ == '__main__':
    print(main('taylor_swift'))