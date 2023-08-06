import setuptools
with open("README.md",'r',encoding='utf8') as f:
    long_description = f.read()
setuptools.setup(
    name ="unique_arithmetic",
    version="1.5",
    author="中国",
    author_email="pgacr123@163.com",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages=setuptools.find_packages(),
    url="https://www.vipcode.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',


)