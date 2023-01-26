from sample_madlibs import harrypotter, hungergames, percyjackson
import random

if __name__ == "__main__":
    m = random.choice([harrypotter, hungergames, percyjackson])
    m.madlib()