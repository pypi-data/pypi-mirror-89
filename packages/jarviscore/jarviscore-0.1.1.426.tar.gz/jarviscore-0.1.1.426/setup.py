import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jarviscore",
    version="0.1.1.426",
    author="Cubbei",
    author_email="cubbei@outlook.com",
    description="A python package for creating Twitch Bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/cubbei/jarviscore",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyMySQL', 'PyYAML', 'requests', 'simplejson'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    license="GPL",
    python_requires='>=3.6',
)
