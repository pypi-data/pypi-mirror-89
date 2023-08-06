from setuptools import setup
import setuptools
# with open("README.md", "r") as fh:
#     long_description = fh.read()
long_description = ''
setup(
    name='textone',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/panchunguang',
    license='MIT',
    author='Chunguang Pan',
    author_email='panchunguang@126.com',
    description='aitext',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)