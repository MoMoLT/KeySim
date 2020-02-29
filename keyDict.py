def readFile(filename):
    with open(filename, 'r') as f:
        for key in f.readlines():
            key = key.strip()
            yield key

def getDict():
    return dict(zip(readFile('./资源/KeyName.txt'), readFile('./资源/KeyId.txt')))

if __name__ == '__main__':
    a = getDict()
    print(a)
    
    
