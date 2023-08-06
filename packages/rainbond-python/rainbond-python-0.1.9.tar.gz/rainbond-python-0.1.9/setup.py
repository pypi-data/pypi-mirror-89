import setuptools
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, 'README.md')
with open('README.md', "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name='rainbond-python',
    version='0.1.9',
    description='Rainbond python cloud native development base library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/hekaiyou/rainbond-python",
    author="Kaiyou He",
    author_email="hky0313@outlook.com",
    packages=['rainbond_python', 'rainbond_python/example'],
    install_requires=[
        'pymongo'
    ],
    keywords='rainbond python cloud native',
    entry_points={
        'console_scripts': [
            'rainbond = rainbond_python.cli:main'
        ],
    },
)
