from setuptools import find_packages, setup


setup(
    name='healthcheckcore',
    version='0.1',
    package_dir={'': 'src'},
    packages=['healthcheckcore'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
)
