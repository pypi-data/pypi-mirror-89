import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="JinYeong Bak",
    author_email="dongdm@gmail.com",
    name='nosyupylib',
    license="MIT",
    description='NoSyu Python Library',
    version='v1.0.0',
    long_description=README,
    url='https://github.com/NoSyu/nosyupylib',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['slack', 'pymsteams'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)

"""
Source: https://towardsdatascience.com/publishing-your-own-python-package-3762f0d268ec
"""
