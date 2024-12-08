import logging
import datetime
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.helpers.entity import Entity, async_generate_entity_id
from molad.helper import MoladHelper

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, async_add_entities, discovery_info=None):
    if None in (hass.config.latitude, hass.config.longitude, hass.config.time_zone):
        _LOGGER.error(
            "Latitude or Longitude or TimeZone are not set in Home Assistant config"
        )
        return

    entities = [
        MoladSensor(hass),
        IsShabbosMevorchimSensor(hass),
        IsUpcomingShabbosMevorchimSensor(hass),
    ]

    async_add_entities(entities, False)


class BaseSensor(Entity):
    _state = None
    _attributes = {}
    config = {}
    molad = None

    def __init__(self, id, hass):
        """Initialize the sensor"""
        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT,
            id,
            hass=hass,
        )
        self._state = None
        self._attributes = {}
        self.config = hass.config
        self.molad = MoladHelper(self.config)

        self.update_sensor()

    async def async_update(self):
        self.update_sensor()

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
        return self._attributes


class MoladSensor(BaseSensor):
    def __init__(self, hass):
        BaseSensor.__init__(self, "molad", hass)

    def update_sensor(self):
        d = datetime.date.today()
        m = self.molad.get_molad(d)

        self._state = m.molad.friendly
        self._attributes = self.get_attributes_for_molad(m)

        _LOGGER.info("Molad Updated")

    def get_attributes_for_molad(self, m):
        return {
            "icon": "mdi:moon-waxing-crescent",
            "friendly_name": "Molad",
            "day": m.molad.day,
            "hours": m.molad.hours,
            "minutes": m.molad.minutes,
            "am_or_pm": m.molad.am_or_pm,
            "chalakim": m.molad.chalakim,
            "friendly": m.molad.friendly,
            "rosh_chodesh": m.rosh_chodesh.text,
            "rosh_chodesh_days": m.rosh_chodesh.days,
            "rosh_chodesh_dates": m.rosh_chodesh.gdays,
            "is_shabbos_mevorchim": m.is_shabbos_mevorchim,
            "is_upcoming_shabbos_mevorchim": m.is_upcoming_shabbos_mevorchim,
            "month_name": m.rosh_chodesh.month,
        }

    @property
    def name(self) -> str:
        return "Molad"

    @property
    def icon(self):
        """Icon to use in the frontend"""
        return "mdi:moon-waxing-crescent"


class IsShabbosMevorchimSensor(BaseSensor):
    def __init__(self, hass):
        BaseSensor.__init__(self, "is_shabbos_mevorchim", hass)

    def update_sensor(self):
        d = datetime.date.today()

        sm = self.molad.is_shabbos_mevorchim(d)

        self._state = sm

        _LOGGER.info("Is Shabbos Mevorchim Updated")

    @property
    def name(self) -> str:
        return "Is Shabbos Mevorchim"

    @property
    def icon(self):
        """Icon to use in the frontend"""
        return "mdi:moon-waxing-crescent"


class IsUpcomingShabbosMevorchimSensor(BaseSensor):
    def __init__(self, hass):
        BaseSensor.__init__(self, "is_upcoming_shabbos_mevorchim", hass)

    def update_sensor(self):
        d = datetime.date.today()

        sm = self.molad.is_upcoming_shabbos_mevorchim(d)

        self._state = sm

        _LOGGER.info("Is Upcoming Shabbos Mevorchim Updated")

    @property
    def name(self) -> str:
        return "Is Upcoming Shabbos Mevorchim"

    @property
    def icon(self):
        """Icon to use in the frontend"""
        return "mdi:moon-waxing-crescent"
