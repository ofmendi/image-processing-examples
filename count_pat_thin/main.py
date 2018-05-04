import numpy as np
import cv2

def count(img):
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
    img = cv2.blur(img, (3, 3))

    ret, labels = cv2.connectedComponents(img)

    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)

    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0

    return (ret, labeled_img)

def thin(img):
    size = np.size(img)
    res = np.zeros(img.shape, np.uint8)

    ret, img = cv2.threshold(img, 127, 255, 0)
    structuring_element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    img = cv2.blur(img, (3, 3))

    while True:
        eroded = cv2.erode(img, structuring_element)
        tmp = cv2.dilate(eroded, structuring_element)
        tmp = cv2.subtract(img, tmp)
        res = cv2.bitwise_or(res, tmp)
        img = eroded.copy()
        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            return res

def main():
    """ Main func """
    img = cv2.imread('input2.png', 0)
    skel = thin(img)
    c, i = count(img)
    print("Tespit edilen patates sayısı : " + str(c))
    cv2.imshow("skel", skel)
    cv2.waitKey()    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bye... bye.. ")