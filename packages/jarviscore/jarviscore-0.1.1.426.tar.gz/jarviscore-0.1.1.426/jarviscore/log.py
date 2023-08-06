from .model import Model
from .helpers import Helpers
from .settings import Settings
from pathlib import Path
from .errors import MissingSetting, ConfigFileNotFound
from pymysql.err import OperationalError

class _bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Log():
    log_format: str
    instance: str
    verbose: list
    client: str
    model: Model

    def __init__(self, instance, client="Twitch", verbose=None):
        self.enable_db = False
        self.verbose = ["debug", "log", "info", "warn", "error"]
        self.log_format = "\033[92m{time}\033[0m ({level}) [{instance}]: {message}"
        self.chat_log_format = "\033[92m{time}\033[0m ({level}) [{instance}] {chatter}: {message}"
        self.log_file_format = "{time} ({level}) [{instance}]: {message}\n"
        self.instance = instance
        self.client = client
        try:
            settings = Settings()
            if settings.has_key("database.user") and settings.has_key("database.pass") and settings.has_key("database.name"):
                self.enable_db = True
            else:
                raise MissingSetting("Database Settings are not present.")
            try:
                self.model = Model()
                self.__confirm_log_table()
            except OperationalError:
                self.enable_db = False
                self.debug("Database connection could not be established, ensure the databse is available.")
        except ConfigFileNotFound:
            # Config file doesn't exist
            pass
        except KeyError:
            # database setting key does not exist
            pass
        except MissingSetting:
            # Databse Settings don't exist
            pass

        if verbose is None:
            try:
                verbose = Settings().get_setting("log")
            except MissingSetting:
                verbose = "log"
            except ConfigFileNotFound:
                verbose = "log"
        

        if verbose == "debug":
            self.verbose = ["debug", "log", "info", "warn", "error"]
        elif verbose == "log":
            self.verbose = ["log", "info", "warn", "error"]
        elif verbose == "info":
            self.verbose = ["info", "warn", "error"]
        elif verbose == "warn":
            self.verbose = ["warn", "error"]
        elif verbose == "error":
            self.verbose = ["error"]


    def debug(self, message):
        if "debug" in self.verbose:
            self.__render({
                "time": Helpers().get_timestamp(),
                "level": "dbug",
                "instance": self.instance,
                "message": message
            })
        self.__record(message, "debug")

    def log(self, message):
        if "log" in self.verbose:
            self.__render({
                "time": Helpers().get_timestamp(),
                "level": "log_",
                "instance": self.instance,
                "message": message
            })
        self.__record(message, "log")

    
    def info(self, message):
        if "info" in self.verbose:        
            self.__render({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.OKBLUE}info{_bcolors.ENDC}",
                "instance": self.instance,
                "message": message
            })
        self.__record(message, "info")

    def sent(self, message, channel, jid=None, sid=None):
        if "info" in self.verbose:        
            self.__render_chat({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.HEADER}sent{_bcolors.ENDC}",
                "instance": f"{_bcolors.OKGREEN}{channel}{_bcolors.ENDC}",
                "chatter": f"{_bcolors.HEADER}BOT{_bcolors.ENDC}",
                "message": message
            })
        self.__record(f"[BOT::Sent]: {message}", "chat")
        if jid is not None:
            self.__record_chat(message, "BOT::Sent", channel, jid, sid)
        
    
    def sent_whisper(self, message, channel):
        if "info" in self.verbose:        
            self.__render_chat({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.HEADER}whisper{_bcolors.ENDC}",
                "instance": f"{_bcolors.OKGREEN}{channel}{_bcolors.ENDC}",
                "chatter": f"{_bcolors.HEADER}BOT{_bcolors.ENDC}",
                "message": message
            })
        self.__record(f"[BOT::Sent]: {message}", "whisper")
    
    def whisper(self, message, channel):
        if "info" in self.verbose:        
            self.__render({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.OKBLUE}whisper{_bcolors.ENDC}",
                "instance": f"{_bcolors.OKGREEN}{channel}{_bcolors.ENDC}",
                "message": message
            })
        self.__record(message, "whisper")
    
    def chat(self, message, channel, chatter, jid=None, sid=None):
        if "info" in self.verbose:        
            self.__render_chat({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.OKBLUE}chat{_bcolors.ENDC}",
                "instance": f"{_bcolors.OKGREEN}{channel}{_bcolors.ENDC}",
                "chatter": f"{_bcolors.WARNING}{chatter}{_bcolors.ENDC}",
                "message": message
            })
        self.__record(f"[{channel}].[{chatter}]: {message}", "chat")
        if jid is not None:
            self.__record_chat(message, chatter, channel, jid, sid)

    
    def warn(self, message):
        if "warn" in self.verbose:
            self.__render({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.WARNING}warn{_bcolors.ENDC}",
                "instance": self.instance,
                "message": f"{_bcolors.WARNING}{message}{_bcolors.ENDC}"
            })
        self.__record(message, "warn")
        self.__send_pushover_alert(message, "warn")

    
    def error(self, message):
        if "error" in self.verbose:
            self.__render({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.FAIL}errr{_bcolors.ENDC}",
                "instance": self.instance,
                "message": f"{_bcolors.FAIL}{message}{_bcolors.ENDC}"
            })
        self.__record(message, "error")
        self.__send_pushover_alert(message, "error")

    def exception(self, message):
        if "error" in self.verbose:
            self.__render({
                "time": Helpers().get_timestamp(),
                "level": f"{_bcolors.FAIL}excp{_bcolors.ENDC}",
                "instance": self.instance,
                "message": f"{_bcolors.FAIL}{message}{_bcolors.ENDC}"
            })
        self.__record(message, "exception")
        self.__send_pushover_alert(message, "exception")

    def set_verbose(self, verbose):
        self.info(f"Updating verbosity to '{verbose}'")
        if verbose == "debug":
            self.verbose = ["debug", "log", "info", "warn", "error"]
        elif verbose == "log":
            self.verbose = ["log", "info", "warn", "error"]
        elif verbose == "info":
            self.verbose = ["info", "warn", "error"]
        elif verbose == "warn":
            self.verbose = ["warn", "error"]
        elif verbose == "error":
            self.verbose = ["error"]

    def set_instance(self, instance):
        self.instance = instance

    def __render(self, data):
        print(self.log_format.format(**data))
    
    def __render_chat(self, data):
        print(self.chat_log_format.format(**data))


    def __record_chat(self, message, chatter, channel, jarvis_id, stream_id = None, retry = True):
        sanitisedMessage = message \
            .replace("'", "''") \
            .replace("\"","\"\"")
        if stream_id is None: 
            query = f"""
            INSERT INTO Channel_Chat
            (IdentityID, Channel, Chatter_DisplayName, Message)
            VALUES
            ('{jarvis_id}','{channel}','{chatter}','{sanitisedMessage} ')
            """
        else:
            query = f"""
            INSERT INTO Channel_Chat
            (IdentityID, SRID, Channel, Chatter_DisplayName, Message)
            VALUES
            ('{jarvis_id}','{stream_id}','{channel}','{chatter}','{sanitisedMessage} ')
            """
        try:
            if self.enable_db:
                self.model.insert(query)
        except Exception as ex:
            print(f"{_bcolors.FAIL}An exception occurred saving the log to the database{_bcolors.ENDC}")
            print(f"Exception: {ex}")
            print(f"Query: {query}")
            self.__heal_model()
            if retry:
                print("Attempting single retry of db save")
                self.__record_chat(message, chatter, channel, jarvis_id, stream_id, False)
            else:
                print("retried attempt failed - couldn't save log to db")

    def __record(self, message, level, retry = True):
        sanitisedMessage = message \
            .replace("'", "''") \
            .replace("\"","\"\"")
        query = f"insert into Logs (Source, Message, LogLevel, LogTime, Component) values ('{self.instance}', '{sanitisedMessage} ', '{level}', '{Helpers().get_timestamp()}', '{self.client}')"
        try:
            if self.enable_db:
                self.model.insert(query)
        except Exception as ex:
            print(f"{_bcolors.FAIL}An exception occurred saving the log to the database{_bcolors.ENDC}")
            print(f"Exception: {ex}")
            print(f"Query: {query}")
            self.__heal_model()
            if retry:
                print("Attempting single retry of db save")
                self.__record(message, level, False)
            else:
                print("retried attempt failed - couldn't save log to db")
    
    def __send_pushover_alert(self, message: str, log_level: str):
        pass

    
    def __heal_model(self):
        print("Attempting to heal Model Object")
        settings = Settings()
        db_user = settings.get_setting("database.user")
        db_pass = settings.get_setting("database.pass")
        self.model = Model(user=db_user, password=db_pass)

    
    def __confirm_log_table(self):
        query = "SHOW TABLES LIKE 'Logs';"
        logsExist = self.model.fetchOne(query)
        if logsExist is None:
            create_logs = """CREATE TABLE `Logs` (
                `ID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
                `Source` VARCHAR(255) NOT NULL,
                `Message` TEXT NOT NULL,
                `LogLevel` VARCHAR(100) NOT NULL DEFAULT 'Undefined',
                `LogTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `Client` VARCHAR(255) NULL DEFAULT NULL,
                `Component` VARCHAR(255) NULL DEFAULT NULL,
                PRIMARY KEY (`ID`)
            )
            COLLATE='utf8mb4_bin'
            ENGINE=InnoDB
            ;"""
            self.model.update(create_logs)
            if self.model.fetchOne(query) is None:
                self.enable_db = False
                self.error("Failed to create Logs table")
            else:
                self.log("Logs table created successfully")



