from PIL import Image
import numpy as np


def arr2txt(arr, filename):
    with open(filename, 'a') as txt:
        for i in arr:
            for j in i:
                txt.write(str(j) + " ")
            else:
                txt.write("\n")


def rgb2gray(rgb_arr):
    return np.array(np.dot(rgb_arr[..., :3], [0.299, 0.587, 0.114]), dtype=np.uint8)


def main():
    with Image.open("input.png") as img:
        arr = np.array(img.getdata(), np.uint8, copy=True).reshape(
            img.size[1], img.size[0], 3)


        arr2txt(rgb2gray(arr), "gray.txt")

        for i, j in zip((0, 1, 2), (1, 2, 0)):
            tmp_arr = np.copy(arr)
            tmp_arr[..., i] = 0
            tmp_arr[..., j] = 0
            filename = "c{}.txt".format(i)
            arr2txt(tmp_arr, filename)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bye... bye.. ")

