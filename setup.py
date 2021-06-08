import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()

setuptools.setup(
    name="midd",
    version="1.1.2",
    author="Renato Oliveira",
    author_email="renatoliveira@pm.me",
    description="The magic image duplicate detector works as its name suggests: it shows you potential duplicates of your images.",
    description_long="The magic image duplicate detector works as its name suggests: it shows you potential duplicates of your images.",
    url="https://github.com/renatoliveira/midd",
    packages = ["midd"],
    entry_points={
        "console_scripts": [
            "midd = midd.main:run",
        ]
    },
    classifiers=[
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Image Recognition"
    ],
    excluded=[
        "sample_images/*",
        "repository_images/*"
    ],
    install_requires=[
        "Pillow==8.2.0",
        "tqdm==4.56.0",
        "click>=6",
    ],
    python_requires=">=3.6"
)