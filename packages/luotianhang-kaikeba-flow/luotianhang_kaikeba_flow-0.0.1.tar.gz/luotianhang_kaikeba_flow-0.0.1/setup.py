import setuptools

with open("README.md",'r',encoding='utf-8') as fh:
    long_description=fh.read()

setuptools.setup(
    name="luotianhang_kaikeba_flow",
    version='0.0.1',
    author="luotianhang",
    author_email="673567903@qq.com",
    description="this is a test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",



)