from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="da-xn-island",
    version="1.0.1",
    description="The Da-xn Island package allows you to get Da-xn Island API data instantly with simple functions!",
    long_description_content_type="text/markdown",
    long_description=readme(),
    url="https://da-xn.com/packages",
    author="Da-xn",
    author_email="dan@da-xn.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["da_xn_island"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={},
)
