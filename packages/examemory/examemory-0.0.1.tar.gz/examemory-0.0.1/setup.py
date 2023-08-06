import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="examemory",
    version="0.0.1",
    author="Alexander Pfefferle",
    author_email="alex@pfefferle.xyz",
    description="A small memory hacking package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexanderpfefferle/examemory",
    packages=["examemory"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
