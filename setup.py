from Cython.Build import cythonize
from distutils.core import setup
from os.path import realpath

setup(
    name="matching_snippets",
    version="0.0.0",
    packages=['matching_snippets/'],
    description="Match a partial, corrupted sequence against a collection of documents, etc",
    author="Andrew Nystrom",
    author_email="AWNystrom@gmail.com",
    url="https://github.com/AWNystrom/MatchingSnippets",
    keywords=[],
    license="Apache 2.0",
    classifiers=["Programming Language :: Python",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 2",
                 "License :: OSI Approved :: Apache Software License",
                 "Operating System :: OS Independent",
                 "Development Status :: 4 - Beta",
                 "Intended Audience :: Developers"
                 ],
    install_requires=['simhash', 'spacy', 'nltk'],
    )