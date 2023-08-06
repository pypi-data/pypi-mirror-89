from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: POSIX :: Linux",
    "License :: OSI Approved :: The Unlicense (Unlicense)",
   "Programming Language :: Python :: 3.9"


]

setup(name ="gigatronapi",
      version = "0.0.1",
      description = "A very basic calculator",
      long_description = open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
      url="",
      author = "Darko Dekan",
      author_email = "darko.dekan@protonmail.com",
      license="The Unlicense (Unlicense)",
      classifiers=classifiers,
      keywords="gigatron",
      packages=find_packages(),
      install_requires=['requests']
)