import json
from os.path import isfile

def save(dict_): # saves the dictionary
    with open("33c.json", "w") as f: json.dump(dict_, f)

def load(): # loads json file into memory as dictonary
    if isfile("3cc.json"):
        with open("3cc.json", "r") as f: r=json.loads(f.read())

        # loads numerical keys as integers and not strings
        dict_={int(i):r[i] for i in r if i.isdigit()}
        for i in r:
            if not i.isdigit(): dict_[i]=r[i]
        return dict_

    else:
        raise FileNotFoundError("Make sure there is a file called \"3cc.json\" and it contains at least \"\{\}\"")

# debugging and testing
if __name__=="__main__":
    pass