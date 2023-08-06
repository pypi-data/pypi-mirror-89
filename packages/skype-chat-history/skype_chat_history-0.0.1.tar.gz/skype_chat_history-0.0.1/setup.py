from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: POSIX :: Linux",
    "License :: OSI Approved :: The Unlicense (Unlicense)",
   "Programming Language :: Python :: 3.9"


]

setup(name ="skype_chat_history",
      version = "0.0.1",
      description = "Skype Chat History Extractor",
      long_description = open("README.rst").read() + "\n\n" + open("CHANGELOG.txt").read(),
      url="http://pythoncasovi.com",
      author = "Darko Dekan",
      author_email = "darko.dekan@protonmail.com",
      license="The Unlicense (Unlicense)",
      classifiers=classifiers,
      keywords=["skype", "chat", "history", "parse", "extract", "json"],
      packages=find_packages(),
      install_requires=['json']
)