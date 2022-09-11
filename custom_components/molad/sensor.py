import logging
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.helpers.entity import Entity, async_generate_entity_id
from molad import Molad

_LOGGER = logging.getLogger(__name__)

version = "0.2.1"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):

    if None in (config['latitude'], config['longitude'], config['timezone']):
        _LOGGER.error("Latitude or Longitude or TimeZone are not set in Home Assistant config")
        return

    entities = [
        MoladSensor(hass, config),
        # IsShabbosMevorchimSensor(hass, config),
    ]

    async_add_entities(entities, False)


class MoladSensor(Entity):

    _state = None
    _attributes = {}
    config = {}
    molad = None

    def __init__(self, hass, config):
        """Initialize the sensor"""
        self.type = sensor_type
        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT,
            'molad',
            hass=hass,
        )
        self._state = None
        self._attributes = {}
        self.config = config
        self.molad = Molad(config)

        self.update_sensor()

    def update_sensor(self):

        d = datetime.date.today()

        m = self.molad.get_molad(d)
        rc = self.molad.get_rosh_chodesh_days(d)
        sm = self.molad.is_shabbos_mevorchim(d)
        a = self.molad.get_attributes(m, sm, rc)

        self._state = m['text']
        self._attributes = a

        _LOGGER.info('Molad Updated')

    async def async_update(self):
        self.update_sensor()

    @property
    def name(self) -> str:
        return "Molad"

    @property
    def icon(self):
        """Icon to use in the frontend"""
        return 'mdi:moon-waxing-crescent'

    @property
    def should_poll(self) -> bool:
        """Return true if the device should be polled for state updates"""
        return True

    @property
    def state(self):
        """Return the state of the sensor"""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.attributes