"""Config file management module"""
import configparser

class ConfigManager:
    """Read and write from config file"""
# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.

    config = configparser.RawConfigParser()
    filename = "app.config"
    # backup_filename = "app_backup.config"

    @classmethod
    def readfrom_config(cls, section, key, type='string'):
        """read from config. type can have values bool,int,float"""
        cls.config.read(cls.filename)
        if cls.config.has_section(section):
            if cls.config.has_option(section, key):
                if type == 'bool':
                    return cls.config.getboolean(section, key)
                elif type == 'int':
                    return cls.config.getint(section, key)
                elif type == 'float':
                    return cls.config.getfloat(section, key)
                else:
                    return cls.config.get(section, key)
            else:
                return ""
        else:
            return ""

    # @classmethod
    # def writeto_config(cls, section, key, value):
    #     cls.config.read(cls.filename)
    #     if not cls.config.has_section(section):
    #         print("creating section"+section)
    #         cls.config.add_section(section)
    #     cls.config.set(section, key, value)
    #     # Writing our configuration file to 'example.cfg'
    #     with open(cls.filename, 'w') as configfile:
    #         cls.config.write(configfile)
    #         configfile.close()

    # @classmethod
    # def backup(cls):
    #     cls.config.read(cls.filename)
    #     if cls.config.has_section('app'):
    #         print("original config file present. Creating backup")
    #         cls.config.read(cls.filename)
    #          # Writing our configuration file to 'example.cfg'
    #         with open(cls.backup_filename, 'w') as backupConfigfile:
    #             cls.config.write(backupConfigfile)
    #             backupConfigfile.close()

    #     else:
    #         print("original config file empty. Restoring backup")
    #         cls.config.read(cls.backup_filename)
    #          # Writing our configuration file to 'example.cfg'
    #         with open(cls.filename, 'w') as configfile:
    #             cls.config.write(configfile)
    #             configfile.close()

#Test the functions here
if __name__ == '__main__':
    # ConfigManager().writeto_config('connection', 'persist', 'wss://192.168.1.4:1989/signal')
    # ConfigManager().writeto_config('device', 'username', 'MAC1234567')
    # ConfigManager().writeto_config('device', 'password', 'MAC1234567')
    #ConfigManager().writeto_config('device', 'isRegistered', 'true')
    #print(ConfigManager().readfrom_config('connection', 'persist'))
    print(ConfigManager().readfrom_config('device', 'isRegistered', 'bool'))


