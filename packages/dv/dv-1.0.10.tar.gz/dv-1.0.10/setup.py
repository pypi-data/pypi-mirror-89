from setuptools import setup


def get_version_from_file():
    with open('VERSION.txt', 'r') as version_file:
        tag = version_file.read()
    return tag


setup(name='dv',
      version=get_version_from_file(),
      description='Library to connect to DV event based vision software',
      url='https://gitlab.com/inivation/dv/dv-python/',
      author='iniVation AG',
      author_email='support@inivation.com',
      license='AGPLv3',
      packages=['dv', 'dv.fb'],
      install_requires=['flatbuffers', 'numpy', 'lz4', 'zstd'],
      python_requires='>=3',
      zip_safe=False)
