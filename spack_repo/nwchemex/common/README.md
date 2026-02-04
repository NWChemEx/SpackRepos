<!--
  ~ Copyright 2026 NWChemEx-Project
  ~
  ~ Licensed under the Apache License, Version 2.0 (the "License");
  ~ you may not use this file except in compliance with the License.
  ~ You may obtain a copy of the License at
  ~
  ~ http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing, software
  ~ distributed under the License is distributed on an "AS IS" BASIS,
  ~ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ~ See the License for the specific language governing permissions and
  ~ limitations under the License.
-->

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
