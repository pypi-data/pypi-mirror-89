from setuptools import setup, find_packages
 
 
 
setup(name='S570',
 
      version='1.1',
 
      #url='https://github.com/the-gigi/conman',
 
      license='MIT',
 
      author='Tigran MKrtchyan',
 
      author_email='tigran.mkrt.bibi@gmail.com',
 
      description='GPL570 platform microarray analyse files',
 
      packages=find_packages(exclude=['tests']),
 
      #long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=["progress==1.5","matplotlib==3.1.0","numpy==1.16.4","pandas==0.24.2","scipy==1.3.0"],
      include_package_data=True,
      #test_suite='nose.collector'
      )