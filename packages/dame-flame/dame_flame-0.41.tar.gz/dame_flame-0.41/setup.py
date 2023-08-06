import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(name='dame_flame',
      version='0.41',
      description='Causal Inference Covariate Matching',
      long_description=long_description,
      keywords='Causal Inference Matching Econometrics Data Machine Learning FLAME DAME',
      url='https://github.com/almost-matching-exactly/DAME-FLAME-Python-Package',
      author='Neha Gupta',
      author_email='neha.r.gupta@duke.edu',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'scikit-learn>=0.23.2',
          'pandas>=0.16.5',
          'numpy>=1.6.1'
      ],
     long_description_content_type="text/markdown",
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )
