import argparse
from version_updater import PackageParser, YamlParser, RegexParser, RequirementsParser

"""
Supports:
- package.json
- .gitlab-ci.yml
- setup.py
- requirements.txt
"""


def get_parser(fname):
    if fname[-4:] == 'json':
        return PackageParser(fname)
    elif fname[-4:] == '.yml' or fname[-4:] == 'yaml':
        return RegexParser(fname, 'yaml')
    elif fname[-8:] == 'setup.py':
        return RegexParser(fname, 'setup')
    elif len(fname) >= 16 and fname[-16:] == 'requirements.txt':
        return RequirementsParser(fname)
    else:
        return None


def core(filename, do_set, do_deps, bump):
    parser = get_parser(filename)
    if parser:
        if do_set:
            print(f'Setting {filename} to {do_set}')
            parser.set_version(do_set)
        elif bump:
            print(f'Bumping {filename} to {bump}')
            parser.bump(bump)

        if do_deps:
            dep_mappings = do_deps
            all_mappings = [{'dep': s[0], 'var': s[1]} for s in [
                s1.split('=') for s1 in dep_mappings.split(",")]]
            for kv in all_mappings:
                print(
                    f'Setting {filename} dependency {kv["dep"]} to {kv["var"]}')
                parser.set_dep_version(kv["dep"], kv["var"])
        parser.finish()
        print(f'Done!')
    else:
        print(f'Unable to handle file: {filename}')


def main():
    parser = argparse.ArgumentParser(
        description='Update semantic versions for artifacts')
    parser.add_argument('--set', help='Set the main artifact version')
    parser.add_argument('--set-dependencies', dest='set_deps',
                        help='Set a dependency artifact version')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'],
                        help='To bump the version instead of setting a specific value')
    parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                        help='The file to use for the version info')
    args = parser.parse_args()
    filename = args.file[0]
    core(filename, args.set, args.set_deps, args.bump)


if __name__ == "__main__":
    main()
