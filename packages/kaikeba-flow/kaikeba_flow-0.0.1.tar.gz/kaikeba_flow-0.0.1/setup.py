import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kaikeba_flow", # Replace with your own username
    version="0.0.1",
    author="Minchiuan Gao",
    author_email="minchiuan@zju.edu.cn",
    description="This is a mini but function completed neural networks framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)