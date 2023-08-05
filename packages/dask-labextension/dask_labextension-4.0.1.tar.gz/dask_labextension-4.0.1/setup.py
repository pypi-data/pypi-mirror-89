"""
Setup module for the dask_labextension
"""
import setuptools
from setupbase import create_cmdclass, ensure_python, find_packages

import os.path

import versioneer

data_files_spec = [
    (
        "etc/jupyter/jupyter_notebook_config.d",
        "jupyter-config/jupyter_notebook_config.d",
        "dask_labextension.json",
    )
]

package_data_spec = {"dask_labextension": ["*.yaml"]}


cmdclass = versioneer.get_cmdclass(
    create_cmdclass(
        package_data_spec=package_data_spec, data_files_spec=data_files_spec
    )
)


with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"),
    encoding="utf-8",
) as f:
    long_description = f.read()

VERSION = versioneer.get_version()

setup_dict = dict(
    name="dask_labextension",
    version=VERSION,
    description="A Jupyter Notebook server extension manages Dask clusters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    cmdclass=cmdclass,
    include_package_data=True,
    author="Jupyter Development Team",
    author_email="jupyter@googlegroups.com",
    url="http://jupyter.org",
    license="BSD",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "Dask"],
    python_requires=">=3.5",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "bokeh >=1.0.0,!=2.0.0",
        "distributed>=1.24.1",
        "notebook>=4.3.1",
        "jupyter-server-proxy>=1.3.2",
    ],
)

try:
    ensure_python(setup_dict["python_requires"].split(","))
except ValueError as e:
    raise ValueError(
        "{:s}, to use {} you must use python {} ".format(
            e, setup_dict["name"], setup_dict["python_requires"]
        )
    )

setuptools.setup(**setup_dict)
