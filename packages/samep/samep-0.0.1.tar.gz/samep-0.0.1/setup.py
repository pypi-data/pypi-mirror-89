#!/usr/bin/python3
# -*- coding: utf-8 -*-
import setuptools  

setuptools.setup(  
    name="samep",  
    version="0.0.1",  
    author="furimu",  
    description="samebotのplugin",  
    long_description="test",  
    long_description_content_type="text/markdown",
    url="https://github.com/furimu1234/same/tree/main/utils",  
    packages=setuptools.find_packages(),  
    classifiers=[  
        "Programming Language :: Python :: 3.8",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",  
    ],
    install_requires=["asyncpgw", "asyncpg", 'discord.py'],
)  