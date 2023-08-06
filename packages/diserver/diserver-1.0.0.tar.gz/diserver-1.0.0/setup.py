from setuptools import setup

setup(
    name='diserver',
    version='1.0.0',
    author="Tabacaru Eric",
    author_email="erick.8bld@gmail.com",
    description="Hot reload server for developing Discord bots!",
    url="https://github.com/erick-dsnk/discord-bot-server",
    py_modules=['disv'],
    install_requires=[
        'Click',
        'watchdog'
    ],
    entry_points='''
        [console_scripts]
        disv=disv:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)