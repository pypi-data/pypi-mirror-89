import setuptools
from distutils.core import setup
 
setup(name="sxm_converter", version="0.2", description="convert .sxm(Nanonis instruments) to picture easily", author="CoccaGuo", author_email="guojiadong@bnu.edu.cn", setup_requires=['wheel'], py_modules=['sxm_converter.converter', 'sxm_converter.sxm2png'])