from setuptools import setup

setup(
    name='py3mschap',
    version='0.1',
    packages=['py3mschap'],
    url='https://github.com/astibal/py3mschap',
    license='LGPL',
    author='Ales Stibal',
    author_email='astib@mag0.net',
    description='python3 mschap module', long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta', 'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6', 'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['mschap','mschapv1', 'mschapv2','py3mschap'],
    long_description_content_type='text/markdown'
)
