from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import yaml

def load_user_config(config_path="config.yaml"):
    """Load user details from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def render_cover_letter(template_path, context):
    """Render a cover letter from a template and context dict."""
    env = Environment(loader=FileSystemLoader(Path(template_path).parent))
    template = env.get_template(Path(template_path).name)
    return template.render(**context)
