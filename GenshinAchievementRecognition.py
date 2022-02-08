import json
import os
import re
import time
from copy import copy

import cv2
import easyocr
import numpy as np
import pyautogui
import win32gui
from PIL import Image
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import QApplication, QWidget
from imutils.perspective import order_points

from exception.exception import WhereIsYourGameException, ConfigFileErrorException
from util.guiar import encode_date


class GenshinAchievementRecognition(object):
    def __init__(self):
        self.config_path: str = "gar/config.json"
        self.window_name: str = None
        self.dmax: int = None
        self.x_split_data_img_left: int = None
        self.x_split_data_img_right: int = None
        self.ocr_lang: list = None
        self.ocr_model_dir: str = None
        self.title_reformat: bool = None
        self.enable_gpu: bool = None
        self.reader: easyocr.Reader = None
        self.aw: AWindow = None
        self.sharpen_kernel: np.ndarray = None
        self.location_offset: tuple = None
        self.location2item_offset: tuple = None
        self.item2title_offset: tuple = None  # l,u,w,h
        self.item2state_offset: tuple = None  # l,u,w,h
        self.item2progress_offset: tuple = None  # l,u,w,h
        self.item2amount_offset: tuple = None  # l,u,w,h
        self.item2date_offset: tuple = None  # l,u,w,h
        self.scroll_config: tuple = None
        self.template_slash_progress: np.ndarray = None
        self.template_slash_date: np.ndarray = None
        self.template_img_complete: np.ndarray = None
        self.allow_list_num: str = "1234567890"
        self.allow_list_amount: str = None
        self.allow_list_state: str = None
        self.ocr_decoder: tuple = ("greedy", "beamsearch", "wordbeamsearch")
        self.ocr_decoder_index: tuple = None
        self.chtic: np.ndarray = None
        self.load_config()
        self.init()

    def load_config(self):
        config_dir_path: str = os.path.dirname(self.config_path)
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
        self.__load_ndarray_in_config()

    def __load_ndarray_in_config(self):
        self.template_slash_progress = np.array(self.template_slash_progress, dtype=np.uint8)
        self.template_slash_date = np.array(self.template_slash_date, dtype=np.uint8)
        self.sharpen_kernel = np.array(self.sharpen_kernel, dtype=np.int32)
        self.template_img_complete = np.array(self.template_img_complete, dtype=np.uint8)

    def init(self):
        self.reader = easyocr.Reader(self.ocr_lang, model_storage_directory=self.ocr_model_dir)
        self.aw = AWindow(name=self.window_name)
        self.chtic = cv2.calcHist([self.template_img_complete], [0], None, [256], [0.0, 255.0])

    def load_default_config(self):
        self.window_name = "原神"
        self.ocr_lang = ['ch_sim', 'en']
        self.ocr_model_dir = "gar/model"
        self.title_reformat = True
        self.dmax = 560
        self.x_split_data_img_left = 57
        self.x_split_data_img_right = 50
        self.allow_list_amount = ""
        self.allow_list_state = "达成1234567890/"
        self.ocr_decoder_index: tuple = (2, 1, 0, 0, 0, 0, 0, 0)
        self.enable_gpu: bool = False
        self.template_slash_progress = [
            [[215, 227, 237], [214, 226, 236], [214, 226, 236], [211, 223, 233], [183, 197, 209], [188, 202, 214]],
            [[212, 224, 234], [212, 224, 234], [211, 223, 233], [194, 206, 216], [162, 176, 188], [169, 183, 195]],
            [[214, 226, 236], [215, 227, 237], [210, 224, 236], [178, 192, 204], [154, 168, 180], [174, 188, 200]],
            [[214, 226, 236], [214, 226, 236], [203, 217, 229], [164, 178, 190], [157, 171, 183], [194, 208, 220]],
            [[211, 225, 237], [211, 225, 237], [192, 206, 218], [153, 167, 179], [164, 178, 190], [207, 221, 233]],
            [[212, 226, 238], [210, 224, 236], [182, 196, 208], [153, 167, 179], [176, 190, 202], [211, 225, 237]],
            [[208, 224, 237], [200, 216, 229], [166, 180, 192], [156, 170, 182], [191, 205, 217], [212, 226, 238]],
            [[209, 225, 238], [194, 210, 223], [154, 167, 181], [160, 174, 186], [204, 218, 230], [214, 228, 240]],
            [[205, 221, 237], [180, 197, 210], [149, 165, 178], [171, 187, 200], [208, 222, 234], [215, 229, 241]],
            [[201, 217, 233], [166, 182, 198], [152, 168, 181], [186, 202, 215], [211, 225, 237], [212, 226, 238]],
            [[193, 209, 225], [152, 168, 184], [159, 175, 188], [201, 217, 230], [213, 227, 239], [212, 226, 238]],
            [[185, 201, 217], [147, 163, 179], [167, 183, 196], [207, 223, 236], [211, 225, 237], [214, 228, 240]]]
        self.template_slash_date = [[[235, 244, 248], [233, 242, 246], [197, 211, 223], [173, 187, 199]],
                                    [[232, 241, 245], [228, 237, 241], [176, 190, 202], [164, 178, 190]],
                                    [[234, 243, 247], [223, 232, 236], [166, 178, 188], [177, 189, 199]],
                                    [[232, 241, 245], [205, 214, 218], [161, 173, 183], [199, 211, 221]],
                                    [[229, 239, 246], [180, 190, 197], [164, 175, 183], [216, 227, 235]],
                                    [[225, 235, 242], [168, 178, 185], [176, 187, 195], [224, 235, 243]],
                                    [[198, 210, 220], [160, 172, 182], [194, 204, 214], [226, 236, 246]],
                                    [[174, 186, 196], [160, 172, 182], [209, 219, 229], [227, 237, 247]],
                                    [[165, 180, 196], [170, 185, 201], [224, 236, 248], [220, 232, 244]],
                                    [[167, 182, 198], [180, 195, 211], [220, 232, 244], [226, 238, 250]]]
        self.template_img_complete = self.__get_default_template_img_complete()
        self.sharpen_kernel = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
        self.location_offset = (80, -50, 1045, -170)
        self.location2item_offset = (-18, 18, -565, 125)
        self.item2title_offset = (90, 10, 475, 40)  # l,u,w,h
        self.item2state_offset = (665, 30, 35, 20)  # l,u,w,h
        self.item2progress_offset = (630, 31, 95, 18)  # l,u,w,h
        self.item2amount_offset = (625, 38, 105, 18)  # l,u,w,h
        self.item2date_offset = (636, 60, 88, 17)  # l,u,w,h
        self.scroll_config = (1230, 130, 500)
        return {
            "window_name": self.window_name,
            "enable_gpu": self.enable_gpu,
            "ocr_lang": self.ocr_lang,
            "ocr_model_dir": self.ocr_model_dir,
            "title_reformat": self.title_reformat,
            "allow_list_amount": self.allow_list_amount,
            "allow_list_state": self.allow_list_state,
            "dmax": self.dmax,
            "x_split_data_img_left": self.x_split_data_img_left,
            "x_split_data_img_right": self.x_split_data_img_right,
            "ocr_decoder_index": self.ocr_decoder_index,
            "sharpen_kernel": self.sharpen_kernel,
            "location_offset": self.location_offset,
            "location2item_offset": self.location2item_offset,
            "item2title_offset": self.item2title_offset,
            "item2state_offset": self.item2state_offset,
            "item2progress_offset": self.item2progress_offset,
            "item2amount_offset": self.item2amount_offset,
            "item2date_offset": self.item2date_offset,
            "scroll_config": self.scroll_config,
            "template_slash_progress": self.template_slash_progress,
            "template_slash_date": self.template_slash_date,
            "template_img_complete": self.template_img_complete,
        }

    def generate_default_config_file(self, filepath=None):
        _filepath = filepath
        if filepath is None:
            _filepath = self.config_path
        config = self.load_default_config()
        with open(self.config_path, "w", encoding='utf-8-sig') as f:
            f.write(json.dumps(config, indent=3, ensure_ascii=False).encode("utf-8-sig").decode("utf-8-sig"))
        return config

    def capture(self):
        if self.aw.window == 0:
            self.aw.update_window()
            if self.aw.window == 0:
                raise WhereIsYourGameException(self.window_name)
        return self.aw.capture_window()

    def recognize(self, reformat: bool = True):
        image = self.capture()
        origin_image = np.array(image, dtype=np.uint8)
        if origin_image.shape[0] == 1:
            from exception.exception import GameCaptureException
            raise GameCaptureException()
        gray = cv2.cvtColor(origin_image, cv2.COLOR_BGR2GRAY)
        _, location_binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        location_cropped_binary = location_binary[
                                  self.location_offset[0]:self.location_offset[1],
                                  self.location_offset[2]:self.location_offset[3]]
        cnts, _ = cv2.findContours(location_cropped_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxs = np.array([np.int0(cv2.boxPoints(cv2.minAreaRect(c))) for c in cnts], dtype=np.int32)
        boxs = sorted(boxs, key=lambda x: x[:, 1].min())
        record = []

        for box in boxs:
            area = cv2.contourArea(box)
            if area < 1980:
                continue
            _dmax = box[:, 1].max()
            if _dmax > self.dmax:
                continue
            title, amount, progress, target_progress, year, month, day = "", 1, -1, -1, -1, -1, -1
            box = order_points(box)
            box = box.astype(dtype=np.int32)
            box = self.apply_location_offset(box)
            box = self.apply_location2item_box(box)
            box_title = self.apply_item2title_box(box)
            img_title = self.transform_crop_by_box(origin_image, box_title)
            result_title = self.reader.recognize(img_title, decoder=self.ocr_decoder[self.ocr_decoder_index[0]])
            title = result_title[0][1]
            if self.title_reformat:
                title = re.sub(r'[^\w]', '', title).replace("_", "")
            box_amount_text = self.apply_item2amount_box(box)
            img_amount_text = self.transform_crop_by_box(origin_image, box_amount_text)
            img_amount_text = self.transform_rds(img_amount_text)
            result_amount_text = self.reader.recognize(img_amount_text,
                                                       decoder=self.ocr_decoder[self.ocr_decoder_index[1]],
                                                       allowlist=self.allow_list_amount)
            is_achievement_complete = 0
            if "总" in result_amount_text[0][1] or "计" in result_amount_text[0][1]:
                t_amount: str = copy(result_amount_text[0][1])[::-1]
                tt_amount = ""
                for ta in t_amount:
                    if ta.isdigit():
                        tt_amount += ta
                    else:
                        break
                try:
                    amount = int(tt_amount[::-1])
                except:
                    amount = 1
                is_achievement_complete = 1
            else:
                box_state = self.apply_item2state_box(box)
                img_state = self.transform_crop_by_box(origin_image, box_state)
                img_state = self.make_clear(img_state, [200, 255], 200)
                result_state = self.reader.recognize(img_state, decoder=self.ocr_decoder[self.ocr_decoder_index[2]],
                                                     allowlist=self.allow_list_state)
                if "达" in result_state[0][1] or "成" in result_state[0][1]:
                    is_achievement_complete = 1
                else:
                    box_progress = self.apply_item2progress_box(box)
                    img_progress = self.transform_crop_by_box(origin_image, box_progress)
                    result_template = cv2.matchTemplate(img_progress, self.template_slash_progress,
                                                        cv2.TM_SQDIFF_NORMED)
                    cv2.normalize(result_template, result_template, 0, 1, cv2.NORM_MINMAX, -1)
                    _, _, min_loc, _ = cv2.minMaxLoc(result_template)
                    img_target_progress = img_progress[:, min_loc[0] + self.template_slash_progress.shape[1] - 1:]
                    img_target_progress = self.make_clear(img_target_progress, [190, 255], 100)
                    result_target_progress = self.reader.recognize(img_target_progress,
                                                                   decoder=self.ocr_decoder[self.ocr_decoder_index[3]],
                                                                   allowlist=self.allow_list_num)
                    try:
                        target_progress = int(result_target_progress[0][1])
                    except:
                        target_progress = -1
                    img_progress = img_progress[:, :min_loc[0] + 1]
                    img_progress = self.make_clear(img_progress, [190, 255], 100)
                    result_progress = self.reader.recognize(img_progress,
                                                            decoder=self.ocr_decoder[self.ocr_decoder_index[4]],
                                                            allowlist=self.allow_list_num)
                    try:
                        progress = int(result_progress[0][1])
                    except:
                        progress = -1
            if is_achievement_complete:
                box_date = self.apply_item2date_box(box)
                img_date = self.transform_crop_by_box(origin_image, box_date)
                img_date = cv2.cvtColor(img_date, cv2.COLOR_BGR2RGB)

                img_date_split_for_slash_left = img_date[:, :self.x_split_data_img_left]
                result_template_left = cv2.matchTemplate(img_date_split_for_slash_left, self.template_slash_date,
                                                         cv2.TM_SQDIFF_NORMED)
                cv2.normalize(result_template_left, result_template_left, 0, 1, cv2.NORM_MINMAX, -1)
                _, _, left_slash_min_loc, _ = cv2.minMaxLoc(result_template_left)
                left_slash_anchor_x = left_slash_min_loc[0] + self.template_slash_date.shape[1]
                img_year = img_date[:, :left_slash_min_loc[0] + 1]
                img_year = self.transform_rds(img_year)
                img_year = self.make_clear(img_year, [205, 255], 55)
                result_year = self.reader.recognize(img_year, decoder=self.ocr_decoder[self.ocr_decoder_index[5]],
                                                    allowlist=self.allow_list_num)
                year = result_year[0][1]
                try:
                    year = int(year[-4:])
                except:
                    year = -1
                img_date_split_for_slash_right = img_date[:, self.x_split_data_img_right:]
                result_template_right = cv2.matchTemplate(img_date_split_for_slash_right,
                                                          self.template_slash_date,
                                                          cv2.TM_SQDIFF_NORMED)
                cv2.normalize(result_template_right, result_template_right, 0, 1, cv2.NORM_MINMAX, -1)
                _, _, right_slash_min_loc, _ = cv2.minMaxLoc(result_template_right)
                right_slash_anchor_x = self.x_split_data_img_right + right_slash_min_loc[0]
                img_day = img_date[:, right_slash_anchor_x + self.template_slash_date.shape[1] + 1:]
                img_day = self.transform_rds(img_day)
                img_day = self.make_clear(img_day, [200, 255], 120)
                result_day = self.reader.recognize(img_day, decoder=self.ocr_decoder[self.ocr_decoder_index[6]],
                                                   allowlist=self.allow_list_num)
                day = result_day[0][1]
                try:
                    day = int(day)
                except:
                    day = -1
                img_month = img_date[:, left_slash_anchor_x + 1:right_slash_anchor_x - 1]
                img_month = self.transform_rds(img_month)
                img_month = self.make_clear(img_month, [200, 255], 125)
                result_month = self.reader.recognize(img_month, decoder=self.ocr_decoder[self.ocr_decoder_index[7]],
                                                     allowlist=self.allow_list_num)
                try:
                    month = int(result_month[0][1])
                except:
                    month = -1
            if reformat:
                if is_achievement_complete:
                    record.append((title, is_achievement_complete, encode_date(year, month, day), amount))
                else:
                    record.append((title, is_achievement_complete, progress, target_progress))
            else:
                record.append((title, year, month, day, amount, progress, target_progress))
        final_result = tuple(record)
        return final_result

    def recognize_uid(self, val=100):
        img = self.aw.capture_window()
        img = np.array(img, dtype=np.uint8)
        if img.shape[0] == 1:
            from exception.exception import GameCaptureException
            raise GameCaptureException()
        img = img[-20:, -120:-20]
        img = self.make_clear(img, [254, 255], val)
        result = self.reader.recognize(img, decoder='greedy',
                                       allowlist="1234567890", detail=0)[0]
        if len(result) != 9:
            return -1
        else:
            try:
                result = int(result)
                return result
            except:
                return -1

    @staticmethod
    def make_clear(img, thres, val):
        img = img.copy()
        b = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, ba = cv2.threshold(b, thres[0], 255, cv2.THRESH_BINARY)
        _, bb = cv2.threshold(b, thres[1], 255, cv2.THRESH_BINARY_INV)
        img[img <= val] = val
        img[ba != 255] -= val
        img[bb != 255] -= val + thres[1] - thres[0]
        return img

    def scroll_down(self):
        try:
            win32gui.SetForegroundWindow(self.aw.window)
        except:
            from exception.exception import WhereIsYourGameException
            raise WhereIsYourGameException(self.window_name)
        x, y, _, _ = self.aw.get_window_rect()
        pyautogui.mouseDown(x + self.scroll_config[0], y + self.scroll_config[1] + self.scroll_config[2])
        time.sleep(0.1)
        pyautogui.moveTo(x + self.scroll_config[0], y + self.scroll_config[1], duration=0.5)
        # time.sleep(0.1)
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    def transform_rds(self, x, val=4):
        x = cv2.resize(x, (int(x.shape[1] * val), int(x.shape[0] * val)))
        x = cv2.fastNlMeansDenoisingColored(x, None, 3, 3, 7, 21)
        x = self.img_sharpen(x)
        return x

    def apply_location_offset(self, box):
        box[:, 0] += self.location_offset[2]
        box[:, 1] += self.location_offset[0]
        return box

    def apply_location2item_box(self, box):
        box[0, 0] += self.location2item_offset[2]
        box[0, 1] += self.location2item_offset[0]
        box[1, 0] += self.location2item_offset[3]
        box[1, 1] += self.location2item_offset[0]
        box[2, 0] += self.location2item_offset[3]
        box[2, 1] += self.location2item_offset[1]
        box[3, 0] += self.location2item_offset[2]
        box[3, 1] += self.location2item_offset[1]
        return box

    @staticmethod
    def transform_box_luwh(box, luwh):
        box_lu = box[0, :] + luwh[:2]
        box_rd = box_lu[:] + luwh[-2:]
        box_luwh = np.array([box_lu, (box_rd[0], box_lu[1]), box_rd, (box_lu[0], box_rd[1])])
        return box_luwh

    @staticmethod
    def transform_crop_by_box(_img, _box):
        return _img[_box[0][1]:_box[2][1], _box[0][0]:_box[2][0]]

    def apply_item2title_box(self, box):
        return self.transform_box_luwh(box, self.item2title_offset)

    def apply_item2state_box(self, box):
        return self.transform_box_luwh(box, self.item2state_offset)

    def apply_item2amount_box(self, box):
        return self.transform_box_luwh(box, self.item2amount_offset)

    def apply_item2progress_box(self, box):
        return self.transform_box_luwh(box, self.item2progress_offset)

    def apply_item2date_box(self, box):
        return self.transform_box_luwh(box, self.item2date_offset)

    def img_sharpen(self, img):
        return cv2.filter2D(img, -1, kernel=self.sharpen_kernel)

    @staticmethod
    def __get_default_template_img_complete():
        return [[[235, 227, 216], [235, 227, 215], [235, 225, 213], [235, 227, 216], [234, 224, 211], [234, 224, 211],
                 [237, 228, 216], [237, 228, 216], [236, 228, 216], [234, 224, 210], [234, 223, 209], [234, 223, 209],
                 [234, 224, 209], [236, 227, 215], [237, 228, 216], [237, 228, 216], [234, 224, 210], [234, 223, 209],
                 [234, 223, 210], [234, 224, 211], [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 225, 213],
                 [234, 223, 209], [234, 223, 208], [234, 223, 209], [237, 228, 216], [235, 227, 216], [235, 227, 216],
                 [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216], [232, 223, 209]],
                [[235, 227, 216], [236, 227, 214], [234, 224, 211], [235, 227, 216], [234, 224, 211], [234, 224, 210],
                 [237, 228, 216], [237, 228, 216], [237, 228, 216], [235, 226, 214], [235, 226, 214], [235, 226, 215],
                 [234, 223, 209], [235, 226, 212], [236, 228, 216], [235, 226, 214], [234, 223, 209], [234, 223, 208],
                 [234, 224, 210], [235, 225, 212], [237, 228, 216], [237, 228, 216], [237, 228, 215], [234, 223, 210],
                 [234, 223, 210], [234, 223, 209], [234, 223, 209], [237, 228, 216], [235, 227, 216], [235, 227, 216],
                 [235, 227, 216], [235, 227, 216], [235, 227, 216], [234, 226, 214], [228, 217, 200]],
                [[235, 227, 216], [236, 227, 215], [235, 224, 210], [236, 226, 214], [235, 224, 212], [235, 223, 209],
                 [237, 228, 215], [237, 228, 216], [237, 228, 216], [235, 226, 214], [229, 216, 204], [231, 219, 205],
                 [235, 224, 211], [235, 225, 212], [236, 228, 216], [234, 226, 213], [234, 224, 210], [234, 223, 209],
                 [234, 223, 209], [236, 227, 214], [237, 228, 216], [237, 228, 216], [235, 228, 216], [229, 217, 203],
                 [231, 220, 206], [234, 225, 212], [229, 218, 204], [238, 229, 218], [235, 227, 216], [235, 227, 216],
                 [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 215], [233, 224, 212]],
                [[235, 227, 216], [236, 228, 216], [232, 221, 207], [219, 205, 188], [217, 202, 185], [235, 224, 211],
                 [236, 227, 214], [237, 228, 216], [236, 227, 216], [227, 218, 204], [202, 186, 168], [214, 200, 183],
                 [236, 226, 214], [236, 227, 214], [235, 227, 215], [234, 224, 211], [234, 224, 210], [234, 224, 211],
                 [235, 226, 214], [237, 228, 216], [237, 228, 216], [237, 228, 216], [232, 223, 210], [203, 187, 168],
                 [210, 194, 177], [218, 205, 190], [206, 189, 171], [229, 218, 206], [236, 228, 218], [235, 227, 216],
                 [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216]],
                [[235, 227, 216], [236, 228, 216], [232, 220, 208], [206, 190, 172], [196, 176, 156], [221, 208, 193],
                 [236, 229, 220], [237, 228, 218], [236, 227, 217], [223, 212, 199], [189, 168, 147], [206, 188, 171],
                 [238, 231, 221], [236, 227, 216], [234, 225, 212], [234, 223, 211], [236, 224, 211], [233, 225, 213],
                 [232, 223, 212], [234, 224, 212], [234, 224, 212], [234, 224, 212], [226, 216, 203], [190, 169, 147],
                 [197, 178, 159], [218, 206, 192], [198, 179, 159], [207, 191, 175], [231, 224, 211], [236, 226, 216],
                 [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216]],
                [[235, 227, 216], [236, 228, 216], [235, 226, 213], [222, 209, 193], [199, 181, 162], [199, 182, 161],
                 [225, 214, 201], [227, 216, 203], [226, 215, 203], [215, 202, 187], [188, 168, 147], [203, 185, 168],
                 [228, 218, 205], [225, 214, 200], [227, 214, 201], [235, 226, 214], [233, 224, 212], [217, 205, 190],
                 [203, 186, 169], [203, 187, 169], [204, 187, 169], [203, 187, 169], [201, 184, 166], [188, 167, 146],
                 [191, 171, 151], [203, 185, 168], [192, 172, 152], [190, 170, 149], [207, 191, 173], [232, 223, 210],
                 [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216]],
                [[235, 227, 216], [236, 227, 216], [238, 229, 217], [235, 225, 212], [226, 213, 199], [216, 201, 185],
                 [223, 210, 196], [201, 183, 164], [201, 183, 165], [197, 179, 160], [187, 166, 145], [192, 173, 152],
                 [201, 183, 163], [200, 181, 162], [206, 189, 171], [235, 225, 212], [231, 221, 209], [208, 193, 177],
                 [189, 169, 148], [204, 189, 171], [211, 198, 182], [211, 196, 180], [209, 194, 176], [193, 173, 153],
                 [190, 171, 150], [209, 194, 178], [213, 199, 183], [211, 197, 180], [216, 202, 187], [234, 226, 214],
                 [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216]],
                [[235, 227, 215], [235, 226, 214], [228, 217, 204], [214, 200, 183], [215, 200, 183], [216, 202, 185],
                 [233, 222, 210], [217, 203, 188], [218, 204, 189], [204, 188, 170], [189, 167, 147], [203, 186, 167],
                 [218, 205, 190], [218, 205, 189], [220, 208, 191], [235, 226, 213], [233, 224, 212], [209, 193, 177],
                 [192, 172, 152], [219, 206, 192], [231, 222, 211], [230, 219, 206], [226, 214, 200], [201, 185, 166],
                 [193, 173, 153], [226, 215, 200], [224, 212, 198], [204, 186, 168], [219, 205, 189], [236, 224, 211],
                 [235, 225, 212], [235, 226, 213], [236, 227, 215], [235, 227, 216], [235, 227, 216]],
                [[233, 225, 213], [232, 222, 211], [222, 210, 196], [202, 185, 167], [193, 173, 153], [201, 183, 163],
                 [236, 228, 215], [235, 228, 216], [233, 226, 214], [208, 192, 176], [190, 169, 148], [211, 196, 180],
                 [236, 226, 215], [236, 226, 212], [235, 225, 211], [236, 227, 216], [234, 225, 213], [208, 193, 175],
                 [188, 166, 145], [199, 182, 163], [204, 188, 171], [205, 188, 172], [208, 192, 175], [209, 194, 176],
                 [192, 172, 151], [220, 208, 194], [211, 196, 180], [191, 171, 150], [222, 209, 194], [235, 224, 212],
                 [234, 223, 209], [234, 223, 208], [234, 223, 208], [234, 223, 209], [235, 226, 214]],
                [[235, 227, 216], [234, 226, 214], [232, 223, 210], [220, 208, 195], [191, 171, 150], [197, 178, 158],
                 [237, 227, 216], [235, 224, 211], [227, 219, 206], [194, 176, 156], [188, 167, 147], [197, 178, 158],
                 [218, 204, 189], [237, 226, 214], [237, 229, 216], [237, 228, 216], [234, 225, 212], [208, 192, 175],
                 [189, 169, 148], [205, 188, 170], [207, 191, 174], [187, 166, 145], [198, 180, 161], [215, 201, 186],
                 [190, 169, 148], [207, 191, 174], [196, 177, 157], [200, 182, 163], [235, 226, 214], [234, 226, 213],
                 [235, 227, 216], [234, 223, 209], [234, 223, 208], [234, 223, 208], [234, 223, 211]],
                [[235, 227, 216], [236, 226, 213], [234, 225, 212], [231, 221, 209], [193, 173, 153], [197, 178, 158],
                 [238, 228, 217], [230, 220, 206], [206, 191, 174], [191, 171, 151], [208, 193, 176], [200, 184, 165],
                 [197, 179, 159], [222, 211, 197], [238, 230, 219], [237, 228, 217], [233, 225, 212], [206, 190, 172],
                 [193, 173, 154], [224, 214, 200], [225, 214, 201], [188, 168, 146], [204, 188, 170], [225, 214, 201],
                 [188, 167, 146], [193, 173, 153], [193, 174, 153], [220, 207, 192], [235, 225, 212], [234, 223, 209],
                 [234, 225, 213], [235, 227, 216], [234, 223, 209], [234, 223, 209], [234, 223, 209]],
                [[235, 227, 216], [235, 226, 214], [234, 223, 211], [230, 219, 207], [192, 173, 153], [197, 178, 158],
                 [231, 221, 209], [208, 193, 176], [196, 177, 158], [213, 199, 184], [233, 223, 211], [225, 215, 200],
                 [201, 184, 165], [200, 181, 163], [225, 213, 199], [238, 229, 218], [232, 223, 212], [202, 185, 166],
                 [194, 176, 156], [231, 222, 210], [226, 216, 203], [189, 169, 147], [208, 191, 175], [231, 222, 210],
                 [194, 174, 154], [190, 170, 149], [208, 194, 177], [236, 227, 215], [237, 229, 217], [236, 227, 215],
                 [236, 225, 213], [235, 224, 212], [234, 223, 209], [234, 223, 209], [234, 223, 208]],
                [[235, 227, 215], [235, 227, 217], [234, 226, 216], [221, 209, 195], [190, 170, 149], [194, 174, 153],
                 [215, 201, 186], [207, 191, 173], [220, 207, 194], [232, 224, 213], [238, 229, 219], [236, 228, 218],
                 [226, 215, 202], [209, 194, 177], [211, 196, 180], [238, 228, 217], [231, 222, 210], [196, 176, 156],
                 [200, 183, 163], [231, 221, 209], [217, 205, 190], [190, 170, 148], [209, 194, 176], [222, 211, 197],
                 [191, 171, 150], [191, 171, 150], [218, 205, 189], [239, 231, 221], [236, 228, 216], [233, 223, 210],
                 [237, 229, 217], [237, 228, 216], [237, 228, 216], [235, 225, 212], [234, 223, 209]],
                [[234, 223, 209], [233, 221, 208], [221, 208, 195], [199, 180, 161], [191, 171, 150], [195, 175, 155],
                 [197, 179, 159], [210, 195, 178], [223, 211, 196], [224, 214, 199], [225, 215, 202], [225, 215, 202],
                 [226, 215, 201], [219, 207, 193], [215, 202, 185], [231, 220, 209], [222, 211, 198], [193, 173, 152],
                 [213, 199, 184], [212, 198, 181], [197, 178, 159], [192, 172, 151], [204, 189, 171], [202, 185, 166],
                 [200, 182, 163], [193, 173, 152], [205, 188, 170], [227, 216, 203], [218, 205, 190], [224, 213, 199],
                 [237, 229, 217], [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216]],
                [[234, 223, 208], [232, 221, 207], [218, 204, 189], [196, 176, 156], [218, 205, 190], [218, 205, 190],
                 [200, 182, 163], [199, 181, 161], [200, 182, 163], [199, 181, 161], [201, 183, 163], [201, 184, 165],
                 [202, 184, 165], [202, 184, 165], [204, 188, 170], [220, 207, 193], [206, 191, 174], [207, 191, 173],
                 [232, 222, 211], [224, 212, 198], [216, 202, 187], [213, 199, 182], [203, 187, 169], [215, 200, 184],
                 [225, 212, 198], [211, 196, 178], [191, 171, 150], [200, 183, 165], [205, 188, 170], [230, 220, 206],
                 [237, 229, 217], [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216]],
                [[236, 225, 211], [236, 227, 215], [231, 221, 209], [222, 210, 195], [236, 228, 216], [236, 227, 215],
                 [226, 215, 202], [220, 206, 191], [218, 205, 189], [218, 205, 188], [219, 206, 189], [220, 207, 193],
                 [220, 207, 193], [220, 207, 193], [222, 209, 194], [227, 217, 205], [218, 205, 189], [229, 218, 205],
                 [238, 229, 219], [238, 228, 216], [236, 228, 216], [233, 223, 211], [223, 209, 194], [233, 222, 208],
                 [235, 224, 211], [229, 220, 208], [213, 199, 184], [209, 192, 174], [221, 209, 195], [235, 225, 214],
                 [234, 223, 209], [235, 226, 211], [236, 227, 214], [237, 228, 216], [237, 228, 216]],
                [[235, 227, 216], [235, 227, 216], [237, 229, 217], [236, 227, 216], [237, 228, 217], [237, 228, 217],
                 [237, 229, 217], [236, 228, 216], [235, 227, 214], [235, 226, 212], [235, 226, 212], [237, 230, 218],
                 [236, 230, 218], [237, 230, 218], [237, 229, 217], [237, 228, 217], [233, 223, 211], [238, 229, 217],
                 [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 227, 216], [234, 222, 209], [234, 223, 209],
                 [234, 223, 208], [236, 227, 216], [232, 224, 213], [230, 218, 203], [234, 224, 210], [234, 224, 209],
                 [234, 223, 209], [234, 223, 209], [234, 223, 208], [235, 225, 211], [237, 227, 215]],
                [[235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 226, 212], [235, 225, 211],
                 [235, 225, 212], [235, 225, 211], [235, 226, 212], [236, 227, 215], [236, 228, 215], [237, 228, 216],
                 [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216],
                 [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216], [234, 223, 208], [234, 222, 208],
                 [234, 222, 208], [234, 225, 213], [235, 227, 216], [235, 227, 216], [234, 225, 214], [234, 223, 209],
                 [234, 223, 208], [234, 223, 208], [234, 224, 208], [236, 227, 213], [229, 216, 198]],
                [[235, 227, 216], [235, 227, 216], [235, 227, 216], [235, 227, 216], [234, 223, 208], [234, 223, 208],
                 [234, 223, 208], [234, 223, 208], [234, 223, 208], [234, 223, 208], [234, 223, 209], [235, 224, 212],
                 [235, 226, 215], [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216], [237, 228, 216],
                 [237, 228, 216], [237, 228, 215], [234, 224, 209], [237, 228, 215], [235, 225, 211], [234, 222, 208],
                 [234, 222, 208], [235, 227, 216], [235, 227, 216], [236, 227, 216], [235, 225, 212], [235, 224, 211],
                 [234, 223, 208], [234, 223, 208], [235, 226, 212], [233, 223, 207], [225, 209, 188]],
                [[236, 226, 213], [235, 226, 215], [234, 223, 209], [234, 223, 209], [234, 223, 208], [234, 223, 208],
                 [234, 223, 208], [234, 223, 209], [234, 223, 209], [234, 223, 208], [234, 223, 208], [234, 222, 209],
                 [234, 222, 209], [235, 225, 213], [237, 228, 215], [237, 228, 216], [237, 228, 216], [237, 228, 216],
                 [237, 228, 215], [234, 223, 209], [234, 223, 208], [236, 226, 213], [237, 228, 215], [234, 222, 208],
                 [234, 222, 208], [234, 223, 211], [235, 226, 215], [237, 227, 216], [235, 227, 216], [236, 227, 216],
                 [237, 228, 215], [236, 226, 214], [235, 226, 213], [226, 212, 193], [225, 209, 189]]]


class AWindow:
    def __init__(self, cls=None, name=None):
        self.cls = cls
        self.name = name
        self.__app = QApplication([])
        self.__screen: QScreen = QApplication.primaryScreen()
        self.w = QWidget()
        self._cache_window_cls = None
        self._cache_window_caption = None
        self.window = win32gui.FindWindow(self.cls, self.name)

    def set_window(self, cls=None, name=None):
        self.cls = cls
        self.name = name
        self.update_window()

    def update_window(self):
        self.window = win32gui.FindWindow(self.cls, self.name)

    def get_window_rect(self):
        return win32gui.GetWindowRect(self.window)

    def capture_window(self) -> Image:
        t = self.__screen.grabWindow(self.window)
        return Image.fromqimage(t)
