from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='simplelinearregression',
    version='0.0.1',
    description='A very linear regression package',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Manas Kulkarni',
    author_email='mkulkar2@stevens.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='regression',
    packages=find_packages(),
    install_requires=['']
)
