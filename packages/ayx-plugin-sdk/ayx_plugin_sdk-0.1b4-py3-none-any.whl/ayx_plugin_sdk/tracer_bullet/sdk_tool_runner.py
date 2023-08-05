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
"""Runner for the SDK gRPC lifecycle."""
from typing import TYPE_CHECKING

from ayx_plugin_sdk.providers.amp_provider.grpc_util import (
    SocketAddress,
    build_sdk_engine_client,
    build_sdk_tool_server,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.grpc_repository import (
    GrpcRepository,
)
from ayx_plugin_sdk.providers.amp_provider.resources.generated.sdk_tool_service_startup_info_pb2 import (
    SdkToolServiceStartupInfo,
)

if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.amp_provider.resources.generated.transport_pb2 import (
        ReturnStatus,
    )


class HandshakeFailedException(RuntimeError):
    """Exception when the handshake fails."""

    pass


class SdkToolRunner:
    """Class for managing gRPC lifecycle for the SDK Plugin."""

    def __init__(self, sdk_engine_address: "SocketAddress"):
        """Construct an SDK Tool Runner."""
        self._sdk_engine_address = sdk_engine_address

    def start_service(self) -> None:
        """Start the SDK Tool service."""
        sdk_tool_server, sdk_tool_server_address = build_sdk_tool_server(
            SocketAddress("localhost", 0)
        )

        GrpcRepository().save_sdk_tool_server(sdk_tool_server)
        GrpcRepository().save_sdk_tool_server_address(sdk_tool_server_address)

        GrpcRepository().save_sdk_engine_client(
            build_sdk_engine_client(self._sdk_engine_address)
        )

        GrpcRepository().get_sdk_tool_server().start()

    @staticmethod
    def handshake_with_sdk_engine_service() -> "ReturnStatus":  # type: ignore
        """Run the handshake with the SDK Engine Server."""
        try:
            return_status = (
                GrpcRepository()
                .get_sdk_engine_client()
                .ConfirmSdkEngineServiceConnection(
                    SdkToolServiceStartupInfo(
                        success=True,
                        message=f"Startup of plugin successful!",
                        sdk_tool_server_address=GrpcRepository()
                        .get_sdk_tool_server_address()
                        .address,
                    ),
                )
            )
        except Exception:
            raise HandshakeFailedException("Couldn't connect to server.")

        return return_status  # type: ignore

    @staticmethod
    def wait_for_termination() -> None:
        """Block and wait for the process to terminate."""
        GrpcRepository().get_sdk_tool_server().wait_for_termination()
