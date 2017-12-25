"""
Main thing.
"""
import sys
import os
import glob
from tqdm import tqdm
from PIL import Image
import conversion
import reporting

if __name__ == '__main__':
    '''
    1 = folder path
    2 = % of certainty
    '''
    CERTAINTY = int(sys.argv[2])
    if os.path.isdir(sys.argv[1]):
        IMAGES = glob.glob(sys.argv[1] + '*.png') + glob.glob(sys.argv[1] + '*.jpg')
        print('Reading {} images...'.format(len(IMAGES)))
        RESULTS = {}
        IMAGES = [os.path.abspath(image_path) for image_path in IMAGES]
        for image in tqdm(IMAGES):
            val = conversion.build_map(
                conversion.resize(
                    conversion.to_grayscale(Image.open(image)), 16
                )
            )
            image = ':\\'.join(image.split(':'))
            RESULTS[image] = val
        SIMILAR_IMAGES = {}
        for x in tqdm(RESULTS):
            for y in RESULTS:
                if x != y:
                    if x not in SIMILAR_IMAGES:
                        SIMILAR_IMAGES[x] = []
                    if y not in SIMILAR_IMAGES:
                        SIMILAR_IMAGES[y] = []
                    if x in SIMILAR_IMAGES[y] or y in SIMILAR_IMAGES[x]:
                        break
                    check = conversion.verify(RESULTS[x], RESULTS[y])
                    if check > CERTAINTY:
                        SIMILAR_IMAGES[x].append(y)
                        SIMILAR_IMAGES[y].append(x)
        reporting.generate(SIMILAR_IMAGES)
    else:
        print('[{}] is not a valid directory.'.format(sys.argv[1]))
