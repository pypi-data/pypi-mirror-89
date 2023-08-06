from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Sh0rt',
  version='0.0.1',
  description='Shortner a url via this libary we offer many services',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  #url='https://github.com/Y1z1n/MultiDownloader',  
  author='Yazan Talib',
  author_email='y1z1n.xx@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='', 
  packages=find_packages("Sh0rt"),
  install_requires=['requests'] 
)
