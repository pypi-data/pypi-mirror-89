import cv2
import numpy as np

# # 读取名称为 p6.png的图片
# img = cv2.imread("./img.jpg", 1)
# # img=img[100:500,100:400]
# cv2.imshow('origin', img)
# # cv2.imshow('dist',dist)
# # 灰度
# img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# top = int(0.05 * img.shape[0])  # shape[0] = rows
# bottom = top
# left = int(0.04 * img.shape[1])  # shape[1] = cols
# right = left
# value = [255, 255, 255]
# borderType = cv2.BORDER_CONSTANT
# img = cv2.copyMakeBorder(img, top, bottom, left,
#                          right, borderType, None, value)

# # # 高斯模糊
# img = cv2.GaussianBlur(img, (3, 3), 0)
# # retval, img = cv2.threshold( img, 150, 255,cv2.THRESH_BINARY )
# cv2.imshow('GaussianBlur', img)

# # # Canny提取边缘
# processed = cv2.Canny(img, 30, 100, 1)

# cv2.imshow('Canny', processed)

# image, contours, hierarchy = cv2.findContours(
#     processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # 显示原图和处理后的图像
# cv2.imshow("findContours", image)

# maxAreas = filter(lambda cons: cv2.contourArea(cons) > 2500, contours)

# # print(maxAreas)

# rects = list(map(lambda area: cv2.minAreaRect(area), maxAreas))

# print('rects')
# print(rects)

# boxs = list(map(lambda rect: np.int0(cv2.boxPoints(rect)), rects))

# # for rect in rects:
# #     # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
# #     box = cv2.boxPoints(rect)
# #     box = np.int0(box)
# #     boxs.append(box)
# print('boxs')
# print(boxs)

# cv2.imshow("rect", img)

# # 创建白色幕布
# # temp = np.ones(processed.shape,np.uint8)*255
# # 画出轮廓：temp是白色幕布，contours是轮廓，-1表示全画，然后是颜色，厚度
# temp = cv2.drawContours(img.copy(), boxs, -1, (0, 0, 255), 1)

# cv2.imshow("contours", temp)
# # # print(hierarchy)


# cv2.waitKey(0)
# cv2.destroyAllWindows()


def padRect(image, rect, padding):
    height, width, num = image.shape

    x, y, w, h = rect
    y0, y1, x0, x1 = y-h/2-padding, y+h/2+padding, x-w/2-padding, x+w/2+padding

    if(y0 < 0):
        y0 = 0
    if(y1 > height):
        y1 = height
    if(x0 < 0):
        x0 = 0
    if(x1 > width):
        x1 = width
    return (int(x0), int(y0), int(x1), int(y1))


def calcRect(image, rect, padding=20, areaThreshold=2500):

    x0, y0, x1, y1 = padRect(image, rect, padding)
    img = image[y0:y1, x0:x1]
    cv2.imshow("calcRect", img)
    # top = int(0.05 * image.shape[0])  # shape[0] = rows
    # bottom = top
    # left = int(0.04 * image.shape[1])  # shape[1] = cols
    # right = left
    # value = [255, 255, 255]
    # borderType = cv2.BORDER_CONSTANT
    # img = cv2.copyMakeBorder(img, top, bottom, left,
    #                         right, borderType, None, value)

    cv2.imshow("calcRect0", img)
    # 灰度
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # # 高斯模糊
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # # Canny提取边缘
    processed = cv2.Canny(img, 50, 150, 1)

    cv2.imshow("calcRect1", processed)
    # 寻找轮廓
    img1, contours, hierarchy = cv2.findContours(
        processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if(len(contours)<=0):
        return []

    # 根据面积过滤，筛选大面积的框
    maxAreas = list(filter(lambda cons: cv2.contourArea(cons)
                      > areaThreshold, contours))
    
    print('maxAreas')
    print(len(maxAreas))

    if(len(maxAreas)<=0):
        return []

    # 获取点的矩形
    rects = list(map(lambda area: cv2.minAreaRect(area), maxAreas))

    if(len(rects)<=0):
        return []

    rectArr = list(map(lambda rect: [int(rect[0][0]+x0),int(rect[0][1]+y0),int(rect[1][0]),int(rect[1][1])],rects))
    print('rectArr')
    print(len(rectArr))

    result =  max(rectArr,key=lambda rect:rect[2]*rect[3])
    print('result')
    print(result)

    return [result]


def drawRect(image, rects=[]):
    boxs = []
    for rect in rects:
        pass
        p0, p1, n = (rect[0], rect[1]), (rect[2], rect[3]), 0
        box = np.int0(cv2.boxPoints((p0, p1, n)))
        boxs.append(box)

    temp = cv2.drawContours(image.copy(), boxs, -1, (0, 0, 255), 1)

    return temp


img = cv2.imread("./img.jpg", 1)
print(type(img))
print(img.shape)
arr=np.array([
    [
        [0,1,2], [0,1,2]
    ],
    [
        [0,1,2], [0,1,2]
    ]
])

print(type(arr))
# cv2.imshow("img", img)

# rect = [320, 760, 500, 250]

# # rect = [(200, 200, 400, 400)]

# img1 = drawRect(img, [rect])

# cv2.imshow("img1", img1)

# print(rect)

# rects = calcRect(img, rect,20,200)
# print('rects')
# print(rects)

# img2 = drawRect(img, rects)

# cv2.imshow("img2", img2)


# cv2.waitKey(0)
# cv2.destroyAllWindows()
