from PIL import Image
import numpy as np
from scipy import misc


def arr2txt(arr, filename):
    with open(filename, 'w') as txt:
        for i in arr:
            for j in i:
                txt.write(str(j) + " ")
            else:
                txt.write("\n")


def rgb2gray(rgb_arr):
    return np.array(np.dot(rgb_arr[..., :3], [0.299, 0.587, 0.114]), dtype=np.uint8)


def dilate(img_arr, structuring_element):
    dil_img = np.zeros(img_arr.shape, dtype=np.uint8)
    for i in range(img_arr.shape[0]):
        for j in range(img_arr.shape[1]):
            if img_arr[i, j] == structuring_element[int(structuring_element.shape[0]/2), int(structuring_element.shape[1]/2)]:
                try:
                    dil_img[i:i+structuring_element.shape[0], j:j +
                            structuring_element.shape[1]] = structuring_element
                except ValueError:
                    continue
    else:
        return dil_img


def erosion(img_arr, structuring_element):
    ero_img = np.zeros(img_arr.shape, dtype=np.uint8)
    for i in range(img_arr.shape[0]):
        for j in range(img_arr.shape[1]):
            try:
                if np.array_equal(img_arr[i:i+structuring_element.shape[0], j:j +
                           structuring_element.shape[1]], structuring_element):
                    ero_img[i+int(structuring_element.shape[0]/2),
                            j+int(structuring_element.shape[1]/2)] = 1
            except ValueError:
                continue
    else:
        return ero_img

def opening(img_arr, structuring_element):
    open_arr = np.zeros(img_arr.shape, dtype=np.uint8)
    open_arr = dilate(erosion(img_arr, structuring_element),
                      structuring_element)
    return open_arr


def closing(img_arr, structuring_element):
    close_arr = np.zeros(img_arr.shape, dtype=np.uint8)
    close_arr = erosion(
        dilate(img_arr, structuring_element), structuring_element)
    return close_arr


def boundary(img_arr, structuring_element):
    bou_arr = img_arr - erosion(img_arr, structuring_element)
    return bou_arr

def main():
    with Image.open("input.png") as img:
        arr = np.array(img.getdata(), np.uint8, copy=True).reshape(
            img.size[1], img.size[0], 3)
        gray_arr = rgb2gray(arr)
        
        monochrome = gray_arr < 127
        monochrome = monochrome.astype(np.int)
        mono = monochrome * 255
        structuring_element = np.array(
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8)

        misc.imsave("mono.png", mono)
        dil = dilate(monochrome, structuring_element) * 255
        misc.imsave("dil.png", dil)
        ero = erosion(monochrome, structuring_element) * 255
        misc.imsave("ero.png", ero)
        arr2txt(monochrome, "mono.txt")
        arr2txt(dilate(monochrome, structuring_element), "dilate.txt")
        arr2txt(erosion(monochrome, structuring_element), "erosion.txt")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bye... bye.. ")

