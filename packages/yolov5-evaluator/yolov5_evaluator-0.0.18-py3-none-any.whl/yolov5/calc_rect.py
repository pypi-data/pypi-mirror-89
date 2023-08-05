import cv2
import numpy as np

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


# 精确计算目标区域
def calcRect(image, box, padding=30, areaThreshold=10):

    height, width, chanel = image.shape

    pad = min(box[2], box[3])*0.1
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
    processed = cv2.Canny(img, 50, 150, 1)

    # 寻找轮廓
    contours, hierarchy = cv2.findContours(
        processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if(len(contours) <= 0):
        return None

    rects = [cv2.boundingRect(cnt) for cnt in contours]

    # 根据面积过滤，筛选大面积的框
    rects = list(filter(lambda rect: rect[2]*rect[3] > areaThreshold, rects))

    if(len(rects) <= 0):
        return None

    # 坐标修正
    rects = [[rect[0]+x0, rect[1]+y0, rect[2], rect[3]] for rect in rects]

    # 获取最大的矩形
    rects = max(rects, key=lambda rect: rect[2]*rect[3])

    return rects

# 框校准，image 是图片的三维数组
def calcRectByImage(image, boxs=[], padding=20, areaThreshold=900):
    height, width, chanel = image.shape

    borderType = cv2.BORDER_CONSTANT
    value = [255, 255, 255]
    img = cv2.copyMakeBorder(image, padding, padding,
                             padding, padding, borderType, None, value)

    results = []
    for box in boxs:
        label, x, y, w, h = box
        result = calcRect(img, [x+padding, y+padding,
                                w, h], padding, areaThreshold)
        if(result != None):
            x, y, w, h = result[0]-padding, result[1] - \
                padding, result[2], result[3]
            x = 0 if(x < 0) else x
            y = 0 if(y < 0) else y
            w = width-x if(x+w > width) else w
            h = height-y if(y+h > height) else h
            results.append([label, x, y, w, h])
        else:
            results.append(box)

    return results

# 图片框校准,image 是二进制数组
def calcRectByImageBytes(image, boxs=[], padding=20, areaThreshold=900):
    arr = np.asarray(bytearray(image), dtype="uint8")
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return calcRectByImage(img, boxs, padding, areaThreshold)
