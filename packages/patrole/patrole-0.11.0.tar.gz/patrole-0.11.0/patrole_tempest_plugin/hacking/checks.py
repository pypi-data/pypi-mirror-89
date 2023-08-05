# Copyright 2013 IBM Corp.
# Copyright 2017 AT&T Corporation.
# All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import os
import re

from hacking import core
import pycodestyle


PYTHON_CLIENTS = ['cinder', 'glance', 'keystone', 'nova', 'swift', 'neutron',
                  'ironic', 'heat', 'sahara']

PYTHON_CLIENT_RE = re.compile('import (%s)client' % '|'.join(PYTHON_CLIENTS))
TEST_DEFINITION = re.compile(r'^\s*def test.*')
SETUP_TEARDOWN_CLASS_DEFINITION = re.compile(r'^\s+def (setUp|tearDown)Class')
SCENARIO_DECORATOR = re.compile(r'\s*@.*services\((.*)\)')
RAND_NAME_HYPHEN_RE = re.compile(r".*rand_name\(.+[\-\_][\"\']\)")
MUTABLE_DEFAULT_ARGS = re.compile(r"^\s*def .+\((.+=\{\}|.+=\[\])")
TESTTOOLS_SKIP_DECORATOR = re.compile(r'\s*@testtools\.skip\((.*)\)')
CLASS = re.compile(r"^class .+")
RBAC_CLASS_NAME_RE = re.compile(r'class .+RbacTest')
RULE_VALIDATION_DECORATOR = re.compile(
    r'\s*@rbac_rule_validation.action\(.*')
IDEMPOTENT_ID_DECORATOR = re.compile(r'\s*@decorators\.idempotent_id\((.*)\)')
EXT_RBAC_TEST = re.compile(
    r"class .+\(.+ExtRbacTest\)|class .+ExtRbacTest\(.+\)")

have_rbac_decorator = False


@core.flake8ext
def import_no_clients_in_api_tests(physical_line, filename):
    """Check for client imports from patrole_tempest_plugin/tests/api

    T102: Cannot import OpenStack python clients
    """
    if "patrole_tempest_plugin/tests/api" in filename:
        res = PYTHON_CLIENT_RE.match(physical_line)
        if res:
            return (physical_line.find(res.group(1)),
                    ("T102: python clients import not allowed "
                     "in patrole_tempest_plugin/tests/api/* or "
                     "patrole_tempest_plugin/tests/scenario/* tests"))


@core.flake8ext
def no_setup_teardown_class_for_tests(physical_line, filename):
    """Check that tests do not use setUpClass/tearDownClass

    T105: Tests cannot use setUpClass/tearDownClass
    """
    if pycodestyle.noqa(physical_line):
        return

    if SETUP_TEARDOWN_CLASS_DEFINITION.match(physical_line):
        return (physical_line.find('def'),
                "T105: (setUp|tearDown)Class can not be used in tests")


@core.flake8ext
def service_tags_not_in_module_path(physical_line, filename):
    """Check that a service tag isn't in the module path

    A service tag should only be added if the service name isn't already in
    the module path.

    T107
    """
    matches = SCENARIO_DECORATOR.match(physical_line)
    if matches:
        services = matches.group(1).split(',')
        for service in services:
            service_name = service.strip().strip("'")
            modulepath = os.path.split(filename)[0]
            if service_name in modulepath:
                return (physical_line.find(service_name),
                        "T107: service tag should not be in path")


@core.flake8ext
def no_hyphen_at_end_of_rand_name(logical_line, filename):
    """Check no hyphen at the end of rand_name() argument

    T108
    """
    msg = "T108: hyphen should not be specified at the end of rand_name()"
    if RAND_NAME_HYPHEN_RE.match(logical_line):
        return 0, msg


@core.flake8ext
def no_mutable_default_args(logical_line):
    """Check that mutable object isn't used as default argument

    N322: Method's default argument shouldn't be mutable
    """
    msg = "N322: Method's default argument shouldn't be mutable!"
    if MUTABLE_DEFAULT_ARGS.match(logical_line):
        yield (0, msg)


@core.flake8ext
def no_testtools_skip_decorator(logical_line):
    """Check that methods do not have the testtools.skip decorator

    T109
    """
    if TESTTOOLS_SKIP_DECORATOR.match(logical_line):
        yield (0, "T109: Cannot use testtools.skip decorator; instead use "
               "decorators.skip_because from tempest.lib")


@core.flake8ext
def use_rand_uuid_instead_of_uuid4(logical_line, filename):
    """Check that tests use data_utils.rand_uuid() instead of uuid.uuid4()

    T113
    """
    if 'uuid.uuid4()' not in logical_line:
        return

    msg = ("T113: Tests should use data_utils.rand_uuid()/rand_uuid_hex() "
           "instead of uuid.uuid4()/uuid.uuid4().hex")
    yield (0, msg)


@core.flake8ext
def no_rbac_rule_validation_decorator(physical_line, filename):
    """Check that each test has the ``rbac_rule_validation.action`` decorator.

    Checks whether the test function has "@rbac_rule_validation.action"
    above it; otherwise checks that it has "@decorators.idempotent_id" above
    it and "@rbac_rule_validation.action" above that.

    Assumes that ``rbac_rule_validation.action`` decorator is either the first
    or second decorator above the test function; otherwise this check fails.

    P100
    """
    global have_rbac_decorator

    if ("patrole_tempest_plugin/tests/api" in filename or
            "patrole_tempest_plugin/tests/scenario" in filename):

        if RULE_VALIDATION_DECORATOR.match(physical_line):
            have_rbac_decorator = True
            return

        if TEST_DEFINITION.match(physical_line):
            if not have_rbac_decorator:
                return (0, "Must use rbac_rule_validation.action "
                           "decorator for API and scenario tests")

            have_rbac_decorator = False


@core.flake8ext
def no_rbac_suffix_in_test_filename(filename):
    """Check that RBAC filenames end with "_rbac" suffix.

    P101
    """
    if "patrole_tempest_plugin/tests/api" in filename:

        if filename.endswith('rbac_base.py'):
            return

        if not filename.endswith('_rbac.py'):
            return 0, "RBAC test filenames must end in _rbac suffix"


@core.flake8ext
def no_rbac_test_suffix_in_test_class_name(physical_line, filename):
    """Check that RBAC class names end with "RbacTest"

    P102
    """
    if "patrole_tempest_plugin/tests/api" in filename:

        if filename.endswith('rbac_base.py'):
            return

        if CLASS.match(physical_line):
            if not RBAC_CLASS_NAME_RE.match(physical_line):
                return 0, "RBAC test class names must end in 'RbacTest'"


@core.flake8ext
def no_client_alias_in_test_cases(logical_line, filename):
    """Check that test cases don't use "self.client" to define a client.

    P103
    """
    if "patrole_tempest_plugin/tests/api" in filename:
        if "self.client" in logical_line or "cls.client" in logical_line:
            return 0, "Do not use 'self.client' as a service client alias"


@core.flake8ext
def no_extension_rbac_test_suffix_in_plugin_test_class_name(physical_line,
                                                            filename):
    """Check that Extension RBAC class names end with "ExtRbacTest"

    P104
    """
    suffix = "ExtRbacTest"
    if "patrole_tempest_plugin/tests/api" in filename:
        if EXT_RBAC_TEST.match(physical_line):
            subclass, superclass = physical_line.split('(')
            subclass = subclass.split('class')[1].strip()
            superclass = superclass.split(')')[0].strip()
            if "." in superclass:
                superclass = superclass.split(".")[1]

            both_have = all(
                clazz.endswith(suffix) for clazz in [subclass, superclass])
            none_have = not any(
                clazz.endswith(suffix) for clazz in [subclass, superclass])

            if not (both_have or none_have):
                if (subclass.startswith("Base") and
                        superclass.startswith("Base")):
                    return

                # Case 1: Subclass of "BaseExtRbacTest" must end in `suffix`
                # Case 2: Subclass that ends in `suffix` must inherit from base
                # class ending in `suffix`.
                if not subclass.endswith(suffix):
                    error = ("Plugin RBAC test subclasses must end in "
                             "'ExtRbacTest'")
                    return len(subclass) - 1, error
                elif not superclass.endswith(suffix):
                    error = ("Plugin RBAC test subclasses must inherit from a "
                             "'ExtRbacTest' base class")
                    return len(superclass) - 1, error
