from setuptools import setup
import setuptools

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: Microsoft :: Windows
Operating System :: Unix
Programming Language :: C
Programming Language :: C++
Programming Language :: Cython
Programming Language :: Python
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development :: Libraries
"""

MAJOR = 0
MINOR = 0
MICRO = 2
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


def setup_package():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    metadata = dict(
        name="pyrankit",  # Replace with your own username
        version=VERSION,
        author="ZhongchuanSun",
        author_email="zhongchuansun@gmail.com",
        description="rankit",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        platforms=["Windows", "Linux"],
        classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires='>=3.6'
    )
    setup(**metadata)


if __name__ == '__main__':
    setup_package()
