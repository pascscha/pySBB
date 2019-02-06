import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySBB",
    version="1.0.0",
    author="Pascal Schärli",
    author_email="pas.schaerli@sunrise.ch",
    description="An unofficial python wrapper for the SBB api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pasch13/pySBB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
