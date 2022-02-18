import json
import logging
import os

from pruina.socket.client import PruinaSocketClient
from pruina.socket.handler.PruinaHandler import PruinaHandler
from pynput.keyboard import Listener, KeyCode

from exception.exception import ConfigFileErrorException
from util.proto.GenshinAchievementRecognition_pb2 import IdMessage, Response, Results

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class GenshinAchievementRecognitionClient(PruinaSocketClient):
    def __init__(self):
        self.host: str = None
        self.port: int = None
        self.start_key: str = None
        self.config_path: str = "gar/client_config.json"
        self.load_config()
        super().__init__(host=self.host, port=self.port)
        self.is_started: bool = False
        self.is_loading: bool = False
        self.my_id = None
        self.my_id_message = None
        self.my_id_message_bytes = None
        self.key_listener = Listener(on_release=self.key_hook)
        self.__init()

    def load_config(self):
        config_dir_path = os.path.dirname(self.config_path)
        if not os.path.exists(config_dir_path):
            os.makedirs(config_dir_path)
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding='utf-8-sig') as f:
                try:
                    config = json.loads(f.read())
                except:
                    raise ConfigFileErrorException()
        else:
            config = self.generate_default_config_file()
        self.__load_config(config)

    def __load_config(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    def load_default_config(self):
        self.host = '127.0.0.1'
        self.port = 50003
        self.start_key = 'q'
        return {
            "host": self.host,
            "port": self.port,
            "start_key": self.start_key,
        }

    def generate_default_config_file(self, filepath=None):
        _filepath = filepath
        if filepath is None:
            _filepath = self.config_path
        config = self.load_default_config()
        with open(self.config_path, "w", encoding='utf-8-sig') as f:
            f.write(json.dumps(config, indent=3, ensure_ascii=False).encode("utf-8-sig").decode("utf-8-sig"))
        return config

    def __init(self):
        try:
            self.connect()
        except:
            logging.info(f"Cannot connect to server[{self.host}:{self.port}].")
            import os
            os.system("pause")
            exit(0)
        self.start_key = KeyCode.from_char(self.start_key.lower())
        self.my_id = id(self)
        self.my_id_message = IdMessage()
        self.my_id_message.id = self.my_id
        self.my_id_message_bytes = self.my_id_message.SerializeToString()
        self.hooks.add_hook("response", self.unpack_response)
        self.hooks.add_hook("results", self.unpack_results)
        self.key_listener.start()
        logging.info(f"按[{self.start_key}]开始。")
        logging.info(f"press the key[{self.start_key}] to start.")
        logging.info(f"按其他键取消。")
        logging.info(f"press any other key to cancel.")

    def key_hook(self, key):
        if self.is_loading:
            return True
        self.is_loading = True
        if self.start_key == key:
            self.start()
        else:
            self.cancel()
        self.is_loading = False

    def start(self):
        if self.is_started:
            return
        else:
            self.is_started = True
            logging.info(f"[{self.my_id}]: Requesting...")
            self.send("start_recognition", self.my_id_message_bytes)

    def cancel(self):
        if self.is_started:
            logging.info(f"[{self.my_id}]: Canceling...")
            try:
                self.send("cancel_recognition", self.my_id_message_bytes)
            except Exception as e:
                raise e
            finally:
                self.is_started = False
        else:
            return

    def unpack_response(self, response_message_bytes, handler: PruinaHandler = None, **kwargs):
        r = Response()
        r.ParseFromString(response_message_bytes)
        logging.info(f"[{r.id}]:[{r.state}]: {r.remark}")
        if r.state == 1004 or r.state == 1003:
            self.is_started = False
        elif r.state < 0:
            self.is_started = False

    @staticmethod
    def unpack_results(results_message_bytes, handler: PruinaHandler = None, **kwargs):
        rs = Results()
        rs.ParseFromString(results_message_bytes)
        if rs.results:
            rs_str = [str(r.title) + "\t" + str(r.state) + "\t" + str(r.data_a) + "\t" + str(r.data_b) for r in
                      rs.results]
            rs_str = "\n".join(rs_str)
            logging.info("Results[len=" + str(len(rs.results)) + "]:\n" + str(rs_str))

    def except_handle(self, e, handler):
        if type(e) == ConnectionResetError:
            logging.info("Disconnect.")
            return
        else:
            raise e


if __name__ == '__main__':
    garc = GenshinAchievementRecognitionClient()
    garc.wait_until_finish()
