import re
import sys

# TODO(Connor) Merge small blocks upwards

def clean(name):
    name = name.upper()
    name = re.sub(r'[^A-Z]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'\b(\w)\w*\b', '\\1', name)
    
    parts = sorted(name.split(' '))
    return ''.join(parts)

def makeAuthorBlocks(path):
    with open(path, "r") as file:
        for line in file:
            id, name = line.strip().split("\t")
            print("%s\t%s" % (id, clean(name)))

if __name__ == '__main__':
    # TODO(Connor) Add error checking
    path = sys.argv[1]
    makeAuthorBlocks(path)
