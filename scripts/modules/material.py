## Blender Python Script マテリアル用
###### created: 2022-05-10
###### updated: 2022-06-21

from typing import List
from typing import Tuple
import os
import random

import bpy # FIXME:
# don't import "bpy" directly
from bpy.types import ActionFCurves
from bpy.types import FCurve
from bpy.types import Image
from bpy.types import Keyframe
from bpy.types import Material
from bpy.types import NodeLinks
from bpy.types import NodeSocketFloat
from bpy.types import NodeTree
from bpy.types import ShaderNodeMapping
from bpy.types import ShaderNodeTexCoord
from bpy.types import ShaderNodeTexImage

import utils

#######################################################################################################
def init():
    utils.replace_textures()
    utils.delete_unused_nodes()
    utils.delete_unused_images()

#######################################################################################################
def flat():
    utils.flatten_shader_or_not(0)

#######################################################################################################
def unflat():
    utils.flatten_shader_or_not(1)

#######################################################################################################
## キーフレームアニメーションするテクスチャ画像を置き換える関数
def setup_sequence_texture(material_name: str):
    # テクスチャー画像は .blend 同一ディレクトリの textures ディレクトリに存在する前提
    current_path = bpy.data.filepath
    current_dir = os.path.dirname(current_path)
    image: Image = bpy.data.images.load(filepath=f"{current_dir}\\textures\\{material_name}_0.png") # bpy.data.images["orng_eyes_0.png"]
    texture_node: ShaderNodeTexImage = bpy.data.materials[material_name].node_tree.nodes["Image Texture"] # bpy.data.materials["orng_eyes"].node_tree.nodes["Image Texture"] # type:'TEX_IMAGE'
    texture_node.image = image

#######################################################################################################
## マテリアルのテクスチャに連番画像を設定する関数
def setup_sequence_param(material_name: str, cut_count: int):
    bpy.data.images[f"{material_name}_0.png"].source = "SEQUENCE"
    texture_node: ShaderNodeTexImage = bpy.data.materials[material_name].node_tree.nodes["Image Texture"] # bpy.data.materials["orng_eyes"].node_tree.nodes["Image Texture"] # type:'TEX_IMAGE'
    texture_node.image_user.frame_duration = cut_count # 4カットなら4 ※基数0: デフォルト画像が 0
    texture_node.image_user.frame_start = 1 # スタートフレーム
    texture_node.image_user.frame_offset = 0 # 0 でOK
    texture_node.image_user.use_auto_refresh = True

#######################################################################################################
## マテリアルにUVアニメーション用の マッピング Node 設定をする関数
def setup_mapping_node(material_name: str) -> None:
    material: Material = bpy.data.materials[material_name]
    # get and create nodes
    texture_node: ShaderNodeTexImage = material.node_tree.nodes["Image Texture"]
    coord_node: ShaderNodeTexCoord = material.node_tree.nodes.new("ShaderNodeTexCoord")
    coord_node.location = (-700, 300)
    mapping_node: ShaderNodeMapping = material.node_tree.nodes.new("ShaderNodeMapping")
    mapping_node.location = (-500, 300)
    # link nodes
    node_tree: NodeTree = material.node_tree
    node_links: NodeLinks = node_tree.links
    node_links.new(input=coord_node.outputs[2], output=mapping_node.inputs[0])
    node_links.new(input=mapping_node.outputs[0], output=texture_node.inputs[0])
    # setup nodes
    mapping_node.vector_type = "TEXTURE"
    node_socket: NodeSocketFloat = mapping_node.inputs[1]
    node_socket.default_value[1] = 1

#######################################################################################################
## アニメーションするマテリアルのテクスチャ Node にキーフレームを設定する機能 ※連番画像
## フレーム1からカット数分の画像オフセット値をする関数
def _set_init_frame_offset(material_name: str, cut_count: int) -> None:
    # フレーム1からカット数分の画像オフセット値をする
    #   frame 1: 1 を表示
    #   frame 2: 2 をまだ表示させたくなので   -1 して 1を表示
    #   frame 3: 3 をまだ表示させたくなので   -2 して 1を表示
    #   frame 4: 4 をまだ表示させたくなので   -3 して 1を表示
    #   frame n: n をまだ表示させたくなので -(n-1) して 1を表示
    #       ※ 初回2秒カットとして 48フレームまではオフセット表域として使用可能
    #       ※ 最後の frame_offset 値は -(カット数 - 1)
    texture_node: ShaderNodeTexImage = bpy.data.materials[material_name].node_tree.nodes["Image Texture"]
    texture_node.image_user.frame_offset = 0
    texture_node.image_user.keyframe_insert(data_path="frame_offset", frame=0)
    for idx in range(cut_count):
        cut_num = idx + 1
        texture_node.image_user.frame_offset = -idx
        texture_node.image_user.keyframe_insert(data_path="frame_offset", frame=cut_num)
    #texture_node.image_user.frame_offset = 0
    #texture_node.image_user.keyframe_insert("frame_offset", frame=1)
    #texture_node.image_user.frame_offset = -1
    #texture_node.image_user.keyframe_insert("frame_offset", frame=2)
    #texture_node.image_user.frame_offset = -2
    #texture_node.image_user.keyframe_insert("frame_offset", frame=3)
    #texture_node.image_user.frame_offset = -3
    #texture_node.image_user.keyframe_insert("frame_offset", frame=4)

#######################################################################################################
## 1フレームに設定した1画像以降のn画像をカット切り替えのタイミングでオフセット設定する関数
def _set_cut_frame_offset(material_name: str, cut_count: int, cut_start_frame_list: List[int]) -> None:
    # 1フレームに設定した1画像以降のn画像をカット切り替えのタイミングでオフセット設定する
    #   ※ 最後の frame_offset 値 -(カット数 - 1) から + n++ した値を frame_offset 値とする
    cut_remain_count = cut_count - 1
    for idx in range(cut_remain_count):
        cut_num = idx + 1
        texture_node: ShaderNodeTexImage = bpy.data.materials[material_name].node_tree.nodes["Image Texture"]
        texture_node.image_user.frame_offset = -cut_remain_count + cut_num
        texture_node.image_user.keyframe_insert(data_path="frame_offset", frame=cut_start_frame_list[cut_num]) # 2カット目から
    #texture_node.image_user.frame_offset = -2
    #texture_node.image_user.keyframe_insert("frame_offset", frame=25)
    #texture_node.image_user.frame_offset = -1
    #texture_node.image_user.keyframe_insert("frame_offset", frame=49)
    #texture_node.image_user.frame_offset = 0
    #texture_node.image_user.keyframe_insert("frame_offset", frame=73)

#######################################################################################################
## まばたきを設定する関数
def _set_blink(material_name: str, cut_duration_and_start_frame_list: List[Tuple[int, int]]) -> None:
    # init blink
    _set_init_blink(material_name=material_name)
    # set blink for cuts
    for idx, value in enumerate(cut_duration_and_start_frame_list):
        cut_duration: int = value[0]
        cut_start_frame: int = value[1]
        _set_cut_blink(material_name=material_name, cut_duration=cut_duration, cut_start_frame=cut_start_frame) 
    _set_curve_constant(material_name=material_name)

#######################################################################################################
## 口パクを設定する関数
def _set_lipsync(material_name: str, cut_duration_and_start_frame_list: List[Tuple[int, int]]) -> None:
    # init lipsync
    _set_init_lipsync(material_name=material_name)
    # set lipsync for cuts
    for idx, value in enumerate(cut_duration_and_start_frame_list):
        cut_duration: int = value[0]
        cut_start_frame: int = value[1]
        _set_cut_lipsync(material_name=material_name, cut_duration=cut_duration, cut_start_frame=cut_start_frame) 
    _set_curve_constant(material_name=material_name)

#######################################################################################################
## まばたきの初期状態を設定する関数
def _set_init_blink(material_name: str) -> None:
    node_socket: NodeSocketFloat = bpy.data.materials[material_name].node_tree.nodes["Mapping"].inputs[1]
    node_socket.default_value[1] = 1
    node_socket.keyframe_insert(data_path="default_value", frame=0)

#######################################################################################################
## 口パクの初期状態を設定する関数
def _set_init_lipsync(material_name: str) -> None:
    node_socket: NodeSocketFloat = bpy.data.materials[material_name].node_tree.nodes["Mapping"].inputs[1]
    node_socket.default_value[1] = 1
    node_socket.keyframe_insert(data_path="default_value", frame=0)

#######################################################################################################
## カット毎のまばたきを設定する関数
def _set_cut_blink(material_name: str, cut_duration: int, cut_start_frame: int) -> None:
    init_offset = 12 # カット切り替え後のオフセット値
    count = round(cut_duration / 2) # まばたきは2秒に1回
    #print(f"blink count: {count}")
    for idx in range(count):
        if idx == 0: # 初期オフセット値
            offset1 = init_offset
        else:
            offset1 = 0
        offset2 = random.randint(-8, 12) # オフセットのランダム値
        #print(f"blink offset2: {offset2}")
        next = int((cut_duration * 24) * idx / count) # FIXME: 24fps に依存している
        #print(f"blink next: {next}")
        _set_one_blink(material_name=material_name, start_frame=(cut_start_frame + next + offset1 + offset2))

#######################################################################################################
## カット毎の口パクを設定する関数
def _set_cut_lipsync(material_name: str, cut_duration: int, cut_start_frame: int) -> None:
    init_offset = 6 # カット切り替え後のオフセット値
    count = round(cut_duration / 2) # 口パクは2秒に1回
    #print(f"lipsync count: {count}")
    for idx in range(count):
        if idx == 0: # 初期オフセット値
            offset1 = init_offset
        else:
            offset1 = 0
        offset2 = random.randint(-8, 12) # オフセットのランダム値
        #print(f"lipsync offset2: {offset2}")
        next = int((cut_duration * 24) * idx / count) # FIXME: 24fps に依存している
        #print(f"lipsync next: {next}")
        _set_one_lipsync(material_name=material_name, start_frame=(cut_start_frame + next + offset1 + offset2))

#######################################################################################################
## 1回のまばたきを設定する関数
def _set_one_blink(material_name: str, start_frame: int) -> None:
    close_value: float = 0.25
    open_value: float = 1.00
    duration: int = 5 # 目をつむるフレーム数
    node_socket: NodeSocketFloat = bpy.data.materials[material_name].node_tree.nodes["Mapping"].inputs[1]
    node_socket.default_value[1] = close_value
    node_socket.keyframe_insert(data_path="default_value", frame=start_frame)
    node_socket.default_value[1] = open_value
    node_socket.keyframe_insert(data_path="default_value", frame=(start_frame + duration))

#######################################################################################################
## 1回の口パクを設定する関数
def _set_one_lipsync(material_name: str, start_frame: int) -> None:
    close_value: float = 0.25
    open_value: float = 1.00
    duration: int = 5 # 口を閉じるフレーム数
    twice_interval: int = 12 # 口パクは連続二回
    node_socket: NodeSocketFloat = bpy.data.materials[material_name].node_tree.nodes["Mapping"].inputs[1]
    node_socket.default_value[1] = close_value
    node_socket.keyframe_insert(data_path="default_value", frame=start_frame)
    node_socket.default_value[1] = open_value
    node_socket.keyframe_insert(data_path="default_value", frame=(start_frame + duration))
    node_socket.default_value[1] = close_value
    node_socket.keyframe_insert(data_path="default_value", frame=(start_frame + twice_interval))
    node_socket.default_value[1] = open_value
    node_socket.keyframe_insert(data_path="default_value", frame=(start_frame + duration + twice_interval))

#######################################################################################################
## マテリアルの補完曲線を一定に設定する関数
def _set_curve_constant(material_name: str) -> None:
    # set interpolation curve of the keyframe
    node_tree: NodeTree = bpy.data.materials[material_name].node_tree
    fcurves: ActionFCurves = node_tree.animation_data.action.fcurves
    for fcurve in fcurves:
        fcurve: FCurve
        for keyframe in fcurve.keyframe_points:
            keyframe: Keyframe
            keyframe.interpolation = "CONSTANT"

#######################################################################################################
## 表情のアニメを設定する関数
def set_face_anime(cut_duration_and_start_frame_list: List[Tuple[int, int]]) -> None:
    material_name_list: List[str] = ["emly_eyes", "emly_mouth", "orng_eyes", "orng_mouth"] # FIXME:
    cut_count: int = len(cut_duration_and_start_frame_list)
    cut_start_frame_list: List[int] = list(map(lambda x: x[1], cut_duration_and_start_frame_list))
    for material_name in material_name_list:
        material_name: str
        ## フレーム1からカット数分の画像オフセット値をする
        _set_init_frame_offset(material_name=material_name, cut_count=cut_count)
        ## フレーム1に設定した1画像以降のn画像をカット切り替えのタイミングでオフセット設定する関数
        _set_cut_frame_offset(material_name=material_name, cut_count=cut_count, cut_start_frame_list=cut_start_frame_list)
        ## 目パチ・口パクを設定する
        if "eyes" in material_name:
            _set_blink(material_name=material_name, cut_duration_and_start_frame_list=cut_duration_and_start_frame_list)
        if "mouth" in material_name:
            _set_lipsync(material_name=material_name, cut_duration_and_start_frame_list=cut_duration_and_start_frame_list)
        ## マテリアルの補完曲線を一定に設定する
        _set_curve_constant(material_name=material_name)
