from setuptools import setup


# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    set_requires=[
        'setuptools_scm',
    ],
    use_scm_version={
        'write_to': 'xotes/__version__.py',
    },

    name='xotes',
    description='personal note management system.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jameson Graef Rollins',
    author_email='jrollins@finestructure.net',
    url='https://gitlab.com/jrollins/xotes',
    license='GPL-3.0-or-later',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=[
        'xotes'
    ],
    install_requires=[
        'dateutil',
        'git',
        'pyyaml',
        'urwid',
        'xapian',
        ],
    entry_points={
        'console_scripts': [
            'xotes = xotes.__main__:main',
        ],
    },
)
