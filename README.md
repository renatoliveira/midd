# midd
Magical Image Duplicate Detector

This is a simple Python program to detect duplicate of images in a directory.

```
python main.py <directory> <certainty>
```

Where `directory` is the path of the folder you want to run the script on. And `certainty` is the percentage of, well, certainty, that the script will consider two images identical.

When running on the `sample_images` directory the expected behavior is that the script will open your default web browser and show a temporary HTML file with the images in a table of `image => [similar images]`. With these three examples of Krystal arts, from Star Fox, the output should be two rows, of images `7ca89435aee9a06c3c4879347093ece6` and `9b54005da1051123d6b5d81e5d8f3e1b`, which are identical (except for the resolution, that is different).