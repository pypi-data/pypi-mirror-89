import cv2
import numpy as np

AREA_RATE = 0.6

# 填充目标区域padding像素


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


# 精确计算目标区域
def calcRect(image, box, padding=5, areaThreshold=900):

    height, width, chanel = image.shape

    pad = max(box[2], box[3])*0.1
    pad = padding if pad > padding else pad
    # 放到目标区域
    x0, y0, x1, y1 = padRect(image, box, pad)
    img = image[y0:y1, x0:x1]

    # 灰度
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    img = cv2.equalizeHist(img)
    # 高斯模糊
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Canny提取边缘
    processed = cv2.Canny(img, 50, 100, 1)

    # 寻找轮廓
    contours, hierarchy = cv2.findContours(
        processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if(len(contours) <= 0):
        return None

    rects = [cv2.boundingRect(cnt) for cnt in contours]

    points = list()
    for rect in rects:
        points.append((rect[0], rect[1]))
        points.append((rect[0]+rect[2], rect[1]+rect[3]))
        # points.append((rect[0], rect[1]+rect[3]))
        # points.append((rect[0]+rect[2], rect[1]))

    # # 四个顶点
    # point4s = [(0, 0), (x1-x0, 0), (0, y1-y0), (x1-x0, y1-y0)]

    # # 寻找离四个顶点最近的矩形点
    # tarPoints = []
    # radius = (x1-x0)/10
    # for point in points:
    #     for p in point4s:
    #         if(isNearbyPoint(p, radius, point)):
    #             tarPoints.append(point)

    # if(len(tarPoints) > 0):
    #     rect = cv2.boundingRect(np.array(tarPoints))
    # else:
    #     rect = cv2.boundingRect(np.array(points))

    rect = cv2.boundingRect(np.array(points))
    return [rect[0]+x0, rect[1]+y0, rect[2]-1, rect[3]-1]

# 框校准，image 是图片的三维数组


def calcRectByImage(image, boxs=[], padding=5, areaThreshold=900):
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
            if((w*h)/(width*height) > AREA_RATE):
                if(x < 0):
                    w = w+x
                    x = 0
                # x = 0 if(x < 0) else x
                if(y < 0):
                    h = h+y
                    y = 0
                # y = 0 if(y < 0) else y
                w = imgWidth-x if(x+w > imgWidth) else w
                h = imgHeight-y if(y+h > imgHeight) else h
                results.append([label, x, y, w, h])
            else:
                results.append(box)
            # results.append([label, x, y, w, h])
        else:
            results.append(box)

    return results

# 图片框校准,image 是二进制数组


def calcRectByImageBytes(image, boxs=[], padding=5, areaThreshold=900):
    arr = np.asarray(bytearray(image), dtype="uint8")
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return calcRectByImage(img, boxs, padding, areaThreshold)

# 图片框校准,source 是图片文件路径


def calcRectByImagePath(source, boxs=[], padding=5, areaThreshold=900):
    img = img0 = cv2.imread(source)
    return calcRectByImage(img, boxs, padding, areaThreshold)
