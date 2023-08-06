from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='sattar_package',
    version='0.0.12',
    description='A very basic libray',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Sattar Monjezi',
    author_email='sattarmonjezi88@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='special_topics_IAUN',
    packages=find_packages(),
    install_requires=["matplotlib==3.3.3",
                      "pandas==1.1.5",
                      "numpy>=1.1.0",
                      "scikit-learn>=v0.19.1"]
)
