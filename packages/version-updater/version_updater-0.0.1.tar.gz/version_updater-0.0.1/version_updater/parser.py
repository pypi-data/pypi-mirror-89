import semver


class AbstractParser:

    def __init__(self, filename):
        self.filename = filename

    def get_version(self):
        return ''

    def set_version(self, new_version):
        pass

    def set_dep_version(self, depname, new_version):
        pass

    def return_content(self):
        return None

    def finish(self):
        pass

    def bump(self, which):
        ver = self.get_version()
        semantic_ver = semver.VersionInfo.parse(ver)
        newver = semantic_ver
        if which.lower() == 'major':
            newver = semantic_ver.bump_major()
        elif which.lower() == 'minor':
            newver = semantic_ver.bump_minor()
        elif which.lower() == 'patch':
            newver = semantic_ver.bump_patch()
        final_ver = f'{newver.major}.{newver.minor}.{newver.patch}'
        print(f'Setting final version to {final_ver}')
        self.set_version(final_ver)
