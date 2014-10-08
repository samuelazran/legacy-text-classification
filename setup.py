from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='text-classification',
    version='0.1',
    description='python packege that uses popular ML libraries such as scikit-learn to simplify text classification tasks',
	long_description=readme(),
    url='https://github.com/samuelazran/TextClassification.git',
    author='Samuel Azran',
    author_email='samuelazran@gmail.com',
    license='MIT',
	include_package_data=True,
    entry_points = {
        'console_scripts': ['predict=text_classification.command_line:predict'],
    },
    packages=['text_classification','text_classification.lib.langid'],
	package_data={'text_classification': ['*.bat']},
	install_requires=[
        'scikit-learn','dill'
    ],
	test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)