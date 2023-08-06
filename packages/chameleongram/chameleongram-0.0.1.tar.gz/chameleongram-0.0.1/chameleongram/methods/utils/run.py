import trio

from chameleongram.exceptions import Propagate, NowStop


class Run:
    async def run(self):
        """Run a client instance."""

        await self.start()

        while True:
            if self.handlers:
                update = await self.recv()

                for handler in self.handlers:
                    _update = update

                    if handler.filters is not None:
                        if not handler(_update, self):
                            continue
                    try:
                        await handler.callback(self, _update)
                        continue
                    except NowStop:
                        continue
                    except Propagate:
                        ...

            else:
                await trio.sleep(1)
