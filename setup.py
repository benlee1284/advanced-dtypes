import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="advanced-dtypes",
    version="0.0.2",
    author="Ben Lee",
    description="Data types not found in the standard library that are cool in various different ways ;)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["advanced_dtypes"],
    package_dir={"":"."},
    install_requires=[],
    project_urls={
        'Source': 'https://github.com/benlee1284/advanced-dtypes',
        'Tracker': 'https://github.com/benlee1284/advanced-dtypes/issues',
    },
)
