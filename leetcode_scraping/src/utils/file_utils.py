import os
from pathlib import Path


def create_dirs(parent_dir, companies_names, stage_names):
    for comp_name in companies_names:
        for stage_name in stage_names:
            Path(os.path.join(parent_dir, comp_name, stage_name)) \
                .mkdir(parents=True, exist_ok=True)
