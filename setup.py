import re
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

with open("jugaad_data/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
print(version)

setuptools.setup(
    name="jugaad-data", # Replace with your own username
    version=version,
    description="Jugad data is a library to download historical stock data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://marketsetup.in/documentation/jugaad-data/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
    data_files=[('.', ['requirements.txt', "README.md"])],
    # other arguments here...
    entry_points={
        "console_scripts": [
            "jdata = jugaad_data.cli:cli",
        ]
    }
)
