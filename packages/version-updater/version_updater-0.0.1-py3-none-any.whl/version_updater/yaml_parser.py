import json
from ruamel.yaml import YAML
from version_updater.parser import AbstractParser

yaml = YAML()
yaml.indent(offset=2)


class YamlParser(AbstractParser):
    """
        A parser for gitlab-ci.yaml files
    """

    def __init__(self, filename):
        super().__init__(filename)
        with open(filename) as f:
            js = yaml.load(f)
            self.js = js

    def get_version(self):
        vars = self.js['variables']
        self.vvar = 'VERSION'
        for k in vars.keys():
            if k.lower() == 'version':
                self.vvar = k
        return vars[self.vvar]

    def set_version(self, new_version):
        self.get_version()
        self.js['variables'][self.vvar] = new_version

    def return_content(self):
        return self.js

    def finish(self):
        with open(self.filename, 'w') as outf:
            yaml.dump(self.js, outf)
