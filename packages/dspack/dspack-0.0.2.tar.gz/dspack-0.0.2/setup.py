import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dspack", # Replace with your own username
    version="0.0.2",
    author="Sanjay",
    author_email="vsanjaychowdary1999@gmail.com",
    description="Python Package of datastructures inbuilt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.swecha.org/SANJAY/python_package_contirbution",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
