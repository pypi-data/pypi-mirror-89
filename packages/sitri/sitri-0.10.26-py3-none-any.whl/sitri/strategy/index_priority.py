import typing

from sitri.providers.base import ConfigProvider
from sitri.strategy.base import BaseStrategy


class IndexPriorityStrategy(BaseStrategy):
    """Get value from providers with priority by index in tuple."""

    provider_code = "index_priority"

    def __init__(self, *data_providers: ConfigProvider) -> None:
        """
        :param data_providers: config providers
        """

        self.providers = data_providers

    def get(self, *args, **kwargs) -> typing.Optional[typing.Any]:
        """Get value by index priority strategy.

        :param args: any args for providers
        :param kwargs: any kwargs for providers
        """
        for provider in self.providers:
            result = provider.get(*args, **kwargs)

            if result is not None:
                return result

        return None
