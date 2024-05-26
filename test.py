import numpy as np
import cv2
import math

# NULL 모드에서 PASS(작동없음)


def nullMouse(event, x, y, flags, param):
    pass

# 타원 모드에서 타원 그리기 마우스 설정


def ellipseMouse(event, x, y, flags, param):
    global title, pt
    global firstX, firstY
    global click, image, cnt
    cv2.putText(image, "Ellipse", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

    if event == cv2.EVENT_LBUTTONDOWN:
        # 마우스 좌측 버튼 클릭한 경우만 타원이 그려지도록 click을 true로 설정
        click = True
        firstX = x
        firstY = y

    elif event == cv2.EVENT_MOUSEMOVE and click:
        image = cv2.imread("input.jpg", cv2.IMREAD_COLOR)
        cv2.putText(image, "Ellipse", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
        # 타원 그리기 준비
        pt1 = (int((x-firstX)/2), int((y - firstY)/2))
        center = (firstX + pt1[0], firstY + pt1[1])
        axes = (abs(pt1[0]), abs(pt1[1]))
        # 타원 그리기
        cv2.ellipse(image, center, axes, 0, 0, 360, red, 2, cv2.LINE_AA)
        cv2.imshow(title, image)

    elif event == cv2.EVENT_LBUTTONUP:
        # click을 False로 변경함으로 타원 하나를 생성의 끝을 나타냄.
        click = False
        # 타원 그리기 준비
        pt1 = (int((x-firstX) / 2), int((y - firstY)/2))
        center = (firstX + pt1[0], firstY + pt1[1])
        axes = (abs(pt1[0]), abs(pt1[1]))
        # 타원 그리기
        cv2.ellipse(image, center, axes, 0, 0, 360, red, 2, cv2.LINE_AA)
        # mask - image 크기의 영으로 채워진 mask 생성
        mask = np.zeros_like(image)
        cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)
        ellipse_zone = cv2.bitwise_and(original_image, mask)
        # 지정된 형식에 맞게 타원 사진 저장
        cv2.imwrite('./bdc' + str(cnt).zfill(4) + '.jpg', ellipse_zone)
        cnt += 1
        cv2.imshow(title, image)

# 각도 구하기 - def angle(첫 번째 점, 두 번째(기준점), 마지막 점)


def angle(a, b, c):
    abVector = (a[0] - b[0], a[1] - b[1])
    bcVector = (c[0] - b[0], c[1] - b[1])
    abAngle = math.atan2(abVector[1], abVector[0])
    bcAngle = math.atan2(bcVector[1], bcVector[0])
    radian = bcAngle - abAngle

    if radian < 0:
        radian += 2 * math.pi
    degree = math.degrees(radian)

    return 360 - degree

# 다각형 모드에서 다각형 그리기 마우스 설정


def polygonMouse(event, x, y, flags, param):
    global title, pt
    global lastX, lastY
    global click, image, cnt, firstX, firstY, radius, polyLists, original_image

    radius = 20

    if event == cv2.EVENT_LBUTTONDOWN:
        # 찍은 점이 하나도 없는 경우 / 첫번 째 점 찍기
        if (len(polyLists) == 0):
            cv2.circle(image, (x, y), 1, red, 5)
            polyLists.append((x, y))
            cv2.imshow(title, image)
        # 찍은 점이 하나있는 경우
        elif (len(polyLists) == 1):
            cv2.circle(image, (x, y), 1, red, 5)
            polyLists.append((x, y))
            lastX, lastY = polyLists[0]
            cv2.line(image, (x, y), (lastX, lastY),  red, 5, cv2.LINE_AA)
            cv2.imshow(title, image)
        # 찍은 점이 두개 있고 다음 하나의 점을 찍어 각도가 필요한 경우
        elif (len(polyLists) >= 2):
            nowXY = (x, y)
            if (angle(polyLists[-2],  nowXY, polyLists[-1]) >= 180):
                pass
            else:
                cv2.circle(image, (x, y), 1, red, 5)
                polyLists.append((x, y))
                cv2.line(image, (x, y), polyLists[-2],  red, 5, cv2.LINE_AA)
                cv2.imshow(title, image)

        # 처음 점과 마지막 점 연결 마무리 세팅
        firstX, firstY = polyLists[0]
        a = firstX - x
        b = firstY - y
        c = math.sqrt((a * a) + (b * b))

        # 마지막 점이 처음 점 일정 범위 내에 들어오면 자동완성
        if c <= radius and len(polyLists) > 3:
            # 마지막 점을 처음 점으로 변경
            polyLists[-1] = polyLists[0]
            # 리스트를 넘파이
            numpy_arr = np.array(polyLists)
            # 주어진 점으로 다각형 그리기
            image = cv2.fillConvexPoly(
                image, numpy_arr, (255, 255, 255), lineType=cv2.LINE_AA)
            # mask - image 크기의 영으로 채워진 mask 생성
            mask = np.zeros_like(image)
            cv2.fillConvexPoly(
                mask, numpy_arr, (255, 255, 255), lineType=cv2.LINE_AA)
            poly_zone = cv2.bitwise_and(original_image, mask)
            # 지정된 형식에 맞게 타원 사진 저장
            cv2.imwrite('./bdc' + str(cnt).zfill(4) + '.jpg', poly_zone)
            cnt += 1
            polyLists.clear()
            # 첫 번째 점을 찍을 때 원본 이미지로 복원
            cv2.imshow(title, image)
            image = original_image.copy()

            cv2.putText(image, "Polygon", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)


image = cv2.imread("input.jpg", cv2.IMREAD_COLOR)
original_image = image.copy()
pt = (-1, -1)
red = (0, 0, 255)
title = "Draw"
cnt = 1
polyLists = []
cv2.namedWindow(title)
# 초기 NULL 모드 글자 삽입
cv2.putText(image, "NULL", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
cv2.imshow(title, image)

# 키보드 1과 2의 버튼으로 모드 변경을 위한 플래그 설정
ellipseTF = False
polygonTF = False

click = False

while True:

    key = cv2.waitKey(0) & 0xFF
    if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
        break

    # 키보드 1 입력 시
    if key == 49:
        # 타원 --> NULL
        if ellipseTF and polygonTF == False:
            ellipseTF = False
        # 다각형 --> 타원
        elif ellipseTF == False and polygonTF:
            ellipseTF = True
            polygonTF = False
        # NULL --> 타원
        elif ellipseTF == False and polygonTF == False:
            ellipseTF = True
    # 키보드 2 입력시
    if key == 50:
        # 다각형 --> NULL
        if polygonTF and ellipseTF == False:
            polygonTF = False
        # 타원 --> 다각형
        elif polygonTF == False and ellipseTF:
            polygonTF = True
            ellipseTF = False
        # NULL - > 다각형
        elif ellipseTF == False and polygonTF == False:
            polygonTF = True

    # NULL 모드 진입
    if ellipseTF == False and polygonTF == False:
        polyLists.clear()
        image = original_image.copy()
        cv2.putText(image, "NULL", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
        cv2.setMouseCallback(title, nullMouse)
        # cv2.imshow(title, image)
    # 타원 모드 진입
    elif ellipseTF:
        polyLists.clear()
        image = original_image.copy()
        cv2.putText(image, "Ellipse", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
        cv2.setMouseCallback(title, ellipseMouse)
    # 다각형 모드 진입
    elif polygonTF:
        image = original_image.copy()
        cv2.putText(image, "Polygon", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
        cv2.setMouseCallback(title, polygonMouse)
    cv2.imshow(title, image)

cv2.destroyAllWindows()
