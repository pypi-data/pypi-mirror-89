"""
Wrappers for the "DiskArbitration" framework on macOS.

These wrappers don't include documentation, please check Apple's documention
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
"""

from pyobjc_setup import setup

VERSION = '7.1'

setup(
    name="pyobjc-framework-DiskArbitration",
    description="Wrappers for the framework DiskArbitration on macOS",
    packages=["DiskArbitration"],
    version=VERSION,
    install_requires=["pyobjc-core>=" + VERSION, "pyobjc-framework-Cocoa>=" + VERSION],
    long_description=__doc__,
)
