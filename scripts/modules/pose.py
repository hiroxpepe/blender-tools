## Blender Python Script ポーズ用
###### created: 2022-06-05
###### updated: 2022-06-21

from typing import List
import os
import sys
import importlib

import utils
# don't import "bpy" directly

_pose_py_source_dir: str = "//poses\\"

#######################################################################################################
## 外部のポーズスクリプトを動的に実行する関数
def keyframe_insert(cut_num: int, frame: int) -> None:
    poses_dir: str = f"{utils.get_current_dir()}{_pose_py_source_dir}" # ポーズスクリプトを格納するディレクトリ
    #print(f"poses_dir: {poses_dir}")
    sys.path.append(poses_dir) # 実行パスに追加
    poses_files: List[str] = os.listdir(poses_dir) # ポーズスクリプトのリスト取得
    for pose_file in poses_files:
        pose_file: str
        if pose_file.endswith(f"_{str(cut_num)}_pose.py"): # *_cut_n_pose.py ファイルを処理
            #print(f"pose_file: {pose_file}")
            module_name: str = os.path.splitext(os.path.basename(pose_file))[0] # 拡張子なしがモジュール名
            #print(f"module_name: {module_name}")
            module = importlib.import_module(module_name) # モジュールインポート
            module.keyframe_insert(frame) # 処理実行
            # TODO: Base クラスを設定してインテリセンスに反応させる
