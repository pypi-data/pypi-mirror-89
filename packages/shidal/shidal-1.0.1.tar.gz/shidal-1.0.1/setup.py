from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
   name='shidal',
   version='1.0.1',
   description='Simple hid action listener',
   long_description=long_description,
   author='dataniklas',
   author_email='51879435+data-niklas@users.noreply.github.com',
   packages=['shidal'],  #same as name
   install_requires=['hid'], #external packages as dependencies
)
