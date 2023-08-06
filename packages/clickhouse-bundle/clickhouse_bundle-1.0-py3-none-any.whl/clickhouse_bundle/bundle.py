from applauncher.kernel import ConfigurationReadyEvent
import logging
from clickhouse_driver import Client


class ClickhouseBundle(object):
    def __init__(self):
        self.logger = logging.getLogger("clickhouse")
        self.config_mapping = {
            "clickhouse": {
                "connection_uri": None,
            }
        }

        self.injection_bindings = {}
        self.event_listeners = [
            (ConfigurationReadyEvent, self.configuration_ready)
        ]

    def configuration_ready(self, event):
        config = event.configuration.clickhouse
        self.injection_bindings[Client] = Client.from_url(config.connection_uri)
