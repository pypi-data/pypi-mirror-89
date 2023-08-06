from .ca_implementation import BLUvoCa


class BLUvoCaKia(BLUvoCa):

    def __init__(self, bluvo_config):
        super().__init__(bluvo_config)
        self.bluvo_config.base_url = 'https://myuvo.ca/tods/api/'
