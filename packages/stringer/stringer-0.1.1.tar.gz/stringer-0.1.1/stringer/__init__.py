def swapletter(string):
        a = 0
        n_string = ""
        for i in string:
            if a%2!=0:
                n_string = n_string + i.upper()
            else :
                n_string = n_string + i.lower()
            a+=1
        return n_string

def swapcase(string):
    new = ""
    for i in string:
        if i.isupper():
            new = new + i.lower()
        else:
            new = new + i.upper()
    return new

def capital(string):
    new = ""
    for i in string:
        new = new + i.upper()
    return new

def lower(string):
    new = ""
    for i in string:
        new = new + i.lower()
    return new


if __name__ == "__main__":
    print(swapletter("passion"))
    print(swapcase('passion'))
    print(capital("passion"))
    print(lower("PASSION"))
