from setuptools import setup

setup(name='clean_folder',
      version='1.0.0',
      description='Sorts and cleans the folder',
      url='https://github.com/Yuliia-Vogel/sorter_v2/tree/master',
      author='Yuliia Melnychenko',
      author_email='arwen.vogel@gmail.com',
      license='MIT',
      packages=['clean_folder'],
      install_requires=[],
      entry_points={'console_scripts': ['clean-folder = clean_folder.main:main']})
