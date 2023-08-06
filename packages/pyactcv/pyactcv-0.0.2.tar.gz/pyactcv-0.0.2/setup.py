from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'pandas',
    'numpy'
]

setup_requires = [
    'pytest-runner'
]

tests_require = [
    'pytest',
    'coverage',
    'pytest-cov',
    'coveralls'
]

extras_require = {
    'dev': [
        'pytest',
        'coverage',
        'pytest-cov',
        'coveralls'
    ],
}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyactcv",
    version="0.0.2",
    author="Sebastian Blum",
    author_email="sebast.blum@gmail.com",
    description="Combine the Cognitive Architecture ACT-R with user data",
    py_modules=['pyactcv'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seblum/pyactcv",
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3', # due to f string
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Artistic Software',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        #'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    python_requires='>=3.6',
)
