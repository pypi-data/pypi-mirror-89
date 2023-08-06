import os
import sys
import setuptools

with open(os.path.join(sys.path[0], "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PdfCC",
    version="1.0.0",
    author="S Krishna Bhat",
    author_email="memotoskbhat@gmail.com",
    description="PDF cropper & compressor: removes unwanted noise from pdf \
        and compresses them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pdfcc/PDF-CC.git",
    install_requires=[
          'pdf2image',
          'pillow',
      ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['pdfcc = pdfcc.pdfcc:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
