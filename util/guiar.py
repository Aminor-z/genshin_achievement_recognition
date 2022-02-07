"""
Guiar (Genshin Impact Uniformed Interchangeable Achievement Record)
is a uniformed interchangeable compressed data format for record achievement states of Genshin Impact
interchange format.
"""
import csv
from collections import Iterable

from util.proto.Guiar_pb2 import *

export_file_header = ["成就名称", "状态", "当前进度", "目标进度", "总计", "完成日期"]
state_remark = ["已完成", "未完成"]


class MixedGuiarFileException(Exception):
    def __str__(self):
        return "The guiar file is mixed."


def generate_guiar_item(_id, state, data_a, data_b):
    gi = GuiarItem()
    gi.id = _id
    gi.state = state
    gi.data_a = data_a
    gi.data_b = data_b
    return gi


def generate_guiar_block(gis: Iterable, uid: int, group_id: int):
    if not isinstance(gis, Iterable):
        raise TypeError(f"{type(gis)} object is not iterable")
    if len(gis) == 0:
        return None
    gi: GuiarItem
    gb: GuiarBlock = GuiarBlock()
    gb.uid = uid
    gb.group_id = group_id
    for gi in gis:
        if not isinstance(gi, GuiarItem):
            raise TypeError(f"{type(gi)} object is not GuiarItem")
        else:
            gb.items.append(gi)
    return gb


def encode_guiar_block(gb: GuiarBlock):
    b_gb = gb.SerializeToString()
    return len(b_gb).to_bytes(4, byteorder='big', signed=False) + b_gb


def decode_binary_guiar_block(guiar_block_binary_results: bytes):
    block_size = int().from_bytes(guiar_block_binary_results[:4], byteorder='big', signed=False)
    gb = GuiarBlock()
    gb.ParseFromString(guiar_block_binary_results[4:4 + block_size])
    return 4 + block_size, gb


def decode_guiar_block(gb: GuiarBlock):
    uid = gb.uid
    gis = gb.items
    data_list = []
    for gi in gis:
        data_list.append([gi.id, gi.state, gi.data_a, gi.data_b])
    return uid, data_list


def encode_date(year, month, day):
    if year <= 0 or month <= 0 or day <= 0:
        return 0
    else:
        return (year - 2020) * 384 + ((month - 1) << 5) + (day - 1)


def decode_date(x):
    if x <= 0:
        return 0, 0, 0
    else:
        t = int(x / 384)
        year = t + 2020
        md = x - t * 384
        month = (md >> 5) + 1
        day = md % 32 + 1
    return year, month, day


def export_from_guiar(file_path, save_path, gamt_path="gar/gamt.csv", split_by_state=True):
    r_bin_gbs = b""
    r_gbs = []
    with open(file_path, "rb") as fr:
        r_bin_gbs = fr.read()
        while len(r_bin_gbs) > 4:
            l, r_gb = decode_binary_guiar_block(r_bin_gbs)
            r_bin_gbs = r_bin_gbs[l:]
            while len(r_gbs) - 1 < r_gb.group_id:
                r_gbs.append(None)
            r_gbs[r_gb.group_id] = r_gb
    uid = -1
    achievement_list = []
    for gb in r_gbs:
        if gb is None:
            continue
        _uid, data_list = decode_guiar_block(gb)
        if uid != -1 and _uid != uid:
            raise MixedGuiarFileException()
        achievement_list += data_list
    achievement_list = sorted(achievement_list, key=lambda x: x[0])
    gamt = dict()
    with open(gamt_path, "r", encoding="utf-8-sig") as fr:
        cfr = csv.reader(fr)
        for item in cfr:
            gamt[int(item[3])] = item[1]
    for i, t in enumerate(achievement_list):
        achievement_list[i][0] = gamt[t[0]]
    with open(save_path, "w", encoding="utf-8-sig", newline="") as fw:
        cfw = csv.writer(fw)
        cfw.writerow(export_file_header)
        for achievement in achievement_list:
            title = achievement[0]
            progress = None
            target_progress = None
            state = achievement[1]
            date = None
            amount = None
            if state:
                year, month, day = decode_date(achievement[2])
                date = f"{year}/{month}/{day}"
                amount = achievement[3]
            else:
                progress = achievement[2]
                target_progress = achievement[3]
            state = state_remark[0] if state else state_remark[1]
            row = [title, state, progress, target_progress, amount, date]
            cfw.writerow(row)
