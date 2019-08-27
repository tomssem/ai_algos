from setuptools import setup

setup(
    name='graph_search',
    version='0.1.0',
    author='T. F. W. Nicholson',
    author_email='tfwnicholson@gmail.com',
    packages=['graph_search', 'graph_search.test'],
    scripts=[],
    # url='none_yet',
    license='../../LICENSE',
    description='Implementation of graph search algorithms',
    long_description=open('README.md').read(),
    install_requires=[],
)
