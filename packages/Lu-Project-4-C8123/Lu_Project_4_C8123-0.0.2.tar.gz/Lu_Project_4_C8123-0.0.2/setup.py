import setuptools

with open("README.md", "r", encoding="UTF8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="Lu_Project_4_C8123",
  version="0.0.2",
  author="WangLu",
  author_email="p2009842@ipm.edu.mo",
  description="A example package for course project",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/Lu_Project_4_C8123",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: Free For Educational Use",
  "Operating System :: OS Independent",
  ],
)