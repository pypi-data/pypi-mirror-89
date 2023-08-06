import redgrease.client


def connect(arg):
    print(f"Sylt . SDK . Connect : {arg}")


class Sylt:
    """Sylt Client SDK
    """
    def __init__(
        self,
        server='localhost',
        port=6379,
        **server_kwargs
    ):
        self.server = redgrease.client.RedisGears(
            host=server,
            port=port,
            **server_kwargs
        )
