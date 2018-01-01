"""
Main thing.
"""
import sys
import os
import json
import glob
import click
from tqdm import tqdm
from PIL import Image
import conversion
import reporting

def save_json(images: dict):
    '''
    Saves image hashes in a JSON file.
    '''
    with open('hashdata.json', 'w') as json_file:
        json.dump(images, json_file)

@click.command()
@click.option('-dir', '--directory', default=os.path.curdir, help='Directory to run the script.')
@click.option('-s', '--sample_size', default=16, help='Image sample size to generate the hashes.\
 The bigger, the more precise, and also the slower.')
@click.option('-a', '--accuracy', default=95, help='Accuracy level. Defaults to 95 (as in 95% sure\
 two images are equal.')
@click.option('-j', '--json', 'savejson', default=False, help='Save hash data to a json file.',
              is_flag=True)

def run(directory: str, sample_size: int, accuracy: int, savejson: bool):
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
        for image_x in tqdm(results):
            for image_y in results:
                if image_x != image_y:
                    if image_x not in similar_images:
                        similar_images[image_x] = []
                    if image_y not in similar_images:
                        similar_images[image_y] = []
                    if image_x in similar_images[image_y] or image_y in similar_images[image_x]:
                        break
                    check = conversion.verify(results[image_x], results[image_y])
                    if check > accuracy:
                        similar_images[image_x].append(image_y)
                        similar_images[image_y].append(image_x)
        reporting.generate(similar_images)
        if savejson:
            save_json(results)
    else:
        print('[{}] is not a valid directory.'.format(sys.argv[1]))

if __name__ == '__main__':
    #pylint: disable=E1120
    run()
