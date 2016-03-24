from distutils.core import setup, Extension

define_macros = [('VOID', 'void'),
                 ('REAL', 'double'),
                 ('NO_TIMER', 1),
                 ('TRILIBRARY', 1),
                 ('ANSI_DECLARATORS', 1),
                 ('EXTERNAL_TEST',1)]

setup(name='triangle',
    packages=['triangle'],
    package_dir={'triangle':'triangle'},
    package_data={'triangle':['data/*.node',
                             'data/*.ele',
                             'data/*.poly',
                             'data/*.area',
                             'data/*.edge',
                             'data/*.neigh']},
    version='2015.03.28',
    description='Python binding to the triangle library',
    author='Dzhelil Rufat',
    author_email='drufat@caltech.edu',
    license='GNU LGPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    url='http://dzhelil.info/triangle',
    requires = ['numpy(>=1.5.0)'],
    ext_modules=[
                 Extension('triangle.libtriangle', ['c/triangle.c', 'c/external_test.c', ],
                           include_dirs = ['c'],
                           define_macros = define_macros)
    ]
)
