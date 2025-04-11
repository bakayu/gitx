# Gitx Installation Guide

Installation Guide for gitx

## Prerequisites

-   [Python](https://www.python.org/) 3.9+ (version 3.12 is recommended)
-   [Git](https://git-scm.com/) (any recent version)

## Setup Guide

> [!NOTE]
> This project is currently in the development stage. This installation guide provides instructions for both using and contributing to the project.

1. Clone the repository. (If you are using a fork of the repository, replace the GitHub repo url with your own)

    ```sh
    git clone https://github.com/gitxtui/gitx.git
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

4. To activate the virtual environment created by poetry, run the following commands:

    - On Linux / MacOS / WSL (bash)

    ```sh
    eval $(poetry env activate)
    ```

    - On Windows (powershell)

    ```powershell
    Invoke-Expression (poetry env activate)
    ```

    > [!NOTE]
    > For further information about poetry and managing environments refer to the [poetry docs](https://python-poetry.org/docs/managing-environments/).

5. To install and run the `gitx` package, run the following commands:

    ```sh
    # Install the package in development mode
    poetry install

    # Run the app using the entry point
    poetry run gitxtui # or simply `gitxtui` if already in poetry environment
    ```

6. To build the package, run:

    ```sh
    poetry build

    # This will create dist/gitxtui-<version>.tar.gz and dist/gitxtui-<version>-none-any.whl
    ```

## Running Tests

Run the test suite using pytest:

```sh
pytest
```

## Building Documentation

To build and preview the documentation locally:

```sh
mkdocs serve
```

This will start a local server at http://127.0.0.1:8000/ where you can preview your documentation.
