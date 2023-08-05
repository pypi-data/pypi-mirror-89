# Copyright 2020 Peter Bencze
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import syncer
from pyppeteer.element_handle import ElementHandle


class Element:
    """Represents a web element."""

    def __init__(self, element_handle: ElementHandle) -> None:
        """
        Creates a new element instance.

        :param element_handle: the element handle instance
        """

        self._element_handle = element_handle

    def get_attribute(self, name: str) -> str:
        """
        Returns the specific attribute of this element.

        :param name: the attribute name
        :return: the attribute value
        """

        function = f'element => element.getAttribute({json.dumps(name)})'
        return syncer.sync(self._element_handle.executionContext.evaluate(function, self._element_handle))

    def get_text(self) -> str:
        """
        Returns the text content of this element.

        :return: the text content of this element
        """

        return syncer.sync(self._element_handle.executionContext.evaluate('element => element.textContent',
                                                                          self._element_handle))
