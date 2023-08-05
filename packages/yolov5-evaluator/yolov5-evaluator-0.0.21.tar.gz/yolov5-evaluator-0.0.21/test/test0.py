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

def boundResize(width, height, boxs):
    results = list()
    for box in boxs:
        x, y, w, h = box
        x = 0 if(x < 0) else x
        y = 0 if(y < 0) else y
        w = width-x if(x+w > width) else w
        h = height-y if(y+h > height) else h
        results.append([x, y, w, h])
    return results


def padRect(image, box, padding):
    height, width, num = image.shape

    x, y, w, h = box
    y0, y1, x0, x1 = y-padding, y+h+padding, x-padding, x+w+padding

    y0 = 0 if(y0 < 0) else y0
    y1 = height if(y1 > height) else y1

    x0 = 0 if(x0 < 0) else x0
    x1 = width if(x1 > width) else x1

    return (int(x0), int(y0), int(x1), int(y1))


def isNearbyPoint(target, radius, point):
    x0, y0 = target
    x1, y1 = point
    length = ((x1-x0)**2+(y1-y0)**2)**0.5
    return length < radius


count = 0
# 精确计算目标区域


def calcRect(image, box, padding=10, areaThreshold=10):
    global count
    count = count+1
    height, width, chanel = image.shape

    pad = min(box[2], box[3])*0.1
    pad = padding if pad > padding else pad
    # 放到目标区域
    x0, y0, x1, y1 = padRect(image, box, pad)
    img = image[y0:y1, x0:x1]
    # cv2.imshow('part'+str(count), img)
    # 灰度
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    img = cv2.equalizeHist(img)
    # 高斯模糊
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Canny提取边缘
    processed = cv2.Canny(img, 100, 300, 1)
    cv2.imshow('Canny'+str(count), processed)
    # 寻找轮廓
    contours, hierarchy = cv2.findContours(
        processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print('findContours'+str(count)+':'+str(len(contours)))

    temp = cv2.drawContours(img.copy(), contours, -1, (0, 0, 255), 1)

    # cv2.imshow('drawContours'+str(count), temp)

    if(len(contours) <= 0):
        return None

    rects = [cv2.boundingRect(cnt) for cnt in contours]

    drrects=map(lambda item:[0,item[0]+item[2]/2,item[1]+item[3]/2,item[2],item[3]] ,rects)
    img1 = drawRect(img, drrects)
    showImg("rectx"+str(count), img1)

    points = list()
    for rect in rects:
        points.append((rect[0], rect[1]))
        points.append((rect[0]+rect[2], rect[1]+rect[3]))
        points.append((rect[0], rect[1]+rect[3]))
        points.append((rect[0]+rect[2], rect[1]))

    # 四个顶点
    point4s = [(0, 0), (x1-x0, 0), (0, y1-y0), (x1-x0, y1-y0)]

    
    tarPoints=[]
    radius=20
    for point in points:
        for p in point4s:
            if(isNearbyPoint(p,radius,point)):
                tarPoints.append(point)

    rect = cv2.boundingRect(np.array(tarPoints))

    drrects=map(lambda item:[0,item[0]+item[2]/2,item[1]+item[3]/2,item[2],item[3]] ,[rect])
    img1 = drawRect(img, drrects)
    showImg("rect"+str(count), img1)

    rects = [rect]

    # # 根据面积过滤，筛选大面积的框
    rects = list(filter(lambda rect: rect[2]*rect[3] > areaThreshold, rects))

    if(len(rects) <= 0):
        return None

    rects = [[rect[0]+x0, rect[1]+y0, rect[2], rect[3]] for rect in rects]

    # rects = resizeBox(width, height,rects)
    # print(rects)

    # 获取最大的矩形
    rects = max(rects, key=lambda rect: rect[2]*rect[3])

    return rects


# def calcRectByImage(image, boxs=[], padding=20, areaThreshold=900):
#     arr = np.asarray(bytearray(image), dtype="uint8")
#     img0 = cv2.imdecode(arr, cv2.IMREAD_COLOR)
#     results = []
#     for box in boxs:
#         label, x, y, w, h = box
#         result = calcRect(img0, [x, y, w, h], padding, areaThreshold)
#         if(result != None):
#             results.append([label, result[0], result[1], result[2], result[3]])
#         else:
#             results.append(rect)

#     return results

def calcRectByImage(image, boxs=[], padding=10, areaThreshold=900):
    imgHeight, imgWidth, chanel = image.shape
    borderType = cv2.BORDER_CONSTANT
    value = [255, 255, 255]
    img = cv2.copyMakeBorder(image, padding, padding,
                             padding, padding, borderType, None, value)

    results = []
    for box in boxs:
        label, left, top, width, height = box
        result = calcRect(img, [left+padding, top+padding,
                                width, height], padding, areaThreshold)
        if(result != None):
            x, y, w, h = result[0]-padding, result[1] - \
                padding, result[2], result[3]
            if((w*h)/(width*height) > 0.5):
                x = 0 if(x < 0) else x
                y = 0 if(y < 0) else y
                w = imgWidth-x if(x+w > imgWidth) else w
                h = imgHeight-y if(y+h > imgHeight) else h
                results.append([label, x, y, w, h])
            else:
                results.append(box)
        else:
            results.append(box)

    return results


def drawRect(image, rects=[]):
    borderType = cv2.BORDER_CONSTANT
    value = [255, 255, 255]
    pad = 20
    img = cv2.copyMakeBorder(image, pad, pad, pad, pad,
                             borderType, None, value)
    boxs = []
    for rect in rects:
        pass
        p0, p1, n = (rect[1]+pad, rect[2] + pad), (rect[3], rect[4]), 0
        box = np.int0(cv2.boxPoints((p0, p1, n)))
        boxs.append(box)

    temp = cv2.drawContours(img.copy(), boxs, -1, (0, 0, 255), 2)

    return temp


def rectToBox(rects=[]):
    boxs = [[rect[0], rect[1]-rect[3]/2, rect[2] -
             rect[4]/2, rect[3], rect[4]] for rect in rects]
    return boxs


def boxToRect(boxs=[]):
    rects = [[box[0], box[1]+box[3]/2, box[2]+box[4]/2, box[3], box[4]]
             for box in boxs]
    return rects


def showImg(name, img):
    img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
    borderType = cv2.BORDER_CONSTANT
    value = [255, 255, 255]
    img = cv2.copyMakeBorder(img, 20, 20, 20, 20, borderType, None, value)
    cv2.imshow(name, img)


img = cv2.imread("./image/bjnsh_.png", 1)

# showImg("img", img)

rects = [[1, 709.0, 641.5, 274.0, 29.0], [1, 841.5, 33.5, 93.0, 35.0], [1, 363.0, 642.0, 250.0, 26.0], [0, 724.5, 693.0, 117.0, 42.0], [0, 390.0, 689.5, 126.0, 39.0], [1, 1066.5, 34.5, 89.0, 35.0], [1, 986.0, 644.0, 146.0, 22.0], [1, 1175.0, 34.0, 94.0, 34.0], [0, 1065.0, 689.5, 124.0, 37.0], [1, 727.5, 34.0, 91.0, 34.0], [1, 952.5, 33.5, 95.0, 35.0], [2, 633.5, 38.0, 73.0, 68.0], [0, 353.5, 37.0, 319.0, 62.0], [0, 723.0, 557.5, 338.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                135.0], [0, 383.5, 561.5, 321.0, 129.0], [0, 1070.0, 563.5, 324.0, 133.0], [0, 721.0, 254.5, 1442.0, 375.0]]

rects = list(filter(lambda item: item[0] == 0 or item[0] == 2 , rects))

img1 = drawRect(img, rects)
showImg("source", img1)

boxs = rectToBox(rects)
boxs = calcRectByImage(img, boxs, 5, 900)
# print('boxs1')
# print(boxs)

rects = boxToRect(boxs)
img2 = drawRect(img, rects)
showImg("result", img2)


cv2.waitKey(0)
cv2.destroyAllWindows()
