from setuptools import setup

setup(
    name='rebalance',
    version='0.0.1',
    author='Rodrigo Jordão',
    author_email='rodrigo.jordao@gmail.com',
    url='https://github.com/jordao76/rebalance',
    # on Windows, only numpy==1.12.1 worked
    # the (current) latest 1.13.1 didn't
    install_requires=['matplotlib==2.0.2', 'numpy==1.12.1'],
    py_modules=['rebalance'])
