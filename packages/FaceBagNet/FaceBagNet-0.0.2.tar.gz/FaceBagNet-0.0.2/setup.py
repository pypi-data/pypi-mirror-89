from distutils.core import setup

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(

    name = 'FaceBagNet',

    version = '0.0.2',

    keywords = ('活体检测', '计算机视觉'),

    description = '输入一张图片，输出这个图片上的人是活体还是非活体',
    long_description=long_description,

    license = 'MIT',

    author = 'zhaomingming',
    url='https://github.com/pypa/sampleproject',  # Optional

    author_email = '13271929138@163.com',
    #package_dir={'': 'src'},  
    #packages = find_packages(),
    #py_modules=['nacla.nacla']
    packages=find_packages(),  # Required
    python_requires='>=3.5, <4',
     # If there are data files included in your packages that need to be
    # installed, specify them here.
    #package_data={  # Optional
    #    'src/model': ['rnn.pth'],
    #},
    include_package_data=True,
    install_requires=['imgarg'],
    #data_files=[('model', ['nacla/model/rnn.pth'])],

    #py_modules=['nacla.nacla']
    #packages=find_packages(where='nacla'),  # Required

)

