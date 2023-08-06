from version_updater.parser import AbstractParser


class RequirementsParser(AbstractParser):
    """
        A parser for requirements.txt files
    """

    def __init__(self, filename):
        super().__init__(filename)
        with open(filename) as f:
            self.contents = f.readlines()

    def set_dep_version(self, depname, new_version):
        ans = []
        for oneline in self.contents:
            splits = oneline.split('==')
            res = oneline
            if splits[0] == depname:
                res = f'{depname}=={new_version}\n'
            ans.append(res)
        self.contents = ans

    def bump(self, which):
        pass

    def return_content(self):
        return self.contents

    def finish(self):
        with open(self.filename, 'w') as outf:
            outf.write(''.join(self.contents))
