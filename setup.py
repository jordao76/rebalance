from setuptools import setup

setup(
    name='rebalance',
    description='Exchange-Traded Funds (ETFs) portfolio rebalancing',
    version='0.0.1',
    author='Rodrigo Jordão',
    author_email='rodrigo.jordao@gmail.com',
    url='https://github.com/jordao76/rebalance',
    license='MIT',
    install_requires=['matplotlib'],
    test_suite='test_rebalance',
    py_modules=['rebalance'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'])
