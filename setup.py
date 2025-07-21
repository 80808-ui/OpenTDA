"""OpenTDA: Open-source Python library for topological data analysis"""
import os
import re
import sys
import numpy as np
from os.path import join as pjoin
from setuptools import setup, Extension, find_packages

# === 安全获取版本信息，避免导入未编译模块 ===
def get_version():
    """从tda/__init__.py读取版本号"""
    init_path = os.path.join(os.path.dirname(__file__), 'tda', '__init__.py')
    try:
        with open(init_path) as f:
            version_match = re.search(
                r"^__version__ = ['\"]([^'\"]*)['\"]", 
                f.read(), 
                re.M
            )
            return version_match.group(1) if version_match else "0.0.0"
    except Exception:
        return "0.0.0"  # 后备版本

NAME = "tda"
VERSION = get_version()

# === 必备包检查 ===
try:
    import Cython
    from Cython.Distutils import build_ext
    if Cython.__version__ < '0.18':
        raise ImportError()
except ImportError:
    print('Cython version 0.18 or later is required. Try "pip install cython"')
    sys.exit(1)

# === 平台特定的编译参数 ===
if sys.platform == "win32":
    extra_compile_args = ["/O2", "/arch:AVX2"]  # Windows优化和指令集
else:
    extra_compile_args = ["-O3", "-march=native"]  # Linux/Mac优化

# === 扩展模块配置 ===
extensions = [
    Extension('tda.snf',
              sources=[pjoin('tda', 'snf.pyx')],
              include_dirs=[np.get_include()],
              extra_compile_args=extra_compile_args)
]

# === 读取描述文件 ===
def read(filename):
    with open(filename, 'r', encoding='utf-8') as fi:
        return fi.read()

# === 最终安装配置 ===
setup(
    name=NAME,
    version=VERSION,
    description='Open-source Python library for topological data analysis (TDA)',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author="Brandon B",
    author_email="outlacedev@gmail.com",
    url='https://github.com/outlace/OpenTDA',
    download_url=f'https://github.com/outlace/OpenTDA/tarball/v{VERSION}',
    license='Apache License 2.0',
    packages=find_packages(),
    package_data={
        'tda': ['*.pyx', '*.pxd'],
    },
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.18',
        'scipy>=1.4',
        'matplotlib>=3.2',
        'cython>=0.18'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    zip_safe=False,
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext}
)
