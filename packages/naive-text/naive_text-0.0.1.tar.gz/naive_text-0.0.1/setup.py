import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []
with open('requirements.txt', mode='rt', encoding='utf8') as fin:
    for line in fin:
        install_requires.append(line.rstrip('\n'))

setuptools.setup(
    name="naive_text",
    version="0.0.1",
    description="Text utils in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naivenlp/naive-text",
    author="ZhouYang Luo",
    author_email="zhouyang.luo@gmail.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={

    },
    license="Apache Software License",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    )
)
