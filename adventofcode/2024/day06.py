import utils, re

data_ex = ["....#.....",
".........#",
"..........",
"..#.......",
".......#..",
"..........",
".#..^.....",
"........#.",
"#.........",
"......#...",
]
data = utils.readfile("data/day06.txt")

class Xmap:
    xmap={}
    max_x=0
    max_y=0
    cur_k = 0

    def __init__(self, data):
        xmap = self.init_map(data)

    @staticmethod
    def xy2k(x,y) -> str:
        return f'{x}.{y}'
    
    @staticmethod
    def k2xy(k) -> tuple[int, int]:
        return tuple(map(int, k.split('.')))

    def init_map(self,data):
        self.max_y = len(data)
        self.max_x = len(data[0])
        for y,line in enumerate(data):
            for x, letter in enumerate(line):
                self.set(x,y,letter)
                if letter in ["v",">","^","<"]:
                    self.cur_k = self.xy2k(x,y)
    
    def set(self,x,y, value):
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            return False
        k = self.xy2k(x,y)
        if value == '.':
            if k in self.xmap:
                del self.xmap[k]
        else:
            self.xmap[k] = value
        return True
    
    def get(self, x, y) -> str:
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            return "O"
        k = self.xy2k(x,y)
        if k in self.xmap:
            return self.xmap[k]
        else:
            return "."

    direction = {"v":(0,1),">":(1,0),"^":(0,-1),"<":(-1,0)}
    next = {"v":"<",">":"v","^":">","<":"^"}
    
    def try_move(self):
        x,y = self.cur_pos()
        
        cur_dir = self.get(x,y)
        if cur_dir == "O":
            return False, False
        
        (dx,dy) = self.direction[cur_dir]

        next_move= self.get(x+dx, y+dy)
        if next_move == cur_dir:
            return True, True

        if next_move == "#":
            #print(f"- turn {x}, {y}")
            self.set(x,y, self.next[cur_dir])
            return True, False
        else:
            #print(f"- move {x}, {y}")
            self.set(x+dx, y+dy, cur_dir)
            self.cur_k = self.xy2k(x+dx, y+dy)    
            return True, False

    def cur_pos(self) -> tuple[int, int]:
        return self.k2xy(self.cur_k)
        
    def get_map(self):
        return self.xmap
    
    def simulates(self):
        i = 0
        inside = True
        loop = False
        while inside and not loop:
            i += 1
            if i%100000 == 0:
                print(f"{i} moves {len(self.xmap)}")
            (inside, loop) = self.try_move()
            if i > 500000:
                print("Array size", len(self.xmap), " max x", self.max_x, " max y", self.max_y )
                return True, True
        return inside, loop

    def simulates_loop(self):
        willloop = 0
        inside = True
        basicloop = False
        while inside and not basicloop :
            (inside, basicloop) = self.try_move()
            old_map = dict(self.get_map())
            old_cur_k = self.cur_k

            x,y = self.cur_pos()
            cur_dir = self.get(x,y)
            if cur_dir != "O":
                (dx,dy) = self.direction[cur_dir]
                if self.get(x+dx, y+dy) == "." and self.set(x+dx, y+dy, "#"):
                    print(f"Try {x+dx}, {y+dy}")
                    (_, loop) = self.simulates()
                    if loop :
                        print(f"# in {x+dx}, {y+dy}")
                        willloop += 1
                    else:
                        print("not loop")

                self.xmap = old_map
                self.cur_k = old_cur_k
        return willloop
            




assert Xmap.xy2k(1,2) == "1.2"
print(Xmap.k2xy("1.2"))
assert Xmap.k2xy("1.2") == (1, 2)
assert Xmap(["..",".X"]).get_map() == {"1.1":"X"}
    
def day06(data):
    xmap = Xmap(data)
    xmap.simulates()
    a = [ 1 if l in ["v",">","^","<"] else 0 for l in xmap.get_map().values() ]
    #print(sum(a))
    return sum(a)

#assert day06(data_ex) == 41

#print(day06(data))

def day06b(data):
    xmap = Xmap(data)
    loops = xmap.simulates_loop()
    return loops

assert day06b(data_ex) == 6
print(day06b(data))

#1975, 1976 too high 