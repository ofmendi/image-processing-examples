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

def local_bit_pattern(img_arr):
    lbp_img = np.zeros(img_arr.shape, dtype=np.uint8)
    for i in range(img_arr.shape[0]):
        for j in range(img_arr.shape[1]):
            try:
                tmp_arr = img_arr[i:i + 3, j:j + 3]
                tmp = tmp_arr > tmp_arr[int(
                    tmp_arr.shape[0]/2), int(tmp_arr.shape[1]/2)]
                tmp = tmp.astype(np.int).reshape(1, 9)[0]
                tmp = np.delete(tmp, [4])
                tmp = np.packbits(tmp)
                tmp_arr[int(tmp_arr.shape[0]/2), int(tmp_arr.shape[1]/2)] = tmp
                lbp_img[i:i + 3, j:j + 3] = tmp_arr
            except ValueError:
                continue
    else:
        return lbp_img


def main():
    with Image.open("input.jpg") as img:
        arr = np.array(img.getdata(), np.uint8, copy=True).reshape(
            img.size[1], img.size[0], 3)
        grey_arr = rgb2gray(arr)
        misc.imsave("res.png", local_bit_pattern(grey_arr))

        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bye... bye.. ")

