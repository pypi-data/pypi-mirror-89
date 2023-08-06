import pathlib
import platform
from importlib import import_module

from chameleongram import AuthKey
from chameleongram.connection import Connection
from chameleongram.raw import core, functions, layer
from chameleongram.exceptions import RpcException, InvalidTokenException
from chameleongram.utils import asyncrange


class Start:
    __call__ = lambda *_: ...

    async def start(self):
        """Start the client."""

        if self.blueprint:
            for path in (pathlib.Path(x).rglob("*.py") for x in self.blueprint if x):
                for file in path:
                    module_path = '.'.join(file.parent.parts + (file.stem,))
                    import_module(module_path)

        async for _ in asyncrange(self.MAX_RETRIES):
            if self.connection:
                await self.connection.close()
            self.auth_key, self.server_salt = await AuthKey(
                self.dc_id, self.test_mode
            ).generate()
            self.connection = Connection(
                self.dc_id, test_mode=self.test_mode, transport=self.transport
            )
            await self.connection.connect()
            try:
                await self(core.functions.Ping(ping_id=0))

                await self(
                    functions.InvokeWithLayer(
                        layer=layer,
                        query=functions.InitConnection(
                            api_id=self.api_id,
                            app_version=self.__version__,
                            device_model=f"{platform.python_implementation()} {platform.python_version()}",
                            lang_code="en",
                            lang_pack="",
                            query=functions.help.GetConfig(),
                            system_lang_code="en",
                            system_version=f"{platform.system()} {platform.release()}",
                        ),
                    )
                )

                if self.token:
                    await self(
                        functions.auth.ImportBotAuthorization(
                            api_id=self.api_id,
                            api_hash=self.api_hash,
                            bot_auth_token=self.token,
                        )
                    )

                self.show_message()

                return self
            except (RpcException, AssertionError) as error:
                if type(error) is AssertionError:
                    ...
                elif error.description == "USER_MIGRATE":
                    self.auth_key = None
                    self.auth_key_id = None
                    self.server_salt = None
                    self.session_id = self.rnd()
                    self.dc_id = error.x
                    continue
                elif error.description == "ACCESS_TOKEN_INVALID":
                    raise InvalidTokenException(
                        "The token you entered is invalid or it was revoked. Get a working one from @BotFather."
                    )
