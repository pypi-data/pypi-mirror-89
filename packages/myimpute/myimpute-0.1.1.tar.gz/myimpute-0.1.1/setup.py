import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myimpute",
    version="0.1.1",
    author="Shaobo Zhuang",
    license="MIT",
    author_email="dcbajk@vip.qq.com",
    description="Imputes missing data like a linear equation",
    keywords=['Imputation', 'Missing Values', 'Missing', 'Linear', 'Mean'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    url="https://github.com/imjxydhh/MyImputation",
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
