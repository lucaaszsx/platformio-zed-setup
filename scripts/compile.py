import os
import sys

from InquirerPy.prompts.list import ListPrompt as select
from lib.common import print_success, print_warn
from lib.pio import find_project, pio_call, pio_load_conf


def main():
    project = find_project(sys.argv[0])
    conf = pio_load_conf(project)

    command = ["run"]
    use_env = os.environ["USE_ENV"] == "1"

    if use_env:
        envs = [name.removeprefix("env:") for name, _ in conf if name.startswith("env:")]

        if len(envs) == 0:
            print_warn("No specific environment detected in config, skipping env selection")
        else:
            env = select(message="Which environment?", choices=envs).execute()
            command += ["-e", env]

    exit_code = pio_call(project, command)

    print()
    print_success("Done.")

    return exit_code

if __name__ == "__main__":
    main()
