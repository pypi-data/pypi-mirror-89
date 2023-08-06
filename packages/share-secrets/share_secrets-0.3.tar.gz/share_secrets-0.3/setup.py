from distutils.core import setup
setup(
  name = 'share_secrets',         
  packages = ['share_secrets'],   
  version = '0.3',    
  license='GPLv3',        
  description = 'share secrets with ease.', 
  long_description='''A simple secret sharing tool made in python3 as a student Project , It uses Repeated Encryption using Modular addition
  of one time generated random key with size equal to data fed as input and data itself , so that even for same data fed as input in each
  attempt , secret codes splitted by the program will be different. Even if one of the generated secret backup codes is lost then the secret data
  will be lost forever...  ''' ,
  author = 'Anish M',                  
  author_email = 'aneesh25861@gmail.com',     
  url = 'https://github.com/anish-m-code/share_secret',  
  download_url = 'https://github.com/Anish-M-code/share_secret/archive/v0.3.tar.gz',    
  keywords = ['Secret sharing', 'cryptography'],  
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

