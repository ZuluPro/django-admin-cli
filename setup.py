import os
from setuptools import setup, find_packages
import admin_cli

try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    name='django-admin-cli',
    version=admin_cli.__version__,
    url="https://github.com/ZuluPro/django-admin-cli",
    description="""""",
    long_description=long_description,
    author='ZuluPro (Anthony MONTHE)',
    author_email='anthony.monthe@gmail.com',
    license='BSD',
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
    ],
    packages=find_packages(exclude=['tests.runtests.main']),
    include_package_data=True,
    test_suite='tests.runtests.main',
    install_requires=[],
)
