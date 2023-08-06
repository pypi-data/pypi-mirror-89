import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read().strip()

setuptools.setup(
    name='kode_logger',
    version=version,
    author='KODE',
    licence='MIT',
    author_email='ashelepov@kode-t.ru',
    description='Encode logs to JSON format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        'orjson': ['orjson>=3.1.0'],
    },
    python_requires='>=3.7',
)
