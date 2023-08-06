from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='repocribro_badges',
    version='0.1',
    keywords='repocribro badges repo github',
    description='Extension of repocribro for assigning badges to repositories',
    long_description=long_description,
    author='Marek Suchánek',
    author_email='suchama4@fit.cvut.cz',
    license='MIT',
    url='https://github.com/MarekSuchanek/repocribro-badges',
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'repocribro.ext': [
            'repocribro-badges = repocribro_badges:make_extension'
        ]
    },
    install_requires=[
        'repocribro'
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