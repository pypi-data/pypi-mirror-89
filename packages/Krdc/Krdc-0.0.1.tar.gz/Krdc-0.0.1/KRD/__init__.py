class VBlock:
    def __init__(self, name):
        self.name = name
    def get_name(self):
        for input in input(name):
            print(f"you called {name}!")
        input("call namee: ")
     
if __name__ == '__main__':
    lab = VBlock("hiwa")
    a = input("enter hiwa: ")
    if a == lab.name:
        print(f"you called {lab.name}!")
