from setuptools import setup, find_packages
 

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='PyAcademy',
  version='0.0.3',
  description='Academic Helper',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/chinkushah/PyAcademy.git',  
  author='Rohan Shah and Gaurav Thakur',
  author_email='rohan.h.shah.03@gmail.com, gaugau939@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='education', 
  packages=find_packages(),
  install_requires=['sympy', 'matplotlib'] 
)