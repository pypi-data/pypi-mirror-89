import setuptools
with open("DpyToolHandle/README.md","r",encoding="utf-8") as f:
  long_description=f.read()

setuptools.setup(
    name="dpytoolhandle", # Put your username here!
    version="0.0.1", # The version of your package!
    author="None", # Your name here!
    author_email="none@example.com", # Your e-mail here!
    description="Discord.py extension.", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hillo232/fun", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.6', # The version requirement for Python to run your package!
)
