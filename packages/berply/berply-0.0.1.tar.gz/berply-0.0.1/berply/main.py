import argparse
import yaml

from jinja2 import Environment, StrictUndefined, Template
from pathlib import Path

env = Environment(
    extensions=[],
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--env", "-e", default="local", help="Set the current environment or this run"
)
parser.add_argument(
    "--var", nargs="*", help="Override a variable in the form of key.path=value"
)
parser.add_argument(
    "--label-selector",
    "-l",
    nargs="*",
    help="Filter kubernetes resources based on the label selector",
)


def _load_env_config(env):
    return yaml.safe_load(Path(f"env/{env}.yaml").read_text())


def _deepmerge(into, other):
    for k, v in other.items():
        if v is None:
            into.pop(k)
        elif isinstance(v, dict) and isinstance(into[k], dict):
            _deepmerge(into[k], v)
        else:
            into[k] = v


def load_resources(vars, label_selector=None):
    resources = {}

    for file_name in Path("res").glob("**/*.yaml"):
        tmpl = Template(file_name.read_text())
        datas = yaml.safe_load_all(tmpl.render(vars=vars))

        for idx, data in enumerate(datas):
            if not data:
                continue

            name = f"{file_name.name}:{idx}"
            if "name" in data.get("metadata", {}):
                name = f"{name} ({data['metadata']['name']})"

            if label_selector:
                matched = False
                for k, v in label_selector.items():
                    if data.get("metadata", {}).get("labels", {}).get(k) != v:
                        break
                else:
                    matched = True

                if not matched:
                    continue

            resources[name] = data

    return resources


def main():
    args = parser.parse_args()

    env_config = _load_env_config(args.env)

    if args.var:
        for var in args.var:
            k, v = var.split("=", 1)
            key_parts = k.split(".")

            for part in reversed(key_parts):
                v = {part: v}
            _deepmerge(env_config, v)

    label_selector = None
    if args.label_selector:
        label_selector = dict(kv.split("=", 1) for kv in args.label_selector)

    resources = load_resources(env_config, label_selector)
    for name, resource in resources.items():
        print(f"# resource: {name}")
        print(yaml.safe_dump(resource))
        print("---")


if __name__ == "__main__":
    main()
