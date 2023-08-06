import json
from version_updater.parser import AbstractParser
import re

reg_format_setup = '({tok}\\s*==?\\s*)("|\\\')?([0-9]+[.][0-9]+[.][0-9]+)("|\\\')?'
reg_format_yaml = '(VERSION\\s*:)(\\s*)([0-9]+[.][0-9]+[.][0-9]+)(\\s*)'


class RegexParser(AbstractParser):
    """
        A parser for setup.py files
    """

    def __init__(self, filename, regtype):
        super().__init__(filename)
        self.regtype = regtype
        with open(filename) as f:
            self.contents = f.read()

    def get_version(self):
        reg_format = reg_format_setup if self.regtype == 'setup' else reg_format_yaml
        regc = re.compile(reg_format.format(tok='version'))
        mo = regc.search(self.contents)
        return mo.group(3)

    def set_version(self, new_version):
        self.__subs_core('version', new_version)

    def set_dep_version(self, depname, new_version):
        self.__subs_core(depname, new_version)

    def __subs_core(self, depname, new_version):
        reg_format = reg_format_setup if self.regtype == 'setup' else reg_format_yaml
        regc = re.compile(reg_format.format(tok=depname))
        mo = regc.search(self.contents)
        fstr = f'{mo.group(1)}{mo.group(2)}{new_version}{mo.group(4)}' if mo.group(
            2) and mo.group(4) else f'{mo.group(1)}{new_version}{mo.group(4)}'
        subst = regc.sub(
            fstr, self.contents)
        self.contents = subst

    def return_content(self):
        return self.contents

    def finish(self):
        with open(self.filename, 'w') as outf:
            outf.write(self.contents)
