import os
import configparser


# Get path for config.
folder_path = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(folder_path, "config.conf")
CONFIG_SECTION = "Config"


class Singleton(type):
    """ Use to create a singleton object.
    """

    def __init__(cls, name, bases, dict):
        super().__init__( name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class Config(metaclass=Singleton):
    """ Configuration.
    """

    message = "Failed to read configuration file. {0}"

    def __init__(self):

        # Needed for auto-complete
        self.tcp_buffer_size = None
        self.udp_buffer_size = None
        self.accumulator_packet_size = None

        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)
        self._parse_config_file()

    def _parse_config_file(self):
        """ Parse configuration file.
        """

        str_fields = []
        int_fields = ["tcp_buffer_size", "udp_buffer_size", "accumulator_packet_size"]
        space_separated_list_fields = []

        try:
            self.config.read(CONFIG_PATH)

            for str_field in str_fields:
                value = self.config.get(section=CONFIG_SECTION, option=str_field, raw=True)
                setattr(self, str_field, value)

            for int_field in int_fields:
                value = self.config.get(section=CONFIG_SECTION, option=int_field, raw=True)

                try:
                    value = int(value)
                except ValueError:
                    raise Exception("Can't parse config file. Field '{0}' must ve an integer.".format(int_field))

                setattr(self, int_field, value)

            for list_field in space_separated_list_fields:
                value = self.config.get(section=CONFIG_SECTION, option=list_field, raw=True)
                value = value.split()
                setattr(self, list_field, value)

        except configparser.NoSectionError as e:
            raise Exception(self.message.format("Missing Section: %s" % e))
        except configparser.NoOptionError as e:
            raise Exception(self.message.format("Missing Option: %s" % e))
        except Exception as e:
            raise Exception(self.message.format(e))


if __name__ == '__main__':
    """ Example of using Config.
    """

    config = Config()
    print("tcp buffer size: {}. Type: {} ".format(config.tcp_buffer_size, type(config.tcp_buffer_size)))
    print("udp buffer size: {}. Type: {} ".format(config.udp_buffer_size, type(config.udp_buffer_size)))
