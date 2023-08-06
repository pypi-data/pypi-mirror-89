from setuptools import setup, Extension
import sys

with open('README') as file:
    long_description = file.read()


if sys.version_info.major==2:
    setup(name = "Surpriser",
          version = "1.2.5",
          description = "Surpriser object and some functions.",
          long_description = long_description,
          url = "https://pypi.org/project/Surpriser/",
          author = "Daniel Gamermann",
          author_email = "danielg@if.ufrgs.br",
          license = "",
          package_dir={'Surpriser' : 'Surpriser2'},
          packages=['Surpriser'],
          package_data={'Surpriser': ['data/*.txt', 'data/*.dat']},
          ext_modules=[Extension("Surpriser.surprise", sources=["Surpriser2/csources/_Surprise.c", "Surpriser2/csources/randoms.c", "Surpriser2/csources/surprise.c"]), 
                       Extension("Surpriser.randoms", sources=["Surpriser2/csources/_Uts.c", "Surpriser2/csources/randoms.c"])],
          requires = [],
          classifiers=[
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 3',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Operating System :: OS Independent',
              'Intended Audience :: Science/Research',
              'Intended Audience :: End Users/Desktop',
              'Intended Audience :: Developers',
              'Topic :: Scientific/Engineering :: Physics',
              'Topic :: Scientific/Engineering :: Bio-Informatics',
              'Topic :: Scientific/Engineering :: Chemistry',
              'Topic :: Scientific/Engineering :: Mathematics',
              ])
elif sys.version_info.major==3:
    setup(name = "Surpriser",
          version = "1.2.5",
          description = "Surpriser object and some functions.",
          long_description = long_description,
          url = "https://pypi.org/project/Surpriser/",
          author = "Daniel Gamermann",
          author_email = "danielg@if.ufrgs.br",
          license = "",
          package_dir={'Surpriser' : 'Surpriser3'},
          packages=['Surpriser'],
          package_data={'Surpriser': ['data/*.txt', 'data/*.dat']},
          ext_modules=[Extension("Surpriser.surprise", sources=["Surpriser3/csources/_Surprise.c", "Surpriser3/csources/randoms.c", "Surpriser3/csources/surprise.c"]), 
                       Extension("Surpriser.randoms", sources=["Surpriser3/csources/_Uts.c", "Surpriser3/csources/randoms.c"])],
          requires = [],
          classifiers=[
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 3',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Operating System :: OS Independent',
              'Intended Audience :: Science/Research',
              'Intended Audience :: End Users/Desktop',
              'Intended Audience :: Developers',
              'Topic :: Scientific/Engineering :: Physics',
              'Topic :: Scientific/Engineering :: Bio-Informatics',
              'Topic :: Scientific/Engineering :: Chemistry',
              'Topic :: Scientific/Engineering :: Mathematics',
              ])



