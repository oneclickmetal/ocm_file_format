import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ocm_file_format',
    version='0.0.1',

    author="Matthias Harrer",
    author_email="matthias.harrer@oneclickmetal.com",
    description="Module for reading file in the ocm file format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    python_requires='>=2.7',
)