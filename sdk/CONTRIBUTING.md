## Contributing to the `kfp` SDK

For developing KFP v2 SDK, use the `master` branch.

For developing KFP v1 SDK, use the [sdk/release-1.8 branch](https://github.com/kubeflow/pipelines/tree/sdk/release-1.8).

For general contribution guidelines including pull request conventions, see [pipelines/CONTRIBUTING.md](https://github.com/kubeflow/pipelines/blob/master/CONTRIBUTING.md).

### Pre-requisites 

Clone the repo: 

```bash
git clone https://github.com/kubeflow/pipelines.git && cd pipelines
```

We suggest using a tool like [virtual env](https://docs.python.org/3/library/venv.html) or something similar for isolating 
your environment and/or packages for you development environment. For this setup we'll stick with virtual env. 

For supported python versions, see the sdk [pyproject.toml](https://github.com/kubeflow/pipelines/blob/master/sdk/python/pyproject.toml). 

```bash
# optional, replace with your tool of choice
python -m venv env && source ./env/bin/activate
```

As with any Python package development, first ensure [wheels and setuptools](https://realpython.com/python-wheels/) are installed:

```bash
python -m pip install -U pip wheel setuptools
```

All sdk development requirement versions are pinned in [requirements-dev.txt](https://github.com/kubeflow/pipelines/blob/master/sdk/python/requirements-dev.txt).

```bash
pip install -r sdk/python/requirements-dev.txt
```

Install the SDK in development mode using the `--editable` or `-e` flag. This will allow you to implement and test changes iteratively.
Read more about it [here](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).

```bash
pip install -e sdk/python
```

The KFP SDK includes the following components that were previously separate packages but are now consolidated into `kfp`:
- **`kfp.pipeline_spec`**: Protocol buffer definitions for KFP pipeline specifications
- **`kfp.server_api`**: Client API for communicating with the KFP backend server
- **`kfp.kubernetes`**: Kubernetes-specific executor configurations

### Generating Protocol Buffer Code

The SDK relies on protocol buffer code generated from the KFP API definitions. To regenerate the protobuf code (e.g., after updating API definitions):

```bash
cd sdk/python
./generate_protos.sh
```

This script generates Python code for:
- `kfp.pipeline_spec` from `api/v2alpha1/pipeline_spec.proto`
- `kfp.kubernetes` from `kubernetes_platform/proto/kubernetes_executor_config.proto`

### Building Distribution Packages

To build wheel and source distributions for the KFP SDK:

```bash
cd sdk/python
python -m build
```

This will create distribution files in the `dist/` directory:
- `kfp-X.Y.Z-py3-none-any.whl` (wheel distribution)
- `kfp-X.Y.Z.tar.gz` (source distribution)

Note: You may need to install the `build` package first: `pip install build`

### Testing
We suggest running unit tests using [`pytest`](https://docs.pytest.org/en/7.1.x/). From the project root, the following runs all KFP SDK unit tests:
```sh
pytest
```

To run tests in parallel for faster execution, you can run the tests using the `pytest-xdist` plugin:

```sh
pytest -n auto
```

### Code Style
Dependencies for code style checks/changes can be found in the kfp SDK [requirements-dev.txt](https://github.com/kubeflow/pipelines/blob/master/sdk/python/requirements-dev.txt).


#### Style Guide [Required]
The KFP SDK follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

#### Formatting [Required]
Please format your code using [yapf](https://github.com/google/yapf) according to the [`.style.yapf`](https://github.com/kubeflow/pipelines/blob/master/.style.yapf) file.

From the project root, run the following code to format your code:
```sh
yapf --in-place --recursive ./sdk/python
```

#### Docformatter [Required]
We encourage you to lint your docstrings using [docformatter](https://github.com/PyCQA/docformatter).

From the project root, run the following code to lint your docstrings:
```sh
docformatter --in-place --recursive ./sdk/python
```

#### Formatting Imports [Required]
Please organize your imports using [isort](https://pycqa.github.io/isort/index.html) according to the [`.isort.cfg`](https://github.com/kubeflow/pipelines/blob/master/.isort.cfg) file.

From the project root, run the following code to format your code:
```sh
isort sdk/python
```

#### Pylint [Encouraged]
We encourage you to lint your code using [pylint](https://pylint.org/) according to the project [`.pylintrc`](https://github.com/kubeflow/pipelines/blob/master/.pylintrc) file.

From the project root, run the following code to lint your code:
```sh
pylint ./sdk/python/kfp
```

Note: `kfp` is not currently fully pylint-compliant. Consider substituting the path argument with the files touched by your development.

#### Static Type Checking [Encouraged]
Please use [mypy](https://mypy.readthedocs.io/en/stable/) to check your type annotations.

From the project root, run the following code to lint your docstrings:
```sh
mypy ./sdk/python/kfp/
```
Note: `kfp` is not currently fully mypy-compliant. Consider substituting the path argument with the files touched by your development.


#### Pre-commit [Recommended]
Consider using [`pre-commit`](https://github.com/pre-commit/pre-commit) with the provided [`.pre-commit-config.yaml`](https://github.com/kubeflow/pipelines/blob/master/.pre-commit-config.yaml) to implement the above changes:
```sh
pre-commit install
```
