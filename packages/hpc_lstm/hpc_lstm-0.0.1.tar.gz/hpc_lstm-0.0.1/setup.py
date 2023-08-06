import setuptools
from setuptools import setup, find_packages
import os
import glob
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

find_packages(where='.', exclude=(), include=('*',))

include_dirs = os.path.dirname(os.path.abspath(__file__))

setup(
    name='hpc_lstm', # module name
    version='0.0.1',   # 包版本
    ext_modules=[
        CUDAExtension('lstm', sources=['lstm.cu'], include_dirs=[include_dirs]),
        CUDAExtension('mm', sources=['mm.cu'], include_dirs=[include_dirs]),
        CUDAExtension('ln', sources=['ln.cu'], include_dirs=[include_dirs]),
        ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
