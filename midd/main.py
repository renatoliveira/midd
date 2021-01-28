"""
Main thing.
"""
import sys
import os
import json
import glob
import itertools
import click
from tqdm import tqdm
from PIL import Image
from midd import conversion
from midd import reporting

def save_json(images: dict):
    '''
    Saves image hashes in a JSON file.
    '''
    with open('hashdata.json', 'w') as json_file:
        content = {}
        for k, val in images.items():
            key = k.replace('\\', '/')
            content[key] = val
        json.dump(content, json_file, indent=True)

def get_hashes_from_file():
    '''
    Gets hashes from json file, if it exists.
    '''
    hashes = None
    if os.path.isfile(os.path.curdir + '\\hashdata.json'):
        with open('hashdata.json', 'r') as json_file:
            hashes = json.load(json_file)
    else:
        hashes = {}
    return hashes

def remove_repeated_hashes(images_read: list, hashes_from_file: list):
    '''
    Remove repeated hashes so the script doesn't need to generate
    again the hashes we already have in the hashdata.json file.
    '''
    result = []
    for image in (img.replace('\\', '/') for img in images_read):
        if not hashes_from_file or image not in hashes_from_file:
            result.append(image)
    return result

def get_image_hashes(images: list, sample_size: int):
    '''
    Get the hashes for the specified images, using the provided
    sample size.
    '''
    result = {}
    for image in tqdm(images):
        val = conversion.generate_hash(
            conversion.resize_image(
                conversion.to_grayscale(Image.open(image)), sample_size
            )
        )
        result[image] = val
    return result

def compare_hashes(images: dict, precision: int):
    '''
    Compares the hashes.
    '''
    similar_images = {}
    print('Comparing hashes...')
    for sample_a, sample_b in itertools.combinations(images.keys(), 2):
        match_result = conversion.verify(images[sample_a], images[sample_b])
        if match_result >= precision:
            if sample_a not in similar_images:
                similar_images[sample_a] = []
            if sample_b not in similar_images:
                similar_images[sample_b] = []
            similar_images[sample_a].append(sample_b)
            similar_images[sample_b].append(sample_a)
    return similar_images

@click.command()
@click.option('-dir', '--directory', default=os.path.curdir, help='Directory to run the script.')
@click.option('-s', '--samplesize', default=16, help='Image sample size to generate the hashes.\
 The bigger, the more precise, and also the slower.')
@click.option('-a', '--accuracy', default=95, help='Accuracy level. Defaults to 95 (as in 95% sure\
 two images are equal.')
@click.option('-j', '--json', 'savejson', default=False, help='Save hash data to a json file.',
              is_flag=True)
@click.option('-r', '--reset', 'reset', default=False, help='Analyzes every image even if\
 hashdata.json is present. If not used, images in the hashdata.json won\'t be analyzed again, but\
 their hashes will be compared normally.', is_flag=True)
@click.option('-nr', '--no-report', 'noreport', default=False, help='Disables report generation.',
              is_flag=True)
def run(**kwargs):
    '''
    Run the main program.
    '''
    if os.path.isdir(kwargs['directory']):
        images = []
        for image_extension in ['png', 'jpg']:
            print(kwargs['directory'] + '\\*.{}'.format(image_extension))
            images += glob.glob(kwargs['directory'] + '*.{}'.format(image_extension))

        print('Reading {} images...'.format(len(images)))
        existing_hashes = get_hashes_from_file()
        images = [os.path.abspath(image_path) for image_path in images]
        processed_images = get_image_hashes(
            remove_repeated_hashes(images, existing_hashes), kwargs['samplesize']
        )
        combined_images = {**existing_hashes, **processed_images}
        similar_images = compare_hashes(combined_images, kwargs['accuracy'])
        if not kwargs['noreport']:
            reporting.generate(similar_images)
        if kwargs['savejson']:
            save_json(combined_images)
    else:
        print('[{}] is not a valid directory.'.format(sys.argv[1]))

if __name__ == '__main__':
    run()
