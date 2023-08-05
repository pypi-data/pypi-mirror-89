""" 
MIT License

Copyright (c) 2019 Claude SIMON (https://q37.info/s/rmnmqd49)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import setuptools

version = "0.1.3"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edutk",
    version=version,
    author="Claude SIMON",
#    author_email="author@example.com",
    description="Toolkit to make modern exercises for programming tutorials.",
    keywords="education, tutorial, programming, exercise, Atlas toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epeios-q37/edutk-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'atlastk',
    ],
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Intended Audience :: Education",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License ",
      "Operating System :: OS Independent",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",
      "Topic :: Education"
    ]
)
