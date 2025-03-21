# gitx Installation Guide

Installation Guide for gitx

## Prerequisites

-   [Python](https://www.python.org/) 3.9+ (version 3.12 is recommended)
-   [Git](https://git-scm.com/) (any recent version)

## Setup Guide

> [!NOTE]
> This project is currently in the development stage. This installation guide provides instructions for both using and contributing to the project.

1. Clone the repository. (If you are using a fork of the repository, replace the GitHub repo url with your own)

```sh
git clone https://github.com/bakayu/gitx.git
cd gitx
```

2. This project uses [poetry](https://python-poetry.org/) for package management. Install poetry with the following steps: (Skip this step if you have poetry installed)

    - On Linux / MacOS / WSL

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    - On Windows (powershell)

    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

    - Verify the installation with the command: (should say v2.0.0 or above)

    ```sh
    poetry --version
    ```

3. Install Project Dependencies. Inside the project directory (at root level), run the following commands:

```sh
poetry env use python3.12
poetry install --with dev
```

This should install all the necessary dependencies for the project.

4.  To activate the virtual environment created by poetry, run the following commands:

    -   On Linux / Mac / WSL

    ```sh
    eval $(poetry env activate)
    ```

    -   On Windows (powershell)

    ```powershell
    Invoke-Expression (poetry env activate)
    ```

    > [!NOTE]
    > For further information about poetry and managing environments refer to the [poetry docs](https://python-poetry.org/docs/managing-environments/).
