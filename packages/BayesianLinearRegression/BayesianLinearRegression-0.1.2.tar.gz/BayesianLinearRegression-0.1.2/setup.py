# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 03:49:25 2020

@author: jkcle
"""
# read the contents of my README file
from os import path
this_directory = path.abspath(path.dirname("BayesianLinearRegression\\"))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

from setuptools import setup

setup(name="BayesianLinearRegression",
      version="0.1.2",
      description="Fits Linear and Logistic Regression Models using MCMC.",
      packages=["BayesianLinearRegression"],
      long_description=long_description,
      author="John Clements",
      author_email="blr.johnclements@gmail.com",
      zipsafe=False)