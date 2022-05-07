from setuptools import setup, find_packages

VERSION="0.0.5"
with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='underscore3',
    version=VERSION,
    url='https://github.com/sfinktah/underscore3',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license='MIT',
    author='Christopher Anderson',
    author_email='sfinktah@github.spamtrak.org',
    description='TBA',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
    packages=find_packages(),
    install_requires=[],
)

