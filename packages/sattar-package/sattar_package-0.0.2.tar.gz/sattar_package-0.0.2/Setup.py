from setuptools import setup, find_packages


setup(
    name='sattar_package',
    version='0.0.2',
    description='A simple package for Special topics-IAUN',
    long_description=open('README.txt').read(),
    url='https://www.nexinno.ir',
    author='Sattar Monejezi',
    author_email='sattarmonjezi88@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Financial and Insurance Industry'
    ],

    keywords='Special_topics_IAUN',
    packages=find_packages(),
    install_requires=["autocorrect>=0.3.0",
                      "gensim>=3.0.1",
                      "matplotlib>=2.1.0",
                      "pandas==1.1.5",
                      "pyenchant>=2.0.0",
                      "requests>=2.18.0",
                      "spaCy>=2.0.3",
                      "scikit-learn>=v0.19.1",
                      "wikipedia>=1.4.0"],


)
