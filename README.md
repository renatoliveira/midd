# midd
Magical Image Duplicate Detector

This is a simple Python program to detect duplicate of images in a directory.

```
python main.py <directory> <certainty>
```

Where `directory` is the path of the folder you want to run the script on. And `certainty` is the percentage of, well, certainty, that the script will consider two images identical.

When running on the `sample_images` directory the expected behavior is that the script will open your default web browser and show a temporary HTML file with the images in a table of `image => [similar images]`. With these three examples of Krystal arts, from Star Fox, the output should be two rows, of images `7ca89435aee9a06c3c4879347093ece6` and `9b54005da1051123d6b5d81e5d8f3e1b`, which are identical (except for the resolution, that is different).

# How this works

Midd works by using Pillow to get your image file, converting it to grayscale, and then shrinking it to 17x16 pixels. With this grayscale tiny little map it builds a true/false value, like a signature for said image.

This is done to every image inside the specified folder, and then, when it is done with this heavy work, the script starts comparing the images. If you have a folder with 4.000 images then this could take a few minutes, since it will do a little more than 17 million comparisons.

## Example

`7ca89435aee9a06c3c4879347093ece6.jpg` is like this:

![](https://github.com/renatoliveira/midd/blob/master/sample_images/7ca89435aee9a06c3c4879347093ece6.jpg?raw=true)

Then it is turned to grayscale:

![](https://github.com/renatoliveira/midd/blob/master/repository_images/grayscale_sample.jpeg?raw=true)

Which is resized to:

![](https://github.com/renatoliveira/midd/blob/master/repository_images/resized.jpeg?raw=true)

And it is actually `10101001010010100010100101001010011010010100101001001001010010100101100101001010010110010100101001011101010010100101111101001010010111110100101001011111010010100101111101001010010111110100101001011111010010100101111101001010010111110100101001011111010010000101111101001001` after passing through `build_map` in `conversion.py`. This hash is 100% equal to the hash produced by `9b54005da1051123d6b5d81e5d8f3e1b.jpg`.