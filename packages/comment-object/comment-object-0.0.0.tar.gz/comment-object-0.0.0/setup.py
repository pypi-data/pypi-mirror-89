"""
setup for comment-object
"""

from setuptools import setup, find_packages

try:
    import pathlib
    here = pathlib.Path(__file__).parent.resolve()
    # Get the long description from the README file
    long_description = (here / 'README.md').read_text(encoding='utf-8')
except ImportError:
    import os
    here = os.path.dirname(__file__)
    readme_filepath = os.path.join(here, "README.md")
    with open(readme_filepath, "r") as readme:
        long_description = readme.read()


setup(
    name='comment-object',
    version='0.0.0',
    description='An explicit object for comments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mft/comment',
    author='MATSUI Tetsushi',
    author_email='matsui.tetsushi@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords='comment',
    package_dir={'': 'src'},
    packages=["comment"],
    python_requires='>=2.7',
)
