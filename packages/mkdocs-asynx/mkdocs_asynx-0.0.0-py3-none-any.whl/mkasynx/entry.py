from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

class Entry(BasePlugin):
    config_scheme = (
        ('parameter', config_options.Type(bool, default=False)),
    )

    def on_config(self, config, **kwargs):
        print("Hi!")
