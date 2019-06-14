from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bracket_expansion",
    version="1.0.0",
    author="Jeremy Schulman",
    author_email="nwkautomaniac@gmail.com",
    description="string generator for bracket patterns",
    license="Apache 2.0",
    url="https://github.com/jeremyschulman/bracket_expansion",
    py_modules=['bracket_expansion'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking'
    ],
)
