import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

project_urls = {
  'Source Code': 'https://github.com/awesome-patent-mining/sMPA-documentation/tree/master/sMPA',
  'Documentation': 'https://smpa-documentation.readthedocs.io/en/latest/'
}
setuptools.setup(
    name="sMPA", # Replace with your own username
    version="1.0",
    author="Liang Chen",
    author_email="25565853@qq.com",
    description="A semantic path anlalysis toolkit",
	long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/awesome-patent-mining/sMPA-documentation",
    packages=setuptools.find_packages(),
	project_urls = project_urls,
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7.0',
	
)