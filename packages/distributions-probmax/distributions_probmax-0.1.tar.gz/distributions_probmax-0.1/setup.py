from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(name='distributions_probmax',
      version='0.1',
      description='Gaussian and binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['distributions_probmax'],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)