from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirement_packages = f.read().split("\n")


setup(
    name='iqradre',
    version='0.0.2',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nunenuh/iqradre',
    author='Lalu Erfandi Maula Yusnu',
    author_email='nunenuh@gmail.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='pytorch deep learning machine learning',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    python_requires='>=3.6, <=3.6',
    install_requires=requirement_packages,

    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nunenuh/iqradre/issues',
        'Source': 'https://github.com/nunenuh/iqradre/',
    },
)
