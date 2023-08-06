import importlib
import logging
import re

from streamscrobbler import streamscrobbler


log = logging.getLogger(__name__)


class MetadataState:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.play_now = ""
        self.homepage = ""


class LoadMetadata:

    def metadata(self, station):
        pass

    def get(self):
        return self.metadata


class LoadMetadataFromPlugin(LoadMetadata):
    def _normalize_plugin_name(self, name):
        name = re.sub(r"(\s|\-|\.|,|\"|\'|\`)+", "_", name)
        return name.lower()

    def _plugin_name(self, station):
        return "plug_{}".format(self._normalize_plugin_name(station.name))

    def metadata(self, station):

        try:
            plugin = importlib.import_module(
                "coderadio.plugins." + self._plugin_name(station)
            )
        except ImportError:
            log.exception("Plugin not Found")
            return None, None
        else:
            service, artist, title = plugin.run()
            log.info(f"{service} {artist} {title}")
            if not all([service, artist, title]):
                return
            song = "{} - {}".format(artist, title)
        return song, service


class LoadMetadataFromStream(LoadMetadata):
    def metadata(self, station):
        data = streamscrobbler.get_server_info(station.url)
        metadata = data["metadata"]
        if not metadata:
            return
        return metadata.get("song")


class Metadata:
    def __init__(self):
        self.station = None
        self.context = MetadataState()
        self.metadata_from_plugin = LoadMetadataFromPlugin()
        self.metadata_from_stream = LoadMetadataFromStream()

    def get(self):
        """
        Try to get metadata from the plugin or streamscrobbler.
        """
        try:
            song, service = self.metadata_from_plugin.get(self.station)
        except Exception:
            log.exception("plugin error: ")
        else:
            if song and service:
                self.context.play_now = song
            else:
                song = self.metadata_from_stream.get(self.station)
                self.context.play_now = song

    def state(self):
        return self.context

    def __call__(self, station):
        self.station = station
        self.context.id = self.station.id
        self.context.homepage = self.station.homepage
        self.context.name = self.station.name
