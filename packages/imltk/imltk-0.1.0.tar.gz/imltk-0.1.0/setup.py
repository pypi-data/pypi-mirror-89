import setuptools
import imltk

with open("README.md", "rt", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="imltk",
    version=imltk.__version__,
    author="blueloveTH",
    author_email="blueloveTH@foxmail.com",
    description="Interpretable Machine Learning Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blueloveTH/imltk",
    packages=setuptools.find_packages(),
    install_requires=['pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)