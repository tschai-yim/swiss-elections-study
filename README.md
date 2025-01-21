# Swiss Elections Study

## Getting started

First, create the environment from the lock file:

```sh
micromamba create --file conda-lock.yml --name heliotime-server
```

Then, activate it:

```sh
micromamba activate heliotime-server
```

> **Micromamba & PyCharm** <br>
> PyCharm currently [does not support Mamba](https://youtrack.jetbrains.com/issue/PY-58703/Setting-interpreter-to-mamba-causes-PyCharm-to-stop-accepting-run-configurations). As a workaround, install and use Conda in PyCharm but point it to the same environment:
>
> ```sh
> micromamba install conda-forge::conda
> ```
>
> PyCharm will be happy and you can keep using any other tool to manage the environment.

## Various commands

Update the lock file (from `environment.yml`):

```bash
conda-lock --micromamba
```
