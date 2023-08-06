from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='argsls',
  version='0.0.1',
  description='Basic argument functions.',
  long_description=open('README.md').read(),
  author='Crow Randalf',
  author_email='birdpeople16@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='args', 
  packages=find_packages(),
  install_requires=[''] 
)