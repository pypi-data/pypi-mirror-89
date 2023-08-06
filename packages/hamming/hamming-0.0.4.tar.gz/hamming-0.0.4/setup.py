from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 8',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='hamming',
    version='0.0.4',
    description='Hamming code generation and error detection',
    Long_description=open('README.md').read() + '\n\n'
                     + open('CHANGELOG.txt').read(),
    url='',
    author='Ambuj Dubey',
    author_email='ambujdubey2426@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='hamming code',
    packages=['hamming'],
    install_requires=['']
)
