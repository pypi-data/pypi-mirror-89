import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='casex',
      version='1.0.1',
      description='Casulty Expection toolbox',
      long_description=long_description,
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
      ],
      author='Anders la Cour-Harbo et al',
      author_email='alc@es.aau.dk',
      license='CC-BY-4.0',
      packages=setuptools.find_packages(),
      python_requires=">=3.6",
      zip_safe=False)
