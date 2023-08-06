import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imbaedit",
    version="1.0.4",
    author="Jon Craton",
    author_email="jon@joncraton.com",
    description="Image Batch Editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jncraton/imbaedit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'imbaedit=imbaedit:main',
        ],
    },
    install_requires=[
        'pillow',
    ],
)
