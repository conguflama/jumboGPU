from argparse import ArgumentParser
from pathlib import Path
import subprocess

import toml


def config_to_sbatch_flags(config_toml):
    config_dict = toml.load(config_toml)
    sbatch_flags = " ".join([f"{key} {val}" for key, val in config_dict["sbatch"].items()])
    return sbatch_flags


def config_to_launch_cmd(config_toml):
    config_dict = toml.load(config_toml)
    return config_dict["launch_cmd"]


def parse_args(is_search=False):
    parser = ArgumentParser()
    parser.add_argument("config_path")
    if is_search:
        parser.add_argument("search_path")
    parser.add_argument("-no_label", action="store_true",
                        help="Disable automatic '--label [search]_[search #]' launch flag")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sbatch_flags = config_to_sbatch_flags(args.config_path)
    launch_cmd = config_to_launch_cmd(args.config_path)
    if not args.no_label:
        launch_cmd += f" --label {Path(args.config_path).stem}"
    cmd = f"sbatch {sbatch_flags} --wrap \"{launch_cmd}\""
    subprocess.run(cmd, shell=True)
