import json, re, time
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content
        
data_ex = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
"Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
"Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
"Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
"Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]
data = readfile("data/d_2023_02.txt")

def day02(data, cubes):
    possible_games = 0
    for line in data:
        possible = True
        game_number, game_data = re.findall("Game ([0-9]*): (.*)", line)[0]
        for color in ["blue", "red", "green"]:
            game_cubes = re.findall(f"([0-9]+)(?= {color})", game_data)
            if max(map(int,game_cubes)) > cubes[color]:
                print("too much", color, " in ", game_data)
                possible = False
        if possible: 
            possible_games += int(game_number)
    return possible_games

democubes = {"red":12, "green":13, "blue":14}
assert day02(data_ex, democubes) == 8
#day02(data, democubes)

def day02_b(data):
    sum_power = 0
    for line in data:
        game_number, game_data = re.findall("Game ([0-9]*): (.*)", line)[0]
        power = 1
        for color in ["blue", "red", "green"]:
            game_cubes = re.findall(f"([0-9]+)(?= {color})", game_data)
            power *= max(map(int,game_cubes))
        sum_power += power
    return sum_power

assert day02_b(data_ex) == 2286
day02_b(data)
