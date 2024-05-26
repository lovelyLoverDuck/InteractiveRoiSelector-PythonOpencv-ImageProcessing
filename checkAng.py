import math


def angle(a, b, c):
    abVector = (a[0] - b[0], a[1] - b[1])
    bcVector = (c[0] - b[0], c[1] - b[1])
    abAngle = math.atan2(abVector[1], abVector[0])
    bcAngle = math.atan2(bcVector[1], bcVector[0])
    radian = bcAngle - abAngle

    if radian < 0:
        radian += 2 * math.pi
    degree = math.degrees(radian)

    return degree


r = [(100, 300), (200, 200), (100, 100)]

angleResult = angle(r[0], r[1], r[2])

print("점 b의 우측 각도 :", 360 - angleResult)
