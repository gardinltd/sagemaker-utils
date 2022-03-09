import setuptools


try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except:
    long_description = "To be added"


setuptools.setup(
    name="smUtils",
    version="0.0.6",
    author="Sathwik",
    author_email="s.mandava@gardin.co.uk",
    description="Common useful functions for projects using Sagemaker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gardinltd/sagemaker-utils",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    packages=['smUtils'],
    package_dir = {'smUtils': 'sm-utils'},
    python_requires=">=3.6",
)
