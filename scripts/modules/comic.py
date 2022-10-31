## Blender Python Script for Comic
###### created: 2022-06-01
###### updated: 2022-06-27

from typing import Dict
from typing import List
from typing import Tuple
from enum import Enum

import json
import utils
import material
#import armature
import pose
import plant
# don't import "bpy" directly
import bpy

_comic_texture_source_dir: str = "//textures\\"

#######################################################################################################
## Enum

class position(Enum):
    """
    + 位置を表現する列挙体
        + 以下の9ポジションで十分事足りる
        + TODO: ※必要ないかも
    """
    left_top = 1
    center_top = 2
    right_top = 3
    left_mid = 4
    center_mid = 5
    right_mid = 6
    left_bottom = 7
    center_bottom = 8
    right_bottom = 9

class channel(Enum):
    """
    + レイヤーの重ね位置を表現する列挙体
    """
    overlay = 15 # 質感
    effect = 14 # 効果 # MEMO: オノマトペ？
    script = 13 # テキスト
    talk = 12 # セリフ
    balloon = 11 # 吹き出し
    foreground = 10 # 前景
    background = 9 # 背景
    scene = 8 # シーン

#######################################################################################################
## Class
class timeline():
    """
    + タイムラインを表現するクラス
        + 自分の FPS は何なのか知っている
        + n秒のフレーム数値は何であるか提供できる
    """
    ###################################################################################################
    # Constructor

    def __init__(self, fps: float = 24.0):
        self._fps: float = fps

    ###################################################################################################
    # private Methods [verb]

    def _get_start_frame_after(self, seconds: int) -> int:
        return int((self._fps * (seconds)) + 1)

    ###################################################################################################
    # public Methods [verb]

    # FPS を取得します
    def get_fps(self) -> float:
        return self._fps

    # n秒の開始フレーム数値を取得します
    def get_start_frame_of(self, seconds: int) -> int:
        return int(self._get_start_frame_after(seconds - 1))

    # n秒の最終フレーム数値を取得します
    def get_end_frame_of(self, seconds: int) -> int:
        return int(self._fps * (seconds))

#######################################################################################################
### Test Class

import unittest

class test_timeline(unittest.TestCase):

    _fps: float = 24.0

    ###################################################################################################
    def test_get_start_frame_after0(self):
        obj = timeline(fps=self._fps)
        expected = 1 #※0秒後というのは1秒の開始
        actual = obj._get_start_frame_after(0)
        self.assertEqual(expected, actual)

    def test_get_start_frame_after1(self):
        obj = timeline(fps=self._fps)
        expected = 25 #※1秒後というのは2秒の開始
        actual = obj._get_start_frame_after(1)
        self.assertEqual(expected, actual)

    def test_get_start_frame_after2(self):
        obj = timeline(fps=self._fps)
        expected = 49 #※2秒後というのは3秒の開始
        actual = obj._get_start_frame_after(2)
        self.assertEqual(expected, actual)

    def test_get_start_frame_after3(self):
        obj = timeline(fps=self._fps)
        expected = 73 #※3秒後というのは4秒の開始
        actual = obj._get_start_frame_after(3)
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_start_frame_of3(self):
        obj = timeline(fps=self._fps)
        expected = 49 #3秒の開始フレーム
        actual = obj.get_start_frame_of(3)
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_end_frame_of3(self):
        obj = timeline(fps=self._fps)
        expected = 72 #3秒の最終フレーム
        actual = obj.get_end_frame_of(3)
        self.assertEqual(expected, actual)

"""
※そもそも1秒後というのは2秒の開始である
1秒:  1 ～ 24 
2秒: 25 ～ 48 (24 + 24)
3秒: 49 ～ 72
4秒: 73 ～ 96 ((24 *    3)    + 1 ～ 24 * 4)
n秒:          ((24 * (n - 1)) + 1 ～ 24 * n)
"""

#######################################################################################################
## Class
class base_page():
    """
    + ページを表現するクラス
        + 自分が何番目のページか知っている
        + 自分が何秒のページか知っている
        + 自分の開始フレームを知っている
        + 自分の終了フレームを知っている
    """
    ###################################################################################################
    # Constructor

    def __init__(self, num: int, duration: int, start_frame: int, end_frame: int):
        self._num: int = num
        self._duration: int = duration
        self._start_frame: int = start_frame
        self._end_frame: int = end_frame

    ###################################################################################################
    # public Methods [verb]

    def get_start_frame(self) -> int:
        return self._start_frame

    def get_end_frame(self) -> int:
        return self._end_frame

#######################################################################################################
## Class
class fade_page(base_page):
    """
    + セリフを表現するクラス
        + フェードイン・アウトの数値を適切に提供できる
    """
    ###################################################################################################
    # Constructor

    def __init__(self, num: int, duration: int, start_frame: int, end_frame: int):
        super().__init__(num=num, duration=duration, start_frame=start_frame, end_frame=end_frame)
        self._default_cut_fade_in_duration: float = 0.50 # カット始まりフェードイン数値
        self._default_page_fade_in_duration: float = 0.25 # ページ始まりフェードイン数値
        self._default_page_fade_out_duration: float = 0.25 # ページ終わりフェードアウト数値
        self._default_cut_fade_out_duration: float = 0.50 # カット終わりフェードアウト数値

    ###################################################################################################
    # private Methods [verb]

    def _get_fade_in_duration(self, page_count: int) -> float:
        if self._num == 1:
            return self._default_cut_fade_in_duration
        else:
            return self._default_page_fade_in_duration

    def _get_fade_out_duration(self, page_count: int) -> float:
        if self._num == page_count:
            return self._default_cut_fade_out_duration
        else:
            return self._default_page_fade_out_duration

    ###################################################################################################
    # public Methods [verb]

    def get_fade_in_duration(self, page_count: int) -> float: # 1枚パターンもこの値に依存
        return self._get_fade_in_duration(page_count=page_count)

    def get_fade_out_duration(self, page_count: int) -> float: # 1枚パターンもこの値に依存
        return self._get_fade_out_duration(page_count=page_count)

#######################################################################################################
### Test Class

class test_page(unittest.TestCase):
    # ページ 4枚 page_count=4 パターン
    # num: 1 - in: 0.50 out: 0.25
    # num: 2 - in: 0.25 out: 0.25
    # num: 3 - in: 0.25 out: 0.25
    # num: 4 - in: 0.25 out: 0.50

    _cut_fade_duration: float = 0.50
    _page_fade_duration: float = 0.25

    ###################################################################################################
    def test_get_fade_in_duration1(self):
        obj = fade_page(num=1, duration=999, start_frame=999, end_frame=999)
        expected = self._cut_fade_duration
        actual = obj.get_fade_in_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_fade_out_duration1(self):
        obj = fade_page(num=1, duration=999, start_frame=999, end_frame=999)
        expected = self._page_fade_duration
        actual = obj.get_fade_out_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_fade_in_duration2(self):
        obj = fade_page(num=2, duration=999, start_frame=999, end_frame=999)
        expected = self._page_fade_duration
        actual = obj.get_fade_in_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_fade_out_duration2(self):
        obj = fade_page(num=2, duration=999, start_frame=999, end_frame=999)
        expected = self._page_fade_duration
        actual = obj.get_fade_out_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_fade_in_duration3(self):
        obj = fade_page(num=3, duration=999, start_frame=999, end_frame=999)
        expected = self._page_fade_duration
        actual = obj.get_fade_in_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_fade_out_duration3(self):
        obj = fade_page(num=3, duration=999, start_frame=999, end_frame=999)
        expected = self._page_fade_duration
        actual = obj.get_fade_out_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_fade_in_duration4(self):
        obj = fade_page(num=4, duration=999, start_frame=999, end_frame=999)
        expected = self._page_fade_duration
        actual = obj.get_fade_in_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_fade_out_duration4(self):
        obj = fade_page(num=4, duration=999, start_frame=999, end_frame=999)
        expected = self._cut_fade_duration
        actual = obj.get_fade_out_duration(page_count=4) # カットの開始
        self.assertEqual(expected, actual)

#######################################################################################################
## Class
class layer():
    """
    + レイヤー表現するクラス
        + 画像ファイルを想定
            + 自分の重ね位置(チャンネル)を知っている
            + 自分のカットNoを知っている
                + ※通しレイヤーはカットNo:0
            + 画像が存在するディレクトリを知っている
            + 画像の名前リストを知っている
            + 画像の合成方法を知っている
            + フェードイン・アウトの数値を知っている
    """
    # ここにクラス変数を書くと継承クラスで共有となるのでNG
    ###################################################################################################
    # Constructor

    def __init__(self, cut_num: int, page_list: List[fade_page] = []):
        self._channel: int = 0
        self._cut_num: int = cut_num
        self._source_dir: str = _comic_texture_source_dir
        self._source_file_name_list: List[str] = []
        self._blend_type: str = ""
        self._fade_in_and_out_duration: float = 0.00
        self._page_list: List[fade_page] = page_list
        self._use_page: bool = False
        self._can_move: bool = False # 移動するレイヤーかどうか

    ###################################################################################################
    # public Methods [verb]

    def set_image(self, name: str, frame_tuple: Tuple[int, int]) -> None:
        current_dir = utils.get_current_dir()
        if self._use_page == True: # ページ適用レイヤーパターン ※トークレイヤーの1枚パターンもここ
            page_count: int = len(self._source_file_name_list)
            for idx, source_file_name in enumerate(self._source_file_name_list):
                idx: int
                source_file_name: str
                one_page: fade_page = self._page_list[idx] # page 取得
                # check existence of the file
                file_path: str = f"{current_dir}{self._source_dir}{source_file_name}"
                exists_file: bool = utils.exists_file(file_path)
                if exists_file == True:
                    # add image strip to the sequencer
                    utils.add_sequencer_image(
                        name=f"{name}_{str(self._cut_num)}", 
                        file_path=f"{self._source_dir}{source_file_name}", 
                        channel=self._channel, 
                        frame_start=one_page.get_start_frame(),
                        frame_end=one_page.get_end_frame(),
                        blend_type=self._blend_type,
                        fade_in_duration_seconds=one_page.get_fade_in_duration(page_count=page_count),
                        fade_out_duration_seconds=one_page.get_fade_out_duration(page_count=page_count)
                    )
        elif self._can_move == True: # 移動するレイヤー
            # check existence of the file
            file_path: str = f"{current_dir}{self._source_dir}{self._source_file_name_list[0]}"
            exists_file: bool = utils.exists_file(file_path)
            if exists_file == True:
                # カットの長さを分割してシフトして設定する
                frame_start: int = frame_tuple[0]
                frame_end: int = frame_tuple[1]
                cut_duration: int = frame_end - frame_start
                dev_frame: int = 3 # 3フレで分割する
                stop_frame: int = 24 * 1 # 効果は1秒 FIXME: 24FRS に依存
                count: int = int((cut_duration + 1) / dev_frame)
                for idx in range(count):
                    num: int = idx + 1
                    # add image strip to the sequencer
                    one_name: str = f"{name}_{str(self._cut_num)}_{str(num)}"
                    utils.add_sequencer_image(
                        name=one_name, 
                        file_path=f"{self._source_dir}{self._source_file_name_list[0]}", 
                        channel=self._channel, 
                        frame_start=frame_start + (dev_frame * idx), 
                        frame_end=frame_start + (dev_frame * idx) + (dev_frame - 1), 
                        blend_type=self._blend_type,
                        fade_duration_seconds=self._fade_in_and_out_duration
                    )
                    if idx < 8: # 1秒までは
                        move_px: int = 168 #192 # 3フレで移動するピクセル
                        move_px = move_px * (8 - idx) # 徐々に小さく
                        #if move_px > 1080: # 1080px より大きい値は修正
                        #    move_px = 1080
                        bpy.context.scene.sequence_editor.sequences_all[one_name].use_translation = True
                        bpy.context.scene.sequence_editor.sequences_all[one_name].transform.offset_x = move_px
        else: # ページ適用外レイヤーパターン
            # check existence of the file
            file_path: str = f"{current_dir}{self._source_dir}{self._source_file_name_list[0]}"
            exists_file: bool = utils.exists_file(file_path)
            if exists_file == True:
                # add image strip to the sequencer
                utils.add_sequencer_image(
                    name=f"{name}_{str(self._cut_num)}", 
                    file_path=f"{self._source_dir}{self._source_file_name_list[0]}", 
                    channel=self._channel, 
                    frame_start=frame_tuple[0], 
                    frame_end=frame_tuple[1], 
                    blend_type=self._blend_type,
                    fade_duration_seconds=self._fade_in_and_out_duration
                )

#######################################################################################################
## Class
class overlay(layer):
    """
    + オーバーレイを表現するクラス
    """
    ###################################################################################################
    # Constructor

    def __init__(self, cut_num: int, page_list: List[fade_page] = []):
        super().__init__(cut_num=cut_num, page_list=page_list)
        self._channel = channel.overlay.value
        self._source_file_name_list.append(f"overlay_0.png")
        self._blend_type = "OVERLAY"

#######################################################################################################
## Class
class script(layer):
    """
    + script(文字)を表現するクラス
    """
    ###################################################################################################
    # Constructor

    def __init__(self, cut_num: int, page_list: List[fade_page] = []):
        super().__init__(cut_num=cut_num, page_list=page_list)
        self._channel = channel.script.value
        self._blend_type = "ALPHA_OVER"
        self._source_file_name_list.append(f"script_{str(cut_num)}.png") # 1枚を移動する
        self._can_move: bool = True

#######################################################################################################
## Class
class talk(layer):
    """
    + セリフ(会話)を表現するクラス
    + TODO: セリフ画像の自動生成
    """
    ###################################################################################################
    # Constructor

    def __init__(self, cut_num: int, page_list: List[fade_page] = []):
        super().__init__(cut_num=cut_num, page_list=page_list)
        self._channel = channel.talk.value
        self._blend_type = "ALPHA_OVER"
        self._use_page: bool = True
        self._fade_in_and_out_duration = 0.50
        if len(page_list) == 1: # セリフ1枚パターン
            self._source_file_name_list.append(f"talk_{str(cut_num)}.png")
        else:
            for idx, value in enumerate(page_list): # 複数セリフパターン
                page_num = idx + 1
                self._source_file_name_list.append(f"talk_{str(cut_num)}-{str(page_num)}.png")

#######################################################################################################
## Class
class balloon(layer):
    """
    + 吹き出しを表現するクラス
    """
    ###################################################################################################
    # Constructor

    def __init__(self, cut_num: int, page_list: List[fade_page] = []):
        super().__init__(cut_num=cut_num, page_list=page_list)
        self._channel = channel.balloon.value
        self._blend_type = "ALPHA_OVER"
        self._source_file_name_list.append(f"balloon_{str(cut_num)}.png")
        self._fade_in_and_out_duration = 0.25

#######################################################################################################
## Class
class foreground(layer):
    """
    + 前景を表現するクラス
    """
    ###################################################################################################
    # Constructor

    def __init__(self, cut_num: int, page_list: List[fade_page] = []):
        super().__init__(cut_num=cut_num, page_list=page_list)
        self._channel = channel.foreground.value
        self._blend_type = "ALPHA_OVER"
        self._source_file_name_list.append(f"foreground_{str(cut_num)}.png")

#######################################################################################################
## Class
class background(layer):
    """
    + 背景を表現するクラス
    """
    ###################################################################################################
    # Constructor

    def __init__(self, cut_num: int, page_list: List[fade_page] = []):
        super().__init__(cut_num=cut_num, page_list=page_list)
        self._channel = channel.background.value
        self._blend_type = "ALPHA_UNDER"
        self._source_file_name_list.append(f"background_{str(cut_num)}.png")

#######################################################################################################
## Class
class cut():
    """
    + カットを表現するクラス
        + 自分が何番目のカットか知っている
        + 自分が何秒のカットか知っている
        + 自分の開始フレームを知っている
        + 自分の終了フレームを知っている
        + カットごとのレイヤーを生成する
        + ページ(セリフ)情報のリストを持つ
    """
    ###################################################################################################
    # Constructor

    def __init__(self, num: int, duration: int, start_frame: int, end_frame: int, page_list: List[fade_page]):
        self._num: int = num
        self._duration: int = duration
        self._start_frame: int = start_frame
        self._end_frame: int = end_frame
        self._page_list: List[fade_page] = page_list
        if __name__ != "__main__":
            self._init_overlay_layer()
            self._init_script_layer()
            self._init_talk_layer()
            self._init_balloon_layer()
            self._init_foreground_layer()
            self._init_background_layer()

    ###################################################################################################
    # private Methods [verb]

    def _init_overlay_layer(self) -> None:
        new_overlay: overlay = overlay(cut_num=self._num, page_list=self._page_list)
        new_overlay.set_image(name="overlay", frame_tuple=(self._start_frame, self._end_frame))

    def _init_script_layer(self) -> None:
        new_talk: script = script(cut_num=self._num, page_list=self._page_list)
        new_talk.set_image(name="script", frame_tuple=(self._start_frame, self._end_frame))

    def _init_talk_layer(self) -> None:
        new_talk: talk = talk(cut_num=self._num, page_list=self._page_list)
        new_talk.set_image(name="talk", frame_tuple=(self._start_frame, self._end_frame))

    def _init_balloon_layer(self) -> None:
        new_balloon: balloon = balloon(cut_num=self._num, page_list=self._page_list)
        new_balloon.set_image(name="balloon", frame_tuple=(self._start_frame, self._end_frame))

    def _init_foreground_layer(self) -> None:
        new_foreground: foreground = foreground(cut_num=self._num, page_list=self._page_list)
        new_foreground.set_image(name="foreground", frame_tuple=(self._start_frame, self._end_frame))

    def _init_background_layer(self) -> None:
        new_background: background = background(cut_num=self._num, page_list=self._page_list)
        new_background.set_image(name="background", frame_tuple=(self._start_frame, self._end_frame))

    ###################################################################################################
    # public Methods [verb]

    def get_start_frame(self) -> int:
        return self._start_frame

    def get_end_frame(self) -> int:
        return self._end_frame

#######################################################################################################
## Class
class storyboard():
    """
    + 絵コンテを表現するクラス
        + 何枚のカットが存在するか知っている
        + それぞれのカットが何秒か知っている
        + TODO: 個別のカットにアクセスする手段を提供する
        + 通しのレイヤーを生成する
    """
    ###################################################################################################
    # Constructor

    def __init__(self, format: str, fps: float = 24.0):
        # setup
        self._timeline: timeline = timeline(fps)
        self._format: str = format.strip()
        self._count: int = self.get_count()
        self._cutPageDict: Dict[int, Tuple[int, ...]] = {}
        self._cutDict: Dict[int, cut] = {}
        # create cut objects
        cut_duration_count: int = 1 # count of duration
        for cut_idx, cut_duration in enumerate(map(int, self._get_cut_list())):
            cut_num = cut_idx + 1
            # セリフページを生成
            page_tuple: Tuple[int, ...] = self._cutPageDict[cut_idx]
            page_list: List[fade_page] = []
            page_duration_count: int = cut_duration_count # cut_duration_count はこのカットの開始秒
            for page_idx, page_duration in enumerate(page_tuple):
                page_num: int = page_idx + 1
                page_start_frame: int = self._timeline.get_start_frame_of(page_duration_count)
                page_end_frame: int = self._timeline.get_end_frame_of(page_duration_count + (page_duration - 1))
                new_page = fade_page(num=page_num, duration=page_duration, start_frame=page_start_frame, end_frame=page_end_frame)
                page_list.append(new_page)
                page_duration_count += page_duration
            # カットを生成
            cut_start_frame: int = self._timeline.get_start_frame_of(cut_duration_count)
            cut_end_frame: int = self._timeline.get_end_frame_of(cut_duration_count + (cut_duration - 1))
            new_cut: cut = cut(
                num=cut_num, duration=cut_duration, start_frame=cut_start_frame, end_frame=cut_end_frame, 
                page_list=page_list
            ) # この時点でカットのレイヤーが生成・実行される
            self._cutDict[cut_idx] = new_cut
            cut_duration_count += cut_duration # 秒数経過カウンタ

    ###################################################################################################
    # private Methods [verb]

    # カットごとのページ秒数タプルのディクトを取得します
    def _get_cut_page_dict(self) -> Dict[int, Tuple[int, ...]]:
        result: Dict[Tuple[int,Tuple]] = {}
        tmp1: str = self._format.replace("[", "")
        tmp2: List[str] = tmp1.split("]")
        tmp3: List[str] = [value for value in tmp2 if value != '']
        for idx, part in enumerate(tmp3):
            part: str
            splitted_part: Tuple[int, ...] = ()
            if ":" in part:
                splitted_part = tuple(map(int, part.split(":"))) # ":" で分割
            else:
                splitted_part = (int(part),) # 末尾にカンマが必要
            result[idx] = splitted_part
        self._cutPageDict = result
        return result

    # カットごとの秒数リストを取得します
    def _get_cut_list(self) -> List[int]:
        result: List[int] = []
        tuple_list: Dict[Tuple[int, ...]] = self._get_cut_page_dict()
        for tuple in tuple_list.values():
            tuple: Tuple[int, ...]
            cut_duration: int = sum(tuple) # カットごとに合計する
            result.append(cut_duration)
        return result

    # カットごとの開始フレームリストを取得します
    def _get_cut_start_frame_list(self) -> List[int]:
        cut_start_frame_list: List[int] = []
        cut_list: List[int] = self._get_cut_list()
        cut_duration_count = 1 # count of duration
        for cut_duration in cut_list:
            cut_duration: int
            cut_start_frame_list.append(self._timeline.get_start_frame_of(cut_duration_count))
            cut_duration_count += cut_duration
        return cut_start_frame_list

    # カットごとの秒数と開始フレームリストを取得します
    def _get_cut_duration_and_start_frame_list(self) -> List[Tuple[int, int]]:
        cut_duration_and_start_frame_list: List[Tuple[int, int]] = []
        cut_list: List[int] = self._get_cut_list()
        cut_start_frame_list: List[int] = self._get_cut_start_frame_list()
        for idx in range(self.get_count()):
            idx: int
            cut_duration: int = cut_list[idx]
            cut_start_frame: int = cut_start_frame_list[idx]
            cut_duration_and_start_frame_list.append((cut_duration, cut_start_frame))
        return cut_duration_and_start_frame_list

    ###################################################################################################
    # public Methods [verb]

    # フォーマット文字列を取得します ※FIXME: 必要？
    def get_format(self) -> str:
        return self._format

    # カットの数を取得します
    def get_count(self) -> int:
        return len(self._get_cut_list())

    # 全体の尺(秒)を取得します
    def get_total(self) -> int:
        return sum(map(int, self._get_cut_list()))

    # 引数値(1base)の cut オブジェクトを取得します
    def get_cut_of(self, index: int) -> cut:
        return 0 # FIXME:

    # カットごとの秒数と開始フレームリストを取得します
    def get_cut_duration_and_start_frame_list(self) -> List[Tuple[int, int]]:
        return self._get_cut_duration_and_start_frame_list()

    # 処理を実行します
    def set_anime(self) -> bool:
        """
        + 基本的に最後にこれを呼んで自動セットアップが完了する状態
        + 注意：正しい素材や Blender のファイルがないと失敗します！
        """
        # FPS を設定
        fps: int = self._timeline.get_fps()
        utils.set_scene_render_fps(fps)
        # 尺(秒)の取得とフレームエンドを設定
        total: int = self.get_total()
        frame_end: int = self._timeline.get_end_frame_of(total)
        utils.set_scene_frame_end(frame_end)
        # フレーム0にデフォルトポーズを挿入する
        #pose.keyframe_insert(cut_num=0, frame=0)
        # タイムラインにマーカーを削除する
        utils.delete_scene_timeline_markers()
        # カットごとに
        for idx, cut in self._cutDict.items():
            cut_num: int = idx + 1 # cut number
            frame: int = cut.get_start_frame() # start frame
            # タイムラインにマーカーを設定する
            utils.set_scene_timeline_marker_to(f"cut-{str(cut_num)}", frame)
            # ポーズを挿入する
            pose.keyframe_insert(cut_num=(cut_num - 1), frame=(frame - 1)) # 1フレ前に前のカットのポーズ
            pose.keyframe_insert(cut_num=cut_num, frame=frame) # このカットのポーズ
        # ループ補間の為最終フレーム+1の位置にカット1のポーズを挿入する
        pose.keyframe_insert(cut_num=cut_num, frame=(frame_end))
        pose.keyframe_insert(cut_num=1, frame=(frame_end + 1))
        ## ポーズ補間の固定
        #armature.set_curve_constant()
        # カットごとの表情テクスチャのオフセットと目パチ・口パクを設定
        cut_duration_and_start_frame_list: List[Tuple[int, int]] = self._get_cut_duration_and_start_frame_list()
        material.set_face_anime(cut_duration_and_start_frame_list=cut_duration_and_start_frame_list)
        ## キャラの呼吸アニメを設定
        #armature.set_breath_motion(cut_duration_and_start_frame_list=cut_duration_and_start_frame_list)
        # 草木の動き
        plant.set_motion(frame_end=frame_end)
        # シーンを設定する
        utils.add_sequencer_scene(
            name="scene", scene_name="Scene", channel=channel.scene.value, 
            frame_start=1, frame_end=frame_end, blend_type="CROSS"
        )
        # フレーム1を選択
        utils.set_current_frame(frame=1)
        # カット情報シリアライズ
        file_path: str = f"{utils.get_current_dir()}/cut_duration_and_start_frame_list.json"
        with open(file_path, "w") as fp:
            json.dump(cut_duration_and_start_frame_list, fp, indent=4)
        # set OBJECT mode
        utils.set_object_mode()
        print("completed!")
        return True

#######################################################################################################
### Test Class

class test_storyboard(unittest.TestCase):

    ###################################################################################################
    def test_get_format(self):
        obj = storyboard(format="[2][4][4][2][4][4]")
        expected = "[2][4][4][2][4][4]"
        actual = obj.get_format()
        self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_count1(self):
        obj = storyboard(format="[2][4][4][2][4][4]")
        expected = 6
        actual = obj.get_count()
        self.assertEqual(expected, actual)

    def test_get_count2(self):
        obj = storyboard(format="[2][4][4][2][4][4][2][4][4]")
        expected = 9
        actual = obj.get_count()
        self.assertEqual(expected, actual)

    def test_get_count3(self):
        obj = storyboard(format="")
        expected = 0
        actual = obj.get_count()
        self.assertEqual(expected, actual)

    # def test_get_count4(self):
    #     obj = storyboard(format="[4][1:3][4][2:2][1:1:1:1]")
    #     expected = 5
    #     actual = obj.get_count()
    #     self.assertEqual(expected, actual)

    ###################################################################################################
    def test_get_total1(self):
        obj = storyboard("[2][4][2][4]")
        expected = 12
        actual = obj.get_total()
        self.assertEqual(expected, actual)

    def test_get_total2(self):
        obj = storyboard("[4]")
        expected = 4
        actual = obj.get_total()
        self.assertEqual(expected, actual)

    def test_get_total2(self):
        obj = storyboard("[2][4][4][2][4][4][2][4][4]")
        expected = 30
        actual = obj.get_total()
        self.assertEqual(expected, actual)

    ###################################################################################################
    def xx_test_execute(self):
        obj = storyboard("[2][4][4][2][4][4]")
        expected = True
        actual = obj.set_anime()
        self.assertEqual(expected, actual)

#######################################################################################################
### execute unit tests

if __name__ == "__main__":
    unittest.main()
