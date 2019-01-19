import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sbpy",
    version="0.0.1",
    author="Pascal Schärli",
    author_email="pas.schaerli@sunrise.ch",
    description="An unofficial python wrapper for the SBB api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pasch13/sbpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
