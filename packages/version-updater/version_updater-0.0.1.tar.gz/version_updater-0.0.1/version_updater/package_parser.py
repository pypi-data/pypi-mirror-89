import json
from version_updater.parser import AbstractParser


class PackageParser(AbstractParser):
    """
        A parser for package.json files
    """

    def __init__(self, filename):
        super().__init__(filename)
        with open(filename) as f:
            js = json.load(f)
            self.js = js

    def get_version(self):
        return self.js['version']

    def set_version(self, new_version):
        self.js['version'] = new_version

    def set_dep_version(self, depname, new_version):
        self.js['dependencies'][depname] = new_version

    def return_content(self):
        return self.js

    def finish(self):
        with open(self.filename, 'w') as outf:
            outf.write(json.dumps(self.js, indent=2))
