try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description':'MockCraft Python',
    'author':'Nicolas Lau',
    'url':'http://python.mockcraft.art',
    'download_url':'http://python.mockcraft.art/app',
    'author_email':'nicolaslau@outlook.com',
    'version':'0.1',
    'install_requires':['nose'],
    'packages':['MockCraftPython'],
    'scripts':[],
    'name':'MockCraftPython'
}

setup(**config)