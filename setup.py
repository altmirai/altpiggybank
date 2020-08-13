from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['click', 'colorama', 'requests', 'ecdsa', 'base58']

setup(
    author="Altmirai LLC",
    author_email='kyle.stewart@altmirai.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A command line tool that provides the functionality to use cloud HSM services as a bitcoin wallet.",
    name='altpiggybank',
    version='0.0.1',
    py_modules=['altpiggybank'],
    packages=find_packages(exclude=[
        'docs',
        'tests',
    ]),
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points='''
        [console_scripts]
        piggy=src.routes:main''',
    url='https://github.com/altmirai/altpiggybank',
    keywords='altpiggybank')
