from setuptools import setup, find_packages
 
classifiers = []
 
setup(
  name='yandex_object_storage',
  version='0.0.1',
  description='Yandex object storage',
  long_description="Security utils",
  url='',  
  author='Alex Demure',
  author_email='alexanderdemure@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='yandex',
  packages=find_packages(),
  install_requires=[
    'boto3>=1.16.25'
  ],
  dependency_links=['https://github.com/AlexDemure/security_utils']
)
