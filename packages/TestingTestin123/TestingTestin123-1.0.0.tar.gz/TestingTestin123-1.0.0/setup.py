from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name = "TestingTestin123",
    version = "1.0.0",
    description = "a demo",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/darrenkhlim/TestingTestin123",
    author = "Kang Heng",
    author_email = "e0426117@u.nus.edu",
    license = "NUS",
    classsifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages = ["dishastowork"],
    include_package_data = True, # able to contain other types files
    install_requires = ["numpy"], # all other libraries that the package requires
    entry_points = {
        "console_scripts": [
            "TestingTestin123 = dishastowork.aqws:main",
        ]
    }
)

