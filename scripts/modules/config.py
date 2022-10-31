## Blender Python Script 設定用
###### created: 2022-06-22
###### updated: 2022-06-28

from typing import List
from typing import Tuple

# https://lab.syncer.jp/Tool/JSON-Viewer/

#######################################################################################################
## Class
class config():
    """
    + 設定を表現するクラス
        + 設定の内容を提供できる
    """

    ###################################################################################################
    # Constructor

    def __init__(self):
        return

    ###################################################################################################
    # public Methods [verb]

    # 設定を JSON ファイルに保存します
    def save() -> bool:
        return

    # JSON ファイルから設定を読み込みます
    def load() -> bool:
        return

    # ※TBA を取得します
    def get_object_name_and_prefix_list(self) -> List[Tuple[str, str]]:
        return self._fps # object_name="Orange", prefix="orng"
