def ground_collision(P1, ground):
    x, y, z = P1.pos
    if y < ground.pos[1]:
        P1.velocity = [0.0, 0.0, 0.0]
        y = ground.pos[1]
        P1.s = [x, y, z]
        P1.pos = [x, y, z]

def collision(P1, P2):
    if P1.collision is True and P2.collision is True:
        x1, y1, z1 = P1.pos
        x2, y2, z2 = P2.pos
        X1, Y1, Z1 = x1 + P1.size, y1 + P1.size, z1 + P1.size
        X2, Y2, Z2 = x2 + P2.size, y2 + P2.size, z2 + P2.size

        if y1 >= y2 and y1 <= Y2:
            if x1 <= x2 and X1 >= x2:
                y1 = Y2
                P1.velocity = [0.0, 0.0, 0.0]
                P1.pos[1] = y1