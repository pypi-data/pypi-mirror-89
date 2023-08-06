import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NCBI_Companion",
    version="2.1.1",
    author="Xiaoping Li",
    author_email="lixiaopi@oregonstate.edu",
    description="NCBI_Companion assists you to build a reference database with a fasta and a mapping file through Genbank",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lixiaopi1985/NCBI_Companion",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=['biopython>=1.72', 'pandas>=0.23.4','beautifulsoup4>=4.6.3'],
)
