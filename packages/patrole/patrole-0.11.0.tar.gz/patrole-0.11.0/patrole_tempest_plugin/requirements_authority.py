# Copyright 2017 AT&T Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import copy
import yaml

from oslo_log import log as logging

from tempest import config
from tempest.lib import exceptions as lib_exc

from patrole_tempest_plugin.rbac_authority import RbacAuthority
from patrole_tempest_plugin import rbac_exceptions

CONF = config.CONF
LOG = logging.getLogger(__name__)


class RequirementsParser(object):
    """A class that parses a custom requirements file."""
    _inner = None

    class Inner(object):
        _rbac_map = None

        def __init__(self, filepath):
            with open(filepath) as f:
                RequirementsParser.Inner._rbac_map = \
                    list(yaml.safe_load_all(f))

    def __init__(self, filepath):
        if RequirementsParser._inner is None:
            RequirementsParser._inner = RequirementsParser.Inner(filepath)

    @staticmethod
    def parse(component):
        """Parses a requirements file with the following format:

        .. code-block:: yaml

            <service_foo>:
              <api_action_a>:
                - <allowed_role_1>
                - <allowed_role_2>,<allowed_role_3>
                - <allowed_role_3>
              <api_action_b>:
                - <allowed_role_2>
                - <allowed_role_4>
            <service_bar>:
              <api_action_c>:
                - <allowed_role_3>

        :param str component: Name of the OpenStack service to be validated.
        :returns: The dictionary that maps each policy action to the list
            of allowed roles, for the given ``component``.
        :rtype: dict
        """
        try:
            for section in RequirementsParser.Inner._rbac_map:
                if component in section:
                    rules = copy.copy(section[component])

                    for rule in rules:
                        rules[rule] = [
                            roles.split(',') for roles in rules[rule]]

                        for i, role_pack in enumerate(rules[rule]):
                            rules[rule][i] = [r.strip() for r in role_pack]

                    return rules
        except yaml.parser.ParserError:
            LOG.error("Error while parsing the requirements YAML file. Did "
                      "you pass a valid component name from the test case?")
        return {}


class RequirementsAuthority(RbacAuthority):
    """A class that uses a custom requirements file to validate RBAC."""

    def __init__(self, filepath=None, component=None):
        """This class can be used to achieve a requirements-driven approach to
        validating an OpenStack cloud's RBAC implementation. Using this
        approach, Patrole computes expected test results by performing lookups
        against a custom requirements file which precisely defines the cloud's
        RBAC requirements.

        :param str filepath: Path where the custom requirements file lives.
            Defaults to ``[patrole].custom_requirements_file``.
        :param str component: Name of the OpenStack service to be validated.
        """
        self.filepath = filepath or CONF.patrole.custom_requirements_file
        if component is not None:
            self.roles_dict = RequirementsParser(self.filepath).parse(
                component)
        else:
            self.roles_dict = None

    def allowed(self, rule_name, roles):
        """Checks if a given rule in a policy is allowed with given role.

        :param string rule_name: Rule to be checked using provided requirements
            file specified by ``[patrole].custom_requirements_file``. Must be
            a key present in this file, under the appropriate component.
        :param List[string] roles: Roles to validate against custom
            requirements file.
        :returns: True if ``role`` is allowed to perform ``rule_name``, else
            False.
        :rtype: bool
        :raises RbacParsingException: If ``rule_name`` does not exist among the
            keyed policy names in the custom requirements file.
        """
        if not self.roles_dict:
            raise lib_exc.InvalidConfiguration(
                "Roles dictionary parsed from requirements YAML file is "
                "empty. Ensure the requirements YAML file is correctly "
                "formatted.")
        try:
            requirement_roles = self.roles_dict[rule_name]
        except KeyError:
            raise rbac_exceptions.RbacParsingException(
                "'%s' rule name is not defined in the requirements YAML file: "
                "%s" % (rule_name, self.filepath))

        for role_reqs in requirement_roles:
            required_roles = [
                role for role in role_reqs if not role.startswith("!")]
            forbidden_roles = [
                role[1:] for role in role_reqs if role.startswith("!")]

            # User must have all required roles
            required_passed = all([r in roles for r in required_roles])
            # User must not have any forbidden roles
            forbidden_passed = all([r not in forbidden_roles
                                    for r in roles])

            if required_passed and forbidden_passed:
                return True

        return False
