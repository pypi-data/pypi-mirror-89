
import setuptools

setuptools.setup(name='choochoo',
                 packages=setuptools.find_packages(),
                 version='0.38.2',
                 author='andrew cooke',
                 author_email='andrew@acooke.org',
                 description='Data Science for Training',
                 url='https://github.com/andrewcooke/choochoo',
                 long_description='''
# Choochoo (ch2)

An **open**, **hackable** and **free** training diary.

See [documentation](https://andrewcooke.github.io/choochoo/) for full
details.

Source and screenshots on [github](https://github.com/andrewcooke/choochoo).
                 ''',
                 long_description_content_type='text/markdown',
                 include_package_data=True,
                 install_requires=[
                     'bokeh==2.2.3',
                     'cachetools',
                     'colorama',
                     'colorlog',
                     'geoalchemy2',
                     'nbformat==5.0.8',   # https://github.com/jupyter/nbformat/issues/200
                     'jupyter',
                     'matplotlib',
                     'numpy',
                     'openpyxl',
                     'pandas',
                     'pendulum',
                     'psutil',
                     'psycopg2',
                     'pyGeoTile',
                     'pyproj',
                     'rasterio',
                     'requests',
                     'scipy',
                     'shapely',
                     'sklearn',
                     'sqlalchemy-utils',
                     'sqlalchemy==1.3.20',
                     'uritools',
                     'werkzeug',
                     ],
                 entry_points={
                     'console_scripts': [
                         'ch2 = ch2:main',
                     ],
                 },
                 classifiers=(
                     "Programming Language :: Python :: 3.8",
                     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                     "Operating System :: OS Independent",
                     "Development Status :: 4 - Beta",
                 ),
                 )

