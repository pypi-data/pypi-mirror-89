import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvtable",
    version="0.1.0",
    author="Uri Mann",
    author_email="abba.mann@gmail.com",
    description="C++ v-table binding for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urielmann/cinterface",
    license = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=2.7',
    #packages=['pyvtable'],
    package_dir={'src': 'src'}
)