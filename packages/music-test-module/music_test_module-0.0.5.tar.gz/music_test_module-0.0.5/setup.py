import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="music_test_module",
    version="0.0.5",
    author="DHTung",
    author_email="dhtung161997@gmail.com",
    packages=setuptools.find_packages(),
    url="https://github.com/dhtung1997/music_test_module",
    python_requires='>3.6',
)
