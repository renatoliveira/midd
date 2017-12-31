"""
Converts an image to grayscale
"""
import click
from tqdm import tqdm
from PIL import Image

def to_grayscale(img: Image):
    '''
    Uses Pillow 'convert' method to return a grayscale
    version of an image.
    '''
    return img.convert('L')

def resize_image(img: Image, sqsize: int):
    '''
    Resizes the image to a common ratio and pixel format.
    '''
    img = img.resize((sqsize+1, sqsize), Image.BICUBIC)
    return img

def generate_hash(img: Image):
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

@click.command()
@click.option('--file', help='Input image file.')
@click.option('--output', default='output.jpeg', help='Name of the output file. \
# Defaults to "output.jpeg"')
@click.option('--resize', default=False, help='Do the resize thing.', is_flag=True)
@click.option('--grayscale', default=False, help='Convert file to grayscale.', is_flag=True)
@click.option('--buildhash', default=False, help='Generate the image\'s hash.', is_flag=True)
@click.option('--sample_size', default=16, help='Image sample size')
@click.option('--dryrun', default=False, help='Dry run. Won\'t save files or generate reports.',
              is_flag=True)
@click.option('--check', default=False, help='Check two or more files.', is_flag=True)
@click.argument('files', nargs=-1)
def run(**kwargs):
    '''
    Run with command line arguments
    '''
    print(kwargs['check'])
    if not kwargs['check']:
        kwargs['image_file'] = Image.open(kwargs['file'])
        if kwargs['grayscale']:
            kwargs['image_file'] = to_grayscale(kwargs['image_file'])
        if kwargs['resize']:
            kwargs['image_file'] = resize_image(kwargs['image_file'], kwargs['sample_size'])
        if kwargs['buildhash']:
            print(generate_hash(kwargs['image_file']))
        if not kwargs['dryrun']:
            kwargs['image_file'].save(kwargs['output'], 'jpeg')
    else:
        hashes = {}
        results = []
        for filename in kwargs['files']:
            hashes[filename] = generate_hash(
                resize_image(to_grayscale(Image.open(filename)), kwargs['sample_size'])
            )
        for image_x in tqdm(hashes):
            for image_y in hashes:
                if image_x != image_y:
                    results.append((image_x, image_y, verify(hashes[image_x], hashes[image_y])))
        for result in results:
            print('{} is {}% equal to {}.'.format(
                result[0], result[2], result[1]
            ))

if __name__ == '__main__':
    #pylint: disable=E1120
    run()
