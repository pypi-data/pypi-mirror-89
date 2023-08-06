import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HTMLPackImagesaver",
    version="1.0.2",
    author="otapi",
    description="Download and save images of HTML only archives - e.g. backup package of Medium.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otapi/HTMLPackImagesaver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    python_requires='>=3',
) 