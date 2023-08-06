import site
import sys
from setuptools import setup, find_packages


# Workaround to install in user dir but editable,
# see https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='withtray',
    version='0.1.1',
    description='Run any blocking command with systray icon',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/krisfris/withtray',
    author='Kris',
    author_email='31852063+krisfris@users.noreply.github.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click', 'pygobject', 'Pillow', 'pystray'
    ],
    entry_points='''
        [console_scripts]
        withtray=withtray.main:main
    ''',
)
