from NuRadioReco.modules.base.module import register_run
from NuRadioReco.utilities import units
import logging


class channelAddCableDelay:
    """
    Adds the cable delay to channels
    """

    def __init__(self):
        self.logger = logging.getLogger("NuRadioReco.channelApplyCableDelay")

    @register_run()
    def run(self, evt, station, det):
        """
        Adds cable delays to channels
        """
        for channel in station.iter_channels():
            cable_delay = det.get_cable_delay(station.get_id(), channel.get_id())
            self.logger.debug("cable delay of channel {} is {}ns".format(channel.get_id(), cable_delay / units.ns))
            channel.add_trace_start_time(cable_delay)
