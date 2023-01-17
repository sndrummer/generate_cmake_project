# Generate C++ CMake Project From Template

Python script that pulls CMake C++ Project template from `https://github.com/sndrummer/cmake_cpp_basic_template.git` and generates a CMake git project with the project name that is provided.

### Requirements
[GitPython](https://gitpython.readthedocs.io/en/stable/) must be installed.

### Usage
```bash
usage: generate_cmake_project.py [-h] [--gcc-version GCC_VERSION] project_name

positional arguments:
  project_name          The project name

options:
  -h, --help            show this help message and exit
  --gcc-version GCC_VERSION
                        specify the gcc version that should be used
```
