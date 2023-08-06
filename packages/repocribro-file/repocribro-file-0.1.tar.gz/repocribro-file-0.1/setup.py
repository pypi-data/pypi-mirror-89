from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='repocribro-file',
    version='0.1',
    keywords='github repositories sieve projects community',
    description='Repocribro extension allowing getting repo information from defined file',
    long_description=long_description,
    author='Marek Suchánek',
    author_email='suchama4@fit.cvut.cz',
    license='MIT',
    url='https://github.com/MarekSuchanek/repocribro-file',
    zip_safe=False,
    packages=find_packages(),
    package_data={
        'repocribro_file': [
            'templates/core/repo/*.html',
        ]
    },
    entry_points={
        'repocribro.ext': [
            'repocribro-file = repocribro_file:make_extension'
        ]
    },
    install_requires=[
        'repocribro',
        'flask'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
    ],
)
