import yaml
from typing import Tuple


class ConfigHelper:

    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = {
                'latitude': 120,
                'longitude': 40,
                'height': 0,
                'api': '',
                'apikey': '',
                'num_points': 1
            }
            self.config.update(yaml.load(f))
            self.start = None

    @property
    def reference_llh(self) -> Tuple[float, float, float]:
        return self.config['latitude'], \
               self.config['longitude'], \
               self.config['height']

    @property
    def api(self) -> Tuple[str, str]:
        return self.config['api'], self.config['apikey']

    @property
    def num_points(self) -> int:
        return self.config['num_points']
