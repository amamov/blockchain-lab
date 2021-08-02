from typing import Optional
import json


def get_secret(
    key: str, default_value: Optional[str] = None, json_path: str = "./secrets.json"
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")


if __name__ == "__main__":
    pass
