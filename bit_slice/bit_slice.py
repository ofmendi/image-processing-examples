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


def main():
    with Image.open("input.png") as img:
        arr = np.array(img.getdata(), np.uint8, copy=True).reshape(
            img.size[1], img.size[0], 3)
        gray_arr = rgb2gray(arr)
        
        gray_bit_arr = np.unpackbits(gray_arr, axis=1).reshape(
            img.size[1], img.size[0], 8)

        # zeros = np.zeros((256, 256) , dtype=np.uint8)
        # msb = np.stack(
        #     (gray_bit_arr[:, :, 0], zeros, zeros, zeros, zeros, zeros, zeros, zeros), axis=-1)
        
        with Image.open("secret.png").convert('L') as secret_img:
            secret_img_arr = np.array(secret_img.getdata(), dtype=np.uint8).reshape(
                (secret_img.size[0], secret_img.size[1]))

            monochrome = secret_img_arr < 127
            monochrome = monochrome.astype(np.int)
            gray_bit_arr[:, :, 7] = monochrome
            
            gray_bit_arr = gray_bit_arr.reshape((secret_img.size[0], secret_img.size[0] * 8))
            gray_bit_arr = np.packbits(gray_bit_arr, axis=1)
            misc.imsave("output.png", gray_bit_arr)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bye... bye.. ")

