"""
Converts an image to grayscale
"""
import sys
from PIL import Image

def to_grayscale(img: Image):
    '''
    Uses Pillow 'convert' method to return a grayscale
    version of an image.
    '''
    return img.convert('L')

def resize(img: Image, sqsize: int):
    '''
    Resizes the image to a common ratio and pixel format.
    '''
    img = img.resize((sqsize+1, sqsize), Image.BICUBIC)
    return img

def build_map(img: Image):
    '''
    Builds the true/false map, which is turned into the binary sequence
    which is used to compare images
    '''
    width, height = img.size
    pixels = list(img.getdata())
    difference = []
    for row in range(height):
        for col in range(width):
            if col != width:
                difference.append(pixels[col+row] > pixels[(col+row)+1])
    bin_val = ''
    for element in enumerate(difference):
        if element[1]:
            bin_val += '1'
        else:
            bin_val += '0'
    return bin_val

def verify(str1: str, str2: str):
    """
    Verify two numeric (0s and 1s) representations of images.
    """
    if len(str1) == len(str2):
        matches = 0
        misses = 0
        for char in enumerate(str1):
            if str1[char[0]] == str2[char[0]]:
                matches += 1
            else:
                misses += 1
        return (matches * 100) / len(str1)
    print('Lists with different sizes. Aborting...')
    return -1

if __name__ == '__main__':
    if 'gs' in sys.argv and 'rs' in sys.argv and 'bm' in sys.argv:
        build_map(resize(to_grayscale(Image.open(sys.argv[4])), 16))
    elif 'gs' in sys.argv and 'rs' in sys.argv:
        resize(to_grayscale(Image.open(sys.argv[3])), 16).save('output.jpeg', 'jpeg')
    elif sys.argv[1] == 'gs':
        to_grayscale(Image.open(sys.argv[2])).save('output.jpeg', 'jpeg')
    elif sys.argv[1] == 'rs':
        resize(Image.open(sys.argv[2]), 16).save('output.jpeg', 'jpeg')
    elif sys.argv[1] == 'bm':
        build_map(Image.open(sys.argv[2]))
    elif sys.argv[1] == 'check':
        verify(sys.argv[2], sys.argv[3])
