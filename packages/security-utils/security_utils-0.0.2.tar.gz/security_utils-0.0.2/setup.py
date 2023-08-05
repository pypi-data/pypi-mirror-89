from setuptools import setup, find_packages
 
classifiers = []
 
setup(
  name='security_utils',
  version='0.0.2',
  description='Security utils',
  long_description="Security utils",
  url='',  
  author='Alex Demure',
  author_email='alexanderdemure@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='itsdangerous',
  packages=find_packages(),
  install_requires=[
    'itsdangerous>=1.1.0'
  ],
  dependency_links=['https://github.com/AlexDemure/security_utils']
)
