

class Plane:

    def __init__(self,size):
        self.field = bytes(size**2)




if __name__ == '__main__':
    a = Plane(16)
    print(len(a.field))