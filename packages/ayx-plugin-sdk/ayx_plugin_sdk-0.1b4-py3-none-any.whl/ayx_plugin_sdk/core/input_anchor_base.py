# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
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
"""Input anchor interface definition."""
from abc import ABC, abstractmethod
from typing import Any, List

from ayx_plugin_sdk.core.input_connection_base import InputConnectionBase


class InputAnchorBase(ABC):
    """Input anchor interface definition."""

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the input anchor.

        Returns
        -------
        str
            The name of the input anchor.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def allow_multiple(self) -> bool:
        """
        Get the status that indicates if multiple connections are allowed.

        Returns
        -------
        bool
            Boolean indicating if multiple connections are allowed.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def optional(self) -> bool:
        """
        Get the status that indicates if the input anchor is optional.

        Returns
        -------
        bool
            Boolean indicating if input anchor is optional.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def connections(self) -> List[InputConnectionBase]:
        """
        Get the anchor connections.

        Returns
        -------
        List[InputConnectionBase]
            List of all the connections associated with this anchor.
        """
        raise NotImplementedError()

    def __eq__(self, other: Any) -> bool:
        """Implement equivalence check for comparing two Input Anchor objects."""
        if isinstance(other, InputAnchorBase):
            return (
                self.name == other.name
                and self.allow_multiple == other.allow_multiple
                and self.optional == other.optional
                and self.connections == other.connections
            )
        else:
            return NotImplemented
