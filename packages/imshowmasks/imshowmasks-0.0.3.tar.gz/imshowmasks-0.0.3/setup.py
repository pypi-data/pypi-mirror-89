import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imshowmasks", # Replace with your own username
    version="0.0.3",
    author="Malte Brammerloh",
    author_email="m.brammerloh@gmail.com",
    description="A slim package to handle and display binary masks in color over images shown with matplotlib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbrammerloh/imshowmasks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
