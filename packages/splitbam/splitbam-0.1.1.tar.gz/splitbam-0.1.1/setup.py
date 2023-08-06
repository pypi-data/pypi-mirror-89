import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='splitbam',
    version='0.1.1',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='Split a BAM file into two subsamples',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/splitbam.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['pysam'],
    entry_points={
        'console_scripts': ['splitbam=splitbam.splitbam:main',]
    }
)
