import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="songscrounger",
    version="0.2.3",
    author="Juan Carlos Gallegos Dupuis",
    author_email="jcgallegdup@gmail.com",
    description="A tool for finding Spotify tracks and albums from names mentioned in text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/okjuan/song-scrounger",
    packages=setuptools.find_packages(),
    install_requires=["spotify>=0.10.2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
