import utils, sys, re
import functools


data_ex=[
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k"
]
data = utils.readfile("data/d07.txt")
print(data_ex)        
        
def cmd_cd(path, newpath):
    if newpath == "/":
        path = "/"
    elif newpath == "..":
        path = "/".join(path.split("/")[:-2])+"/"
    else:
        path += newpath + "/"    
    return path
    
assert cmd_cd("/", "a") == "/a/"
assert cmd_cd("/a/b/c/", "..") == "/a/b/"

def size_dir(path, files):
    res = ([int(size) for name,size in files.items() if name.startswith(path)])
    #print(res)
    return sum(res)


exemple = {"/a/e": 12, "/a/f": 13, "/a/b/c": 10, "/b/e":5}
assert size_dir("/", exemple) == 40
assert size_dir("/a/", exemple) == 35
assert size_dir("/a/b/", exemple) == 10

    
def d070(data, n=14):
    curpath = "/"
    files = {}
    for line in data:
        #print(line)
        pattern_cmd = '\$ ([a-z]*)( [a-z/\.]+)?'
        command = re.findall(pattern_cmd, line)

        pattern_lsdir = 'dir ([a-z]*)'
        lsdir = re.findall(pattern_lsdir, line)

        pattern_lsfile = '^([0-9]*) ([0-9\.a-z]*)'
        lsfile = re.findall(pattern_lsfile, line)

        if command:
            #print("command", command)
            cmd,path = command[0]
            if cmd == 'cd':
                curpath = cmd_cd(curpath, path.strip())
        elif lsdir:
            files[cmd_cd(curpath, lsdir[0])] = 0
        elif lsfile:
            #print("file:", line, lsfile, curpath)
            size,filename = lsfile[0]
            files[curpath + "" + filename] = size
        else:
            print("Unknown", line)
    dirs = {}
    for name, size in files.items():
        if size == 0:
            size = size_dir(name, files)
            dirs[name] = size
       
    #print("END : ", dirs)
    return dirs, files
    
    
dirs_ex, files_ex = d070(data_ex)
dirs, files = d070(data)

# EXO 1
res = [a_size for a_dir, a_size in dirs.items() if a_size <= 100000]
print(sum(res))

# EXO 2

# exemple
total_size_ex = size_dir("/", files_ex)
print(total_size_ex)
left = 70000000-total_size_ex
print(left)
possible = [size for a_dir,size in dirs_ex.items() if size > left]
print("remove", min(possible))

# real data
total_size = size_dir("/", files)
print(total_size)
left = 70000000-total_size
print(left)
needed = 30000000 - left
possible = [size for a_dir,size in dirs.items() if size > needed]
print(possible)
print("remove", min(possible))