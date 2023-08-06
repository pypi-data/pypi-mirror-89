from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="gsheet_access",
    version="1.0.1",
    description="A Python package to read gsheet  from google drive using gsheet id and plot and save between two numerical axis.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Amreesh kumar",
    author_email="starkk786@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["gsheet_access"],
    include_package_data=True,
    install_requires=["pandas","numpy","gsheet","oauthclient","matplotlib"]
)