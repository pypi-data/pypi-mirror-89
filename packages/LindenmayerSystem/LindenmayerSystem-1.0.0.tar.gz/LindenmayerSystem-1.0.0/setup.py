import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LindenmayerSystem", # Replace with your own username
    version="1.0.0",
    author="Subimal Deb",
    author_email="subimal.deb@gmail.com",
    description="A pure python module for generating iterations from the L-System or Lindenmayer system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/subimal/LSystem",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
