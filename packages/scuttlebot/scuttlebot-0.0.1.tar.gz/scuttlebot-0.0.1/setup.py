import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

discordpy = 'discord.py'
riotwatcher = 'riotwatcher'
bs4 = 'bs4'
lxml = 'lxml'

setuptools.setup(
    name="scuttlebot", # Replace with your own username
    version="0.0.1",
    author="Noah Garrett",
    author_email="nwggaming123@gmail.com",
    description="LoL Discord Bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://discord.gg/VMwphqfmQk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[discordpy, riotwatcher, bs4, lxml]
)