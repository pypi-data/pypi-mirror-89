from setuptools import setup
import codecs
import os.path

# read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# read version information from __init__.py
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='okama',
    version=get_version("okama/__init__.py"),
    license='MIT',
    description='Modern Portfolio Theory (MPT) Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sergey Kikevich',
    author_email='sergey@rostsber.ru',
    url='https://okama.io/',
    download_url='https://github.com/mbk-dev/okama/archive/v0.81.tar.gz',
    keywords=['finance', 'investments', 'efficient frontier', 'python', 'optimization'],
    packages=['okama', 'tests'],
    package_data={'tests': ['*.csv']},
    install_requires=['pandas>=0.25.0',
                      'numpy<=1.19.3',
                      'scipy>=0.14.0',
                      'matplotlib',
                      'requests'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
