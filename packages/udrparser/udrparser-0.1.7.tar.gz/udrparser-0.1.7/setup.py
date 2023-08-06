import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='udrparser',
     version='0.1.7',
    #  scripts=['storagemodel', 'trainmodel'] ,
     author="Arvind Ravish",
     author_email="arvind.ravish@gmail.com",
     description="A simple package to get FQDN IP addresses",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="",
     packages=['udrparser'],  #setuptools.find_packages(),
      #  py_modules=['storagemodel'],
    install_requires=[
        'pandas', 'lxml'
    ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )