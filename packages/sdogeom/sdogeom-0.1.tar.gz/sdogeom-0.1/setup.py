from setuptools import setup

setup(name='sdogeom',
      version='0.1',
      description='A module for reading 3D SDO_GEOMETRY objects from Oracle Spatial',
      url='http://github.com/ghareth/sdogeom',
      author='Gareth Boyes',
      author_email='sdogeom@gxbis.com',
      license='MIT',
      py_modules=['sdogeom/sdogeom'],
      install_requires=['numpy', 'euclid3', 'pandas'],
      python_requires='>=3.6',
      zip_safe=False)