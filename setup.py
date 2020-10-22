import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandas-pipeline-graphviz", # Replace with your own username
    version="0.1.5",
    author="Quentin Chenevier",
    author_email="qchenevier@users.noreply.github.com",
    description="Pandas pipeline in graphviz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qchenevier/pandas-pipeline-graphviz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas>=1.0.0",
        "networkx>=2.5",
        "addict>=2.2",
    ],
    python_requires=">=3.6",
)
