import math

class Tetrahedron:
    s_8_9, s_2_9, s_2_3 = math.sqrt(8/9), math.sqrt(2/9), math.sqrt(2/3)
    vertices =  [(0,0,1), (s_8_9,0,-1/3), (-s_2_9,s_2_3,-1/3), (-s_2_9,-s_2_3,-1/3)]
    faces = [[0,1,2], [0,2,3], [0,3,1], [1,3,2]]

class Hexahedron:
    s_1_3 = 1/math.sqrt(3)
    vertices = [
        (-s_1_3,-s_1_3,-s_1_3), (s_1_3,-s_1_3,-s_1_3), (s_1_3, s_1_3,-s_1_3), (-s_1_3, s_1_3,-s_1_3), 
        (-s_1_3,-s_1_3, s_1_3), (s_1_3,-s_1_3, s_1_3), (s_1_3, s_1_3, s_1_3), (-s_1_3, s_1_3, s_1_3)]
    faces = [[0,1,2,3], [1,5,6,2], [5,4,7,6], [4,0,3,7], [3,2,6,7], [1,0,4,5]]

class Octahedron:
    vertices = [(-1,0,0), (0,-1,0), (0,0,-1), (1,0,0), (0,1,0), (0,0,1)]
    faces = [[0,2,1], [1,2,3], [3,2,4], [4,2,0], [0,1,5], [1,3,5], [3,4,5], [4,0,5]]

class Dodecahedron:
    phi = (1 + math.sqrt(5)) / 2 # φ=(1+√5)/2 is the Golden Ratio.
    a, b, c = 1, 1/phi, 1/(phi*phi)
    vertices = [
        (-b,-b,-b), (b,-b,-b), (b,b,-b), (-b,b,-b), # 0..7: (±φ, ±φ, ±φ)
        (-b,-b,b), (b,-b,b), (b,b,b), (-b,b,b),
        (0,-a,-c), (0,a,-c), (0,a,c), (0,-a,c),     # 8..11: (0, ±φ^2, ±1)
        (-a,-c,0), (a,-c,0), (a,c,0), (-a,c,0),     # 12..15: (±φ^2, ±1, 0)
        (-c,0,-a), (c,0,-a), (c,0,a), (-c,0,a)]     # 16..19: (±1, 0, ±φ^2)
    faces = [
        [16,17,1,8,0], [17,16,3,9,2], [19,18,6,10,7], [18,19,4,11,5],
        [14,13,1,17,2], [13,14,6,18,5], [15,12,4,19,7], [12,15,3,16,0],
        [9,10,6,14,2], [10,9,3,15,7], [8,11,4,12,0], [11,8,1,13,5]]

class Icosahedron:
    vertices = [
        (0,0,1), (0.894,0,0.447), (0.276,0.851,0.447), (-0.724,0.526,0.447), (-0.724,-0.526,0.447), (0.276,-0.851,0.447),
        (0.724,0.526,-0.447), (-0.276,0.851,-0.447), (-0.894,0,-0.447), (-0.276,-0.851,-0.447), (0.724,-0.526,-0.447), (0,0,-1)]
    faces = [
        [1,2,0], [2,3,0], [3,4,0], [4,5,0], [5,1,0], [7,6,11], [8,7,11], [9,8,11], [10,9,11], [6,10,11],
        [1,6,2], [2,7,3], [3,8,4], [4,9,5], [5,10,1], [7,2,6], [8,3,7], [9,4,8], [10,5,9],  [6,1,10]]
