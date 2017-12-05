from setuptools import setup, find_packages

setup(name='Khronos',
      version='0.1',
      description='Time series analytics for Python',
      author='Pierre Foret',
      author_email='pierre_foret@berkeley.edu',
      url='https://github.com/PForet/khronos',
      packages = find_packages(exclude=['*.tests*']),
      license='MIT',
      install_requires=['numpy',
			'datetime'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])