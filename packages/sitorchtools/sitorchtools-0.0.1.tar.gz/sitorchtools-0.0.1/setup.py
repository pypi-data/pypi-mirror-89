import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sitorchtools",
    version="0.0.1",
    author="ulwan",
    license="MIT",
    author_email="ulwan.nashihun@tiket.com",
    description="A small package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/sitorchtools",
    packages=setuptools.find_packages(),
    keywords=["pytorchtools", "pytorch-early-stopping", "image-dataloader", "pytorch-imbalanced", "data-scientist", "deep-learning"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing"

    ],
    install_requires=[
        "matplotlib>=3.3.3",
        "numpy>=1.19.4",
        "scikit-learn>=0.24.0"
    ],
    python_requires=">=3.6",
)
