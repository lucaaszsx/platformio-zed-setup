# platformio-zed-setup

This repository contains a tool built with Python called **Zedio**, that provides an interface for using PlatformIO in a integrated way with **[Zed Editor](https://zed.dev)**. This tool makes building embedded systems with Zed easier, as it uses the builtin [tasks](https://zed.dev/docs/tasks) that Zed provides to abstract away the CLI-based workflow.

## Installation

Python 3.14 or newer ([uv](https://docs.astral.sh/uv/) handles it automatically)

Use `curl` to download the setup script and execute it with `sh`:

```bash
$ curl -LsSf https://raw.githubusercontent.com/lucaaszsx/platformio-zed-setup/refs/heads/main/setup.sh | sh
```

## Usage

The setup script that you have seen in [installation](#installation) section will automatically setup Zed tasks to allow you use Zedio and create your embedded systems on your editor. However, you can also use the CLI tool directly, since its a binary executable installed into your system by **uv** during the setup step.

To get a full specification of the CLI commands provided by Zedio, just run the following command:

```bash
zedio --help
```

## Building

To build this project into your own machine, follow these steps:

1. Clone the repository

```bash
$ git clone https://github.com/lucaaszsx/platformio-zed-setup
```

2. Enter the repository folder

```bash
$ cd platformio-zed-setup
```

3. Run Zedio commands with `uv` (dependencies will be auto-installed)

```bash
$ uv run zedio --help
```

## Contributing

You can contribute in the project by sending a pull request or opening a issue in the **[GitHub repository](https://github.com/lucaaszsx/platformio-zed-setup)**.

## License

Licensed under [MIT License](./LICENSE)