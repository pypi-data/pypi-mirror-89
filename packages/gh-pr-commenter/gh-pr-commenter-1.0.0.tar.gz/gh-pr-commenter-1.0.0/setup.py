import os
import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="gh-pr-commenter",
    version="1.0.0",
    description="Simple Script to post a github comment to a given PR based on a jinja2 template",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="enen92",
    url="https://github.com/enen92/github-pr-log-commenter",
    download_url="https://github.com/enen92/github-pr-log-commenter/archive/main.zip",
    install_requires=requirements,
    python_requires=">=3.5",
    setup_requires=['setuptools>=38.6.0'],
    scripts=['gh-pr-commenter.py'],
    keywords='github pr-comment',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities"
    ] + [('Programming Language :: Python :: %s' % x) for x in '3 3.5 3.6 3.7'.split()]
)