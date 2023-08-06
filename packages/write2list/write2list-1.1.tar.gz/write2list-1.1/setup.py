from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='write2list',
    version='1.1',
    description='Convert a tuple of lists to a list.',
    long_description=long_description,
    long_description_content_type="text/markdown",      
    url='https://github.com/janpreet/write2list',
    author='Janpreet Singh',
    author_email='janpreetsinghgill@gmail.com',
    packages=['write2list'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    zip_safe=False)