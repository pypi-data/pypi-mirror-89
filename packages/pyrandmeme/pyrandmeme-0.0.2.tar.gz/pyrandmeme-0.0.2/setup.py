from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pyrandmeme',
    version='0.0.2',
    description='Random memes for discord.py',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Poggy',
    author_email='poggywastaken123@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='memes',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'discord',
        'random'
    ]
)