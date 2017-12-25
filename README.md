# midd
Magical Image Duplicate Detector

This is a simple script using the Pillow library to find duplicate images inside a folder, given a certain accuracy.

```
python main.py <folder path> <minimnum accuracy>
```

This will make the script run and fetch the images which have a certain % of similarity.

Since the script uses only grayscale for now, it is possible that it will match two completely different images. Overall, the accuracy is pretty good.

When the script is run, it will open a web page with the result, displaying the image on the left, and the similar images on the right.
