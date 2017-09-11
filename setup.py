from setuptools import setup, find_packages

setup(
    name='rebalance',
    description='Exchange-Traded Funds (ETFs) portfolio rebalancing',
    version='0.0.1',
    author='Rodrigo Jordão',
    author_email='rodrigo.jordao@gmail.com',
    url='https://github.com/jordao76/rebalance',
    license='MIT',
    install_requires=['matplotlib','requests'],
    test_suite='tests',
    packages = find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'])
