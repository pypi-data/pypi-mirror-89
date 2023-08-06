from distutils.core import setup

setup(
    name='vaslapp5generator',
    packages=['vaslapp5generator'],
    version='0.0.6',
    license='MIT',
    description='Generate vaslapp v5 entity boilerplate',
    author='Ali Farhoudi',
    author_email='af.farhoudi@gmail.com',
    url='https://github.com/vaslsolutions/vaslapp5generator',
    # download_url='https://github.com/vaslsolutions/vaslapp5generator/archive/0.0.6.zip',
    keywords=['vaslapp', 'vasl baas', 'code generator'],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'vaslapp5generator = vaslapp5generator.generator:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
    package_data={'': ['stubs/*.java']},
)
