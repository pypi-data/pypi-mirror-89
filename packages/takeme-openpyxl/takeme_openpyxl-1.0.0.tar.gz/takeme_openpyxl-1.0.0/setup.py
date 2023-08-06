import setuptools

with open('README.md') as readme_file:
    README = readme_file.read()

setuptools.setup(
    name='takeme_openpyxl',
    version='1.0.0',
    description='Python Wrapper for openpyxl',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'openpyxl'
    ],
    keywords='openpyxl excel TakeMe',
    url='https://github.com/takeme-pay/openpyxl',
    author='Yukitaka Maeda',
    author_email='yukitaka.maeda@takeme.com',
    license='GPLv3+',
    packages=setuptools.find_packages(),
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)

