from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='custom_study',
      version=__import__('custom_study').__version__,
      description='A Django admin theme with a horizontal, tabbed navigation bar',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='http://github.com/',
      author='Chris Rose',
      license='MIT',
      packages=['custom_study'],
      zip_safe=False,
      include_package_data=True,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
      )