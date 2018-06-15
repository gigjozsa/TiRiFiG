#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="TiRiFiG",
      description="A graphical user interface that allows user to TiRiFiC to modify tilted-ring parameters interactively.",
      author="Samuel Twum with MSc Supervisors",
      author_email="samueltwum1@gmail.com",
      packages=find_packages(),
      url='https://github.com/gigjozsa/samtirifik',
      download_url='https://pypi.python.org/pypi/samtirifik',
      # home_page='http://under-construction',
      license="MIT",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Topic :: Scientific/Engineering :: Visualization",
      ],
      platforms=["OS Independent"],
      install_requires=[
          "PyQt>=4",
          "numpy"],
      zip_safe=False,
      include_package_data=True,
      package_data={'TiRiFiG': ['utilities/example/n5204_lo.n5204_lo.fits',
                                'utilities/example/n5204_lo_out_00.def',
                                'utilities/icons/*.png']},
    #   entry_points={
    #       'console_scripts': [
    #           'script_name = script_name:main'
    #       ]}
      )
