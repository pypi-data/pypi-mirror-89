
from distutils.core import setup
setup(
  name = 'TOPSIS-Tanisha-101803042',         
  packages = ['TOPSIS-Tanisha-101803042'],   
  version = '1.0',      
  license='MIT',        
  description = 'Topsis Score and Rank generator',   
  long_description=open("README.md").read(),
  long_description_content_type='text/markdown',
  author = 'Tanisha Garg',                   
  author_email = 'tgarg_be18@thapar.edu',      
  url = 'https://github.com/Tanisha1508/TOPSIS-Tanisha-101803042',   
  download_url = 'https://github.com/Tanisha1508/TOPSIS-Tanisha-101803042/archive/1.0.tar.gz',    
  keywords = ['topsis', 'topsis score', 'rank','Thapar'],   
  install_requires=['numpy','pandas' ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
  ],
)
