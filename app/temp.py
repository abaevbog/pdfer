import math
# 1-1-5 {--4 if sqFt < 1000 else math.floor( (sqFt + 125) / 250) --} 800 -> 4; 1200 -> 4; 1300 -> 5; 1400 -> 5; 1600 -> 6 
# cable: {--1 if sqFt < 1000 else math.ceil(sqFt / 1000) --} | 800 -> 1; 1300 -> 2; 1700 -> 2; 2300 -> 3
# lights: {-- math.ceil(sqFt / 50) --} | 30 -> 0; 80 -> 1; 120 -> 2

def x(sqFt):
    return 4 if sqFt < 1000 else math.floor( (sqFt + 125) / 250)

print(x(1650))