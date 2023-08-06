import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ivy_cms_unused_scanner", # Replace with your own username
    version="0.0.5",
    author="Loc Truong",
    author_email="loctvuit@gmail.com",
    description="Use this to remove unused CMS in your ivy project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrNocTV/ivy_unused_cms_scanner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
