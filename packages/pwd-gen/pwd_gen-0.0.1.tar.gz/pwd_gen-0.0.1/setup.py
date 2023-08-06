import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pwd_gen",
    version="0.0.1",
    author="B00bleTeA",
    author_email="asnojus039@gmail.com",
    description="simple password generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/B00bleaTea/pwd_gen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
