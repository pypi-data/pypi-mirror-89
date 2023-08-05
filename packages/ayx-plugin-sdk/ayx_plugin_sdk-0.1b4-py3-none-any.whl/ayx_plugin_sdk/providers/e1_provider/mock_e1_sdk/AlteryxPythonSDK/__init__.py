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
"""Mocks for testing."""
from .alteryx_engine import AlteryxEngine
from .constants import EngineMessageType, FieldType, Status
from .field import Field
from .output_anchor import OutputAnchor
from .output_anchor_manager import OutputAnchorManager
from .record_copier import RecordCopier
from .record_creator import RecordCreator
from .record_info import RecordInfo
from .record_ref import RecordRef

__all__ = [
    "AlteryxEngine",
    "EngineMessageType",
    "FieldType",
    "Status",
    "Field",
    "RecordInfo",
    "RecordCopier",
    "RecordCreator",
    "RecordRef",
    "OutputAnchor",
    "OutputAnchorManager",
]
