import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="say-something-moon",
    version="1.0.0",
    description="the chatbot when you are alone",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.linkedin.com/in/moonyuema/",
    author="Moon Ma",
    author_email="moon30biology@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["saysomething"],
    include_package_data=True,
    install_requires=[
        "typing"
    ],
    entry_points={"console_scripts": ["saysomething=saysomething.__main__"]},
)