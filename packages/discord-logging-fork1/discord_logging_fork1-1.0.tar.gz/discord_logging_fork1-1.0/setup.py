import setuptools  

with open("README.md", "r", encoding="utf-8") as fh:  
    long_description = fh.read()  

setuptools.setup(  
    name="discord_logging_fork1",  
    version="1.0",  
    author="kadyk_lesha",  
    author_email="novikovprjjects@gmail.com",  
    description="Transfer logs acquired by logging module to discord with webhook!",  
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    url="https://github.com/AlexNovikovRussian/discord_logging",  
    packages=setuptools.find_packages(),  
    classifiers=[  
        "Programming Language :: Python :: 3.8",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",  
    ],  
)  
