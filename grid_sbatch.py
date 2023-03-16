import itertools
from pathlib import Path
import subprocess

import toml

from sbatch import config_to_sbatch_flags, config_to_launch_cmd, parse_args


def search_to_flags(search_toml):
    search_dict = toml.load(search_toml)
    flag_strs = []
    print(search_dict)
    for vals in itertools.product(*search_dict.values()):
        flag_strs.append(" ".join([f"{key} {val}" for key, val in zip(search_dict.keys(), vals)]))
    return flag_strs


if __name__ == "__main__":
    args = parse_args(is_search=True)
    sbatch_flags = config_to_sbatch_flags(args.config_path)
    launch_cmd = config_to_launch_cmd(args.config_path)
    flag_strs = search_to_flags(args.search_path)
    for i, flag_str in enumerate(flag_strs):
        if not args.no_label:
            flag_str += f" --label {Path(args.search_path).stem}_{i}"
        cmd = f"sbatch {sbatch_flags} --wrap \"{launch_cmd} {flag_str}\""
        subprocess.run(cmd, shell=True)
