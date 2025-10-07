# NWChemEx Common Package Components

As of Spack package repository `api: v2.0`, package repositories integrate smoothly with Python's import system and can be imported for use in other packages. This repository is a collection of helpers and abstractions for NWChemEx packages to help with maintenance and development.

## Usage

In other repositories, use the following import statement form:
```python
from spack_repo.nwchemex._common.packages.<package_name>.package import Package
# Or, more generally
from spack_repo.nwchemex._common.<module>.<path> import <desired_item>
```

For more information about importing from packages after `api:v2.0`, see Spack's [Repository Namespaces and Python](https://spack.readthedocs.io/en/latest/repositories.html#repository-namespaces-and-python).
