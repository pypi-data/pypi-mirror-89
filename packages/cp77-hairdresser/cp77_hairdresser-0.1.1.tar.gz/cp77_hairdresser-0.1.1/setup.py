import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cp77_hairdresser",
    version="0.1.1",
    author="Egej Vencelj",
    author_email="egej.vencelj@gmail.com",
    description="Cyberpunk 2077 hairstyle changer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eVen-gits/cp77_hairdresser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyqt5',
    ],
    package_data={
      'cp77_hairdresser': ['ui/*', 'hairstyles.json', 'ui/images/female/*', 'ui/images/male/*'],
    },
)
