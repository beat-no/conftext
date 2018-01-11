from setuptools import setup

setup(
    name='conftext',
    version='0.0.1',
    
    install_requires=['invoke'],
    
    extras_require={
        'dev': [
            'pytest',
        ]
    },
    
    py_modules=['conftext'],
    
    entry_points={
        'console_scripts': [
            'conftext = conftext:program.run',
        ]
    },
    
    author='Øystein S. Haaland',
    author_email='oystein@beat.no',
    description='conftext - helper for managing configuration contexts',
    url='https://gitlab.dev.beat.no/backend/conftext'
)
