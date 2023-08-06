from setuptools import find_packages, setup

setup (name = 'xdo',
       version = '0.5',
       author = 'Daniel Kahn Gillmor',
       author_email = 'dkg@fifthhorseman.net',
       license = 'BSD',
       packages=find_packages(),
       description = 'simulate X11 keyboard/mouse input (bindings for libxdo)',
       classifiers=[
           "License :: OSI Approved :: BSD License",  # 2-clause

           # "Development Status :: 1 - Planning",
           # "Development Status :: 2 - Pre-Alpha",
           # "Development Status :: 3 - Alpha",
           "Development Status :: 4 - Beta",
           # "Development Status :: 5 - Production/Stable",
           # "Development Status :: 6 - Mature",
           # "Development Status :: 7 - Inactive",

           "Programming Language :: Python :: 3.4",
           "Programming Language :: Python :: 3.5",
           "Programming Language :: Python :: 3.6",
           "Programming Language :: Python :: 3.7",
           "Programming Language :: Python :: 3.8",
           "Programming Language :: Python :: 3.9",

           # Only CPython is supported at the moment
           "Programming Language :: Python :: Implementation :: CPython",
           # "Programming Language :: Python :: Implementation :: PyPy",
       ],
       package_data={'': ['README', 'COPYING']})

