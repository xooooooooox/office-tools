from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'includes': ['docxtpl', 'pandas', 'openpyxl'],
    # 如果有额外的包也要在这里声明
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)