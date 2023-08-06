from setuptools import setup, find_packages
from os import path, getenv
from sys import exit
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUGFIX = 6
VERSION_STRING = "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_BUGFIX)

TAG_ENV_VARIABLE = 'CIRCLE_TAG'
TAG_VERSION_PREFIX = "video-latency-test_"

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

packages = ['numpy', 'nptyping', 'func_timeout']

try:
    import cv2
except ImportError:
    packages.append('opencv-python')


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our VERSION_STRING"""
    description = 'verify that the git tag matches our VERSION_STRING'

    def run(self):
        tag = getenv(TAG_ENV_VARIABLE, "")
        # Make sure the tag starts with "video-latency-test_"
        if not tag.startswith(TAG_VERSION_PREFIX):
            info = "Git tag: {0} is not formatted correctly".format(
                tag
            )
            exit(info)
        # Make sure the version after "video-latency-test-_" matches our VERSION_STRING
        if tag[len(TAG_VERSION_PREFIX):] != VERSION_STRING:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION_STRING
            )
            exit(info)


setup(
    name='video-latency-test',
    version=VERSION_STRING,
    description='A simple test for detecting video latency',  # Optional
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/pseudodesign/video-latency-test',
    author='PseudoDesign',
    author_email='info@pseudo.design',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=packages,
    extras_require={
        'test': ['coverage', 'codecov', 'pyfakefs'],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={

    },
    entry_points={
        'console_scripts': [
            'video-latency-test=video_latency_test:cmdline',
        ],
    },
    cmdclass={
        'verify_tag': VerifyVersionCommand,
    }
)