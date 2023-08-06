import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proximus",
    version="0.0.2",
    author="SnowCode",
    description="A web automation of Bbox3 web interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/SnowCode/bbox3",
    packages=setuptools.find_packages(),
)
