#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)


class Plugin:
    """
    Plugin class describes metadatata about an plugin supplied
    """
    def __init__(self):
        self.pid = None
        self.plugin_type = None
        self.factory = False
        self.name = None
        self.description = None
        self.class_name = None
        self.config_properties = None
        self.config_template = None
        self.actor_type = 0

    def is_factory(self) -> bool:
        """
        Checks if this plugin is a factory.
        @return true if the plugin represents a factory
        """
        return self.factory

    def set_factory(self, *, factory: bool):
        """
        Sets the factory flag. A plugin is a factory if it is used to create the
        actual plugin rather than it being the plugin itself.
        @param factory true|false
        """
        self.factory = factory

    def get_id(self) -> str:
        """
        Returns the plugin identifier.
        @return the id
        """
        return self.pid

    def set_id(self, *, pid: str):
        """
        @param pid the id to set
        """
        self.pid = id

    def get_plugin_type(self) -> int:
        """
        @return the pluginType
        """
        return self.plugin_type

    def set_plugin_type(self, *, plugin_type: int):
        """
        @param plugin_type the pluginType to set
        """
        self.plugin_type = plugin_type

    def get_class_name(self) -> str:
        """
        @return the className
        """
        return self.class_name

    def set_class_name(self, *, class_name: str):
        """
        @param class_name the className to set
        """
        self.class_name = class_name

    def get_config_properties(self) -> dict:
        """
        Get config properties
        @return config properties
        """
        return self.config_properties

    def set_config_properties(self, *, config_properties: dict):
        """
        Set config properties
        @param config_properties config properties
        """
        self.config_properties = config_properties

    def get_config_template(self) -> str:
        """
        Get Config template
        @param config template
        """
        return self.config_template

    def set_config_template(self, *, config_template: str):
        """
        Set config template
        @param config_template config template
        """
        self.config_template = config_template

    def get_name(self) -> str:
        """
        Get Name
        @return name
        """
        return self.name

    def set_name(self, *, name: str):
        """
        Set name
        @param name name
        """
        self.name = name

    def get_actor_type(self) -> int:
        """
        Get Actor Type
        @return actor type
        """
        return self.actor_type

    def set_actor_type(self, *, actor_type: int):
        """
        Set actor type
        @param actor_type actor type
        """
        self.actor_type = actor_type
