import csv
import ctypes
import gc
import json
import logging
import time
from copy import copy

from pruina.socket.handler.PruinaHandler import PruinaHandler
from pruina.socket.server import PruinaSocketServer
from pyautogui import FailSafeException

from GenshinAchievementRecognition import GenshinAchievementRecognition
from exception.exception import GameCaptureException, WhereIsYourGameException, ConfigFileErrorException
from util import ResponseCode
from util.guiar import *
from util.proto.GenshinAchievementRecognition_pb2 import IdMessage, Response, Results, Result

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class GenshinAchievementRecognitionServer(PruinaSocketServer):
    def __init__(self, host: str = "127.0.0.1", port: int = 50003):
        self.host: str = host
        self.port: int = port
        self.config_path: str = "gar/server_config.json"
        self.save_record: bool = True
        self.save_record_path: str = None
        self.save_record_backup: bool = True
        self.save_record_backup_path: str = None
        self.enable_gamt: bool = True
        self.gamt_file_path: str = None
        self.gamt_map_dict: dict = None
        self.enable_title_fix: bool = True
        self.title_fix_file_path: str = None
        self.title_fix_dict: dict = None
        self.load_config()
        super(GenshinAchievementRecognitionServer, self).__init__(host=host, port=port)
        self.__server_init()
        self.resources.add_resource("GenshinAchievementRecognition", GenshinAchievementRecognition)
        self.hooks.add_hook("start_recognition", self.start_recognition, new_thread=True)
        self.hooks.add_hook("cancel_recognition", self.cancel_recognition)
        self.hooks.add_hook("heartbeat", lambda _, handler, **__: handler.send("heartbeat", b""))

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
        self.gamt_file_path = "gar/gamt.csv"
        self.title_fix_file_path = "gar/title_fix.csv"
        self.save_record_path = "gar/record/"
        self.save_record_backup_path = "gar/record/backup"
        return {
            "host": self.host,
            "port": self.port,
            "enable_gamt": self.enable_gamt,
            "gamt_file_path": self.gamt_file_path,
            "enable_title_fix": self.enable_title_fix,
            "title_fix_file_path": self.title_fix_file_path,
            "save_record": self.save_record,
            "save_record_path": self.save_record_path,
            "save_record_backup": self.save_record_backup,
            "save_record_backup_path": self.save_record_backup_path,
            "record_type": "guiar",
        }

    def generate_default_config_file(self, filepath=None):
        _filepath = filepath
        if filepath is None:
            _filepath = self.config_path
        config = self.load_default_config()
        with open(self.config_path, "w", encoding='utf-8-sig') as f:
            f.write(json.dumps(config, indent=3, ensure_ascii=False).encode("utf-8-sig").decode("utf-8-sig"))
        return config

    def load_gamt_file(self):
        with open(self.gamt_file_path, "r", encoding='utf-8-sig') as f:
            cf = csv.reader(f)
            for item in cf:
                self.gamt_map_dict[item[0]] = item[1], int(item[2]), int(item[3])

    def load_title_fix_file(self):
        with open(self.title_fix_file_path, "r", encoding='utf-8-sig') as f:
            cf = csv.reader(f)
            for item in cf:
                self.title_fix_dict[item[0]] = item[1]

    def __server_init(self):
        self.set_except_handle(self.except_handle)
        if self.enable_gamt and self.gamt_file_path:
            self.gamt_map_dict = dict()
            self.load_gamt_file()
        if self.enable_title_fix and self.title_fix_file_path:
            self.title_fix_dict = dict()
            self.load_title_fix_file()

    def start_recognition(self, id_message_bytes, handler: PruinaHandler = None, **kwargs):
        id_message = IdMessage()
        id_message.ParseFromString(id_message_bytes)
        _id: int = copy(int(id_message.id))
        str_recognition_id = f"recognition_{_id}"
        if self.properties.get(str_recognition_id) is not None:
            self.just_send_response(handler, _id, ResponseCode.ExistSameRecognitionId,
                                    "The recognize task id already exists.")
        self.just_send_response(handler, _id, ResponseCode.TaskAccepted,
                                "Task accepted.")
        logging.info(f"[{_id}]: Task accepted.")
        gar: GenshinAchievementRecognition = self.resources.get("GenshinAchievementRecognition")
        if gar is None:
            self.just_send_response(handler, _id, ResponseCode.GenshinAchievementRecognitionLoadFailed,
                                    "GenshinAchievementRecognition Component load failed.")
            return
        self.properties.set(str_recognition_id, True)
        try:
            uid = gar.recognize_uid()
            if uid == -1:
                self.just_send_response(handler, _id, ResponseCode.RecognizeUidFailed,
                                        "Failed to recognize uid. Adjust the game screen to ensure your uid is clearly visible.")
            self.just_send_response(handler, _id, ResponseCode.TaskStart, "Task started.")
            logging.info(f"[{_id}]: Task start.")
            last_title = ""
            saved_achievement_id_set = set()
            ggis = []
            while True:
                if not self.properties.get(str_recognition_id):
                    self.just_send_response(handler, _id, ResponseCode.TaskCancel, "Task canceled.")
                    logging.info(f"[{_id}]: Task canceled.")
                    break
                results = gar.recognize()
                last_results_title = copy(results[-1][0])
                if last_results_title == last_title:
                    if self.save_record:
                        self.just_send_response(handler, _id, ResponseCode.SaveFileStart,
                                                f"Start to save achievement record.")
                        logging.info(f"[{_id}]: Saving...")
                        if not os.path.exists(self.save_record_path):
                            os.makedirs(self.save_record_path)
                        file_name = f"{uid}.guiar"
                        file_path = os.path.join(self.save_record_path, file_name)
                        gbs = [generate_guiar_block(__gis, uid, i) for i, __gis in enumerate(ggis)]
                        r_gbs = []
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                r_bin_gbs = f.read()
                            if len(r_bin_gbs) > 4:
                                if self.save_record_backup:
                                    if not os.path.exists(self.save_record_backup_path):
                                        os.makedirs(self.save_record_backup_path)
                                    with open(os.path.join(self.save_record_backup_path,
                                                           f"{file_name}_{int(time.time())}"),
                                              "wb") as f:
                                        f.write(r_bin_gbs)
                                while len(r_bin_gbs) > 0:
                                    try:
                                        l, __gb = decode_binary_guiar_block(r_bin_gbs)
                                        r_bin_gbs = r_bin_gbs[l:]
                                        while len(r_gbs) - 1 < __gb.group_id:
                                            r_gbs.append(None)
                                        if uid == __gb.uid:
                                            r_gbs[__gb.group_id] = __gb
                                    except:
                                        logging.error("Guiar decode failed.")
                                        break
                        while len(gbs) < len(r_gbs):
                            gbs.append(None)
                        while len(r_gbs) < len(gbs):
                            r_gbs.append(None)
                        with open(file_path, "wb") as f:
                            for i, r_gb in enumerate(r_gbs):
                                __bin = b""
                                if r_gb is None and gbs[i] is None:
                                    continue
                                elif gbs[i] is None:
                                    __bin = encode_guiar_block(r_gb)
                                else:
                                    __bin = encode_guiar_block(gbs[i])

                                f.write(__bin)

                        self.just_send_response(handler, _id, ResponseCode.SaveFileFinish,
                                                f"Achievement record saved. [path={file_path}]")
                        logging.info(f"[{_id}]: Saved [file_name={file_name}].")
                        self.just_send_response(handler, _id, ResponseCode.TaskFinish, "Task finish.")
                        logging.info(f"[{_id}]: Task finish.")
                    break
                if self.enable_gamt:
                    gamt_results = []
                    for r in results:
                        try:
                            t = self.gamt_map(copy(r))
                            gamt_results.append(t)
                        except:
                            gamt_results.append((*r, -1, -1))
                            logging.error(f"No title named {r[0]} in gamt.")
                            self.just_send_response(handler, _id, ResponseCode.GamtMappingFailed,
                                                    f"No title named {r[0]} in gamt.")
                    results = gamt_results
                handler.send("results", self.generate_results(_id, uid, results))
                if self.save_record:
                    for r in results:
                        _, state, data_a, data_b, group_id, __id = r
                        if __id == -1 or __id in saved_achievement_id_set:
                            continue
                        else:
                            while len(ggis) - 1 < group_id:
                                ggis.append([])
                            ggis[group_id].append(generate_guiar_item(__id, state, data_a, data_b))
                            saved_achievement_id_set.add(__id)
                if not self.properties.get(str_recognition_id):
                    self.just_send_response(handler, _id, ResponseCode.TaskCancel, "Task canceled.")
                    logging.info(f"[{_id}]: Task canceled.")
                    break
                last_title = last_results_title
                gar.scroll_down()
        except IndexError as e:
            self.just_send_response(handler, _id, ResponseCode.NotInAchievementPage,
                                    "Maybe it's not the isolated achievement page in your game.")
        except FailSafeException as e:
            self.just_send_response(handler, _id, ResponseCode.MoveMouseWhenWorking,
                                    "I think your genshin window was minimized when I am working.")
        except ConnectionResetError as e:
            pass
        except GameCaptureException as e:
            self.just_send_response(handler, _id, ResponseCode.GameCaptureException, str(e))
        except WhereIsYourGameException as e:
            self.just_send_response(handler, _id, ResponseCode.WhereIsYourGame, str(e))
        except OSError as e:
            pass
        except Exception as e:
            import traceback
            logging.error(traceback.format_exc())
            self.just_send_response(handler, _id, ResponseCode.UnknownError, "Unknown Error.")
            handler.request.close()
        finally:
            gc.collect()
            self.properties.remove(str_recognition_id)

    def cancel_recognition(self, id_message_bytes, handler: PruinaHandler = None, **kwargs):
        id_message = IdMessage()
        id_message.ParseFromString(id_message_bytes)
        _id: int = copy(id_message.id)
        cf_continue = self.properties.get(f"recognition_{_id}")
        if cf_continue is None:
            self.just_send_response(handler, _id, ResponseCode.StrangeError, "cf_continue is None.")
            return
        else:
            self.properties.set(f"recognition_{_id}", False)

    @staticmethod
    def generate_response(__id: int, __state: int, __remark: str = ""):
        r = Response()
        r.id = __id
        r.state = __state
        r.remark = __remark
        return r.SerializeToString()

    @staticmethod
    def generate_results(__id: int, __uid: int, __origin_data):
        rs = Results()
        rs.id = __id
        rs.uid = __uid
        for data in __origin_data:
            r = Result()
            r.title = data[0]
            r.state = data[1]
            r.data_a = data[2]
            r.data_b = data[3]
            if len(data) == 6:
                r.group_id = data[4]
                r.id = data[4]
            rs.results.append(r)
        return rs.SerializeToString()

    def gamt_map(self, r):
        title, *data = r
        t = self.gamt_map_dict.get(title)
        if t is None:
            if self.enable_title_fix:
                tt = self.title_fix_dict.get(title)
                if tt is None:
                    raise KeyError()
                else:
                    title = tt
                    t = self.gamt_map_dict.get(title)
                    if t is None:
                        raise KeyError()
                    else:
                        title, group_id, _id = t
                        return title, *data, group_id, _id
            return title, *data, -1, -1
        else:
            title, group_id, _id = t
            return title, *data, group_id, _id

    def just_send_response(self, _handler, _id, _code, _remark):
        try:
            _handler.send("response", self.generate_response(_id, _code, _remark))
        except OSError:
            pass
        except:
            pass

    @staticmethod
    def except_handle(e, handler):
        if type(e) == ConnectionAbortedError:
            return
        if type(e) == OSError:
            return
        if type(e) == ConnectionResetError:
            return


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    import os
    import platform

    if platform.system() == "Windows":
        if platform.release() == "10":
            if not is_admin():
                logging.error("请在管理员模式下启动。")
                logging.error("Please run in administrator mode.")
                os.system('pause')
                exit(0)
        else:
            logging.error("在windows11下不能判断是否在管理员模式下启动，请自行确认是否在管理员模式下启动。")
            logging.error(
                "In Windows 11, it is not possible to determine whether to start in administrator mode, please confirm whether to start in administrator mode.")
    gar = GenshinAchievementRecognitionServer()
    gar.init()
    logging.info("Resources loading finish.")
    gar.serve_forever()
