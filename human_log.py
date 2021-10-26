# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Current maintainer: Marcos Diez [ marcos AT unitron DOT com DOT br ]

# Inspired from: https://github.com/redhat-openstack/khaleesi/blob/master/plugins/callbacks/human_log.py
# Further improved support Ansible 2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    import simplejson as json
except ImportError:
    import json

from ansible.plugins import AnsiblePlugin
    
# Fields to reformat output for
FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout',
          'stderr', 'results']


class CallbackModule(AnsiblePlugin):

    """
    Ansible callback plugin for human-readable result logging
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'human_log'
    CALLBACK_NEEDS_WHITELIST = False

    def _jsoner(self, elem, gap=1, output=None):
        if output is None:
            output = dict()
        if gap > 10:
            output["zzzz_gap"] = gap
            return output

        if elem is None:
            return elem

        # for basic_element in [basestring, int, float, long]:
        if isinstance(elem, (basestring, int, float, long)):
            return elem

        for key, value in elem.iteritems():
            if isinstance(value, bool) or value is None:
                output[key] = value
            elif isinstance(value, dict):
                output[key] = self._jsoner(value, gap+1)
                # self._line_printer(gap, key, "DICT")
                # self._jsoner(value, gap+1)
            elif isinstance(value, list):
                output[key] = new_output = list()
                for list_item in value:
                    new_output.append(self._jsoner(list_item, gap+1))
            else:
                value_str = "{}".format(value)
                if "\n" in value_str:
                    value_str = value_str.replace("\r","").split("\n")

                output[key] = value_str #"{}".format(value) # .replace("\\r","").replace("\\n","\n")
                # self._line_printer(gap, key, value)
        return output

    def _dump_helper(self, msg, terminal_color, result):
        normal_terminal_color = "\033[0m"
        print(msg.format(terminal_color, getattr(result, "_host")))
        print(json.dumps(self._jsoner(result.__dict__), sort_keys=True, indent=3))
        # print(json.dumps(self._jsoner(result._task.__dict__), sort_keys=True, indent=3))
        print(normal_terminal_color)

    # since methods get added all the time, it makes no sense to have a bunch of empty ones
    # instead, we just uncomment the two methods below
    # and see what is the method that is being called


    # def set_play_context(self, play_context):
    #     # this function needs to exist or else __getattr__ breaks...
    #     pass
    #
    # def __getattr__(self, name):
    #     print("This is the function being called: [{}]".format(name))



    def v2_runner_on_failed(self, result, ignore_errors=False):
        red_terminal_color  = "\033[31m"
        return self._dump_helper("{}fatal: [{}]: FAILED! =>\n", red_terminal_color, result)

    def v2_runner_item_on_failed(self, result):
        return self.v2_runner_on_failed(result)

    # def v2_runner_on_ok(self, result):
    #     if result.__dict__.get("_result", {}).get("changed", False):
    #         return self.v2_runner_on_changed(result)
    #
    #     green_terminal_color = "\033[32m"
    #     return self._dump_helper("{}OK: [{}]: OK! =>\n", green_terminal_color, result)
    #
    # def v2_runner_on_changed(self, result):
    #     yellow_terminal_color = "\033[33m"
    #     return self._dump_helper("{}changed: [{}]: changed! =>\n", yellow_terminal_color, result)

