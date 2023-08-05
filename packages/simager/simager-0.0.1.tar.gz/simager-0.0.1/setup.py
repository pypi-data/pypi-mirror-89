import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simager",
    version="0.0.1",
    author="ulwan",
    license="MIT",
    author_email="ulwan.nashihun@tiket.com",
    description="A small package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/simager",
    packages=setuptools.find_packages(),
    package_data={"simager": ["data/normalizer.p", "data/stop_w.p"]},
    keywords=["nlp", "text-processing", "machine-learning", "data-scientist", "text-cleaner"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
    ],
    install_requires=[
        "emoji>=0.6.0",
        "beautifulsoup4>=4.9.3"
    ],
    python_requires=">=3.6",
)
