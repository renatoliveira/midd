"""
Main thing.
"""
import sys
import os
import glob
import click
from tqdm import tqdm
from PIL import Image
import conversion
import reporting

@click.command()
@click.option('--directory', default=os.path.curdir, help='Directory to run the script.')
@click.option('--sample_size', default=16, help='Image sample size to generate the hashes. The\
 bigger, the more precise, and also the slower.')
@click.option('--accuracy', default=95, help='Accuracy level. Defaults to 95 (as in 95% sure two\
 images are equal.')

def run(directory: str, sample_size: int, accuracy: int):
    '''
    Run the main program.
    '''
    if os.path.isdir(directory):
        images = glob.glob(directory + '\\*.png') + glob.glob(directory + '\\*.jpg')
        print('Reading {} images...'.format(len(images)))
        results = {}
        images = [os.path.abspath(image_path) for image_path in images]
        for image in tqdm(images):
            val = conversion.generate_hash(
                conversion.resize_image(
                    conversion.to_grayscale(Image.open(image)), sample_size
                )
            )
            image = ':\\'.join(image.split(':'))
            results[image] = val
        similar_images = {}
        for x in tqdm(results):
            for y in results:
                if x != y:
                    if x not in similar_images:
                        similar_images[x] = []
                    if y not in similar_images:
                        similar_images[y] = []
                    if x in similar_images[y] or y in similar_images[x]:
                        break
                    check = conversion.verify(results[x], results[y])
                    if check > accuracy:
                        similar_images[x].append(y)
                        similar_images[y].append(x)
        reporting.generate(similar_images)
    else:
        print('[{}] is not a valid directory.'.format(sys.argv[1]))

if __name__ == '__main__':
    #pylint: disable=E1120
    run()
