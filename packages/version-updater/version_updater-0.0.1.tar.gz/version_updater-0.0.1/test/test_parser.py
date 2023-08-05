import unittest
import shutil
from main import core

managed_file_fmts = ['test/test-data/{which}/requirements.txt',
                     'test/test-data/{which}/.gitlab-ci.yml',
                     'test/test-data/{which}/package1.json']


class TestParser(unittest.TestCase):

    def tearDown(self):
        for f in managed_file_fmts:
            shutil.copyfile(f.format(which='backup'), f.format(which='input'))

    # update-version --set-dependencies gtfs-realtime-bindings=4.5.6,jupyter=2.3.4 foo-requirements.txt --bump major
    def test_requirements_2_deps(self):
        deps = 'gtfs-realtime-bindings=4.5.6,jupyter=2.3.4'
        self.__test_core('requirements.txt', None, deps, 'major')

    # update-version --set-dependencies react=1.2.3,react-dom=2.3.4 package1.json --bump major
    def test_package_2_deps_bump_major(self):
        deps = 'react=1.2.3,react-dom=2.3.4'
        self.__test_core('package1.json', None, deps, 'major')

    # update-version --bump patch .gitlab-ci.yml
    def test_gl_yaml_bump_patch(self):
        self.__test_core('.gitlab-ci.yml', None, None, 'patch')

    # update-version --set-dependencies semver=4.5.6 setup.py --bump minor
    def test_setup_1_dep_bump_minor(self):
        self.__test_core('setup.py', None, 'semver=4.5.6', 'minor')

    def __test_core(self, which_file, do_set, deps, do_bump):
        input = f'test/test-data/input/{which_file}'
        expect = f'test/test-data/output/{which_file}'
        core(input, do_set, deps, do_bump)
        with open(input) as infile:
            test_contents = infile.read()
            with open(expect) as expect_file:
                expect_contents = expect_file.read()
                self.assertEqual(test_contents, expect_contents,
                                 f'Expected contents to be equal but were not.  Check {input} and compare to {expect}')


if __name__ == '__main__':
    unittest.main()
