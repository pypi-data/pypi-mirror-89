import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rev-seqs",
    version="0.0.1",
    author="Nhan Nguyen",
    author_email="nhannguyen72089@gmail.com",
    description="Revert sequences to consensus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nguyen-t-nhan/rev-seqs",
    install_requires=['numpy', 'pandas', 'pysam'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
