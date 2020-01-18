

def ground_collision(P1, ground):
    x, y, z = P1.pos
    if y <= ground.pos[1]:
        P1.velocity = [0.0, 0.0, 0.0]
        y = ground.pos[1]
        P1.pos = [x, y, z]

def collision(P1, P2):
    if P1.collision is True and P2.collision is True:
        x1, y1, z1 = P1.pos
        x2, y2, z2 = P2.pos
        X1, Y1, Z1 = x1 + P1.size, y1 + P1.size, z1 + P1.size
        X2, Y2, Z2 = x2 + P2.size, y2 + P2.size, z2 + P2.size

        if y1 > y2 and y1 <= Y2:
            if (x1 <= x2 and X1 >= x2) or (x1 >= x2 and x1 <= X2):
                if (z1 <= z2 and Z1 >= z2) or (z1 >= z2 and z1 <= Z2):
                    P1.velocity = [0.0, 0.0, 0.0]
                    P1.pos[1] = Y2
        else:
            if (Z1 >= z2 and Z1 <= Z2) or (z1 <= Z2 and z1 >= z2):
                if (x1 < x2 and X1 > x2):
                    P1.hvel = [0.0, 0.0, 0.0]
                    P2.hvel = [0.0, 0.0, 0.0]
                    P1.haccel = [0.0, 0.0, 0.0]
                    P2.haccel = [0.0, 0.0, 0.0]
                if (x1 < X2 and X1 > X2):
                    P1.hvel = [0.0, 0.0, 0.0]
                    P2.hvel = [0.0, 0.0, 0.0]
                    P1.haccel = [0.0, 0.0, 0.0]
                    P2.haccel = [0.0, 0.0, 0.0]

