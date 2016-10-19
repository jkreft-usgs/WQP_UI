"""
Created on Aug 26, 2016

@author: ayan
"""
import os
import ConfigParser
from setuptools import setup, find_packages


BUMPVERSION_CFG = '.bumpversion.cfg'


def get_package_version():
    """
    Read the .bumpversion.cfg file return
    the current version number listed therein.
    Version number only needs to be maintained
    in the .bumpversion.cfg file.

    :return: current package version
    :rtype: str

    """
    config = ConfigParser.ConfigParser()
    config.read(BUMPVERSION_CFG)
    current_version = config.get('bumpversion', 'current_version')
    return current_version


def read_requirements():
    """
    Get application requirements from
    the requirements.txt file.

    :return: portal_ui Python requirements
    :rtype: list

    """
    with open('requirements.txt', 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements if r.find('git+') != 0]
    dependency_links = [r.strip() for r in requirements if r.find('git+') == 0]
    return {'install_requires': install_requires, 'dependency_links': dependency_links}


def read(filepath):
    """
    Read the contents from a file.

    :param str filepath: path to the file to be read
    :return: file contents
    :rtype: str

    """
    with open(filepath, 'r') as f:
        content = f.read()
    return content


def identify_data_files(directory_names):
    """
    Recursively introspect the contents
    of a directory. Once the contents have been
    introspected, generate a list directories and
    sub-directories with their contents as lists.

    :param list directory_names: absolute or relative name to directories
    :return: all contents of the directories as a list of tuples
    :rtype: list

    """
    directory_data_files = []
    for directory_name in directory_names:
        for root, dirs, files in os.walk(directory_name):
            pathnames = [os.path.abspath(os.path.join(root, filename)) for filename in files]
            data_file_element = (root, pathnames)
            directory_data_files.append(data_file_element)
    return directory_data_files


parsed_requirements = read_requirements()
data_files = identify_data_files(['static'])
setup(name='usgs_flask_wqp_ui',
      version=get_package_version(),
      description='USGS Water Quality Portal User Interface',
      author='Mary Bucknell, James Kreft, Andrew Yan',
      author_email='jkreft@usgs.gov',
      packages=find_packages(),
      include_package_data=True,
      long_description=read('README.md'),
      install_requires=parsed_requirements['install_requires'],
      tests_require=parsed_requirements['install_requires'],
      platforms='any',
      test_suite='nose.collector',
      zip_safe=False,
      # include the tier agnostic configuration file in the distributable
      # the file gets placed in site-packages upon dist installation
      py_modules=['config'],
      # include static files in the distributable
      # they will appear in the root of the virtualenv upon dist installation
      data_files=data_files
      )