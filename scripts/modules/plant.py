## Blender Python Script for Plant
###### created: 2022-06-11
###### updated: 2022-07-02

from typing import List
from typing import Tuple

import hibiscus
import leaves
import palm_tree
import sunflower
import morning_glory

#######################################################################################################
## クリースを設定する関数
def set_crease() -> None:
     hibiscus.set_crease_leafs()
     leaves.set_crease_leafs()
     sunflower.set_crease_leafs()
     morning_glory.set_crease_leafs()

#######################################################################################################
## Freestyle面を設定する関数
def set_freestyle() -> None:
    morning_glory.set_freestyle_petals()

#######################################################################################################
## ボーンに動きをつける関数
def set_motion(frame_end: int) -> None:
     hibiscus.set_motion(frame_end=frame_end)
     palm_tree.set_motion(frame_end=frame_end)
     sunflower.set_motion(frame_end=frame_end)
     # FIXME: ベースクラスを継承させてTypeのコレクションをループして実行する

#######################################################################################################
## 引数のフレーム値でレンダーで非表示にする関数
def hide_from(start_frame: int, value: bool = True) -> None:
    hibiscus.hide_from(start_frame=start_frame, value=value)
    palm_tree.hide_from(start_frame=start_frame, value=value)
    sunflower.hide_from(start_frame=start_frame, value=value)
    # FIXME: ベースクラスを継承させてTypeのコレクションをループして実行する
