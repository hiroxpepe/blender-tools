## Blender Python Script utility functions
###### created: 2022-05-10
###### updated: 2022-06-25

from typing import List
from typing import Dict
from typing import Tuple
import os

import bpy
from bpy.types import Action
from bpy.types import Armature
from bpy.types import BlendDataActions
from bpy.types import Bone
from bpy.types import Image
from bpy.types import Material
from bpy.types import Mesh
from bpy.types import Node
from bpy.types import NodeLink
from bpy.types import NodeSocket
from bpy.types import NodeSocketFloat
from bpy.types import NodeTree
from bpy.types import Object
from bpy.types import Pose
from bpy.types import Scene
from bpy.types import Sequence
from bpy.types import ShaderNodeBsdfPrincipled
from bpy.types import ShaderNodeTexImage
from bpy.types import VertexGroup
import bmesh
from bmesh.types import BMesh
from bmesh.types import BMVert

## [PEP:8 JP](https://pep8-ja.readthedocs.io/ja/latest/#)
## [Google style Python docstring](https://qiita.com/11ohina017/items/118b3b42b612e527dc1d)

#######################################################################################################
## 選択した頂点を表示する関数
def show_verts(coordinate: bool = False) -> None:
    """Function to display the selected vertices.

    Args:
        coordinate (bool): whether to show a vertex coordinate.
    Returns:
        None
    """
    ob: Object = bpy.context.object
    if ob.mode == "EDIT":
        print("-----") # separation
        bm: BMesh = bmesh.from_edit_mesh(ob.data)
        for bmvert in bm.verts:
            bmvert: BMVert
            if bmvert.select:
                if coordinate:
                    print(bmvert.co) # vertex coordinate
                print(bmvert.index) # vertex index
    else:
        print("object is not in edit mode.")

#######################################################################################################
## Object の情報を表示する関数
def show_object_info() -> None:
    for ob in bpy.data.objects:
        ob: Object
        print(f"{ob.name} type: {ob.type}")

#######################################################################################################
## Object のリストを取得する関数
def get_objects(type: str = "ALL") -> List[Object]:
    if type == "ALL":
        return bpy.data.objects
    else:
        return [ob for ob in bpy.data.objects if ob.type == type]

# MESH
# ARMATURE
# CAMERA
# LIGHT

#######################################################################################################
## Material の情報を表示する関数
def show_material_info() -> None:
    for material in bpy.data.materials:
        material: Material
        texture_node: ShaderNodeTexImage = bpy.data.materials[material.name].node_tree.nodes.get("Image Texture")
        if texture_node != None:
            print(f"{material.name} -- texture filepath: {texture_node.image.filepath}")
        else:
            print(f"{material.name} -- not image texture")

#######################################################################################################
## Material のリストを取得する関数
def get_materials() -> List[Material]:
    return bpy.data.materials

#######################################################################################################
## Armature の情報を表示する関数
def show_armature_info() -> None:
    for armature in bpy.data.armatures:
        armature: Armature
        print(f"{armature.name}")
        bone_list: List[Bone] = armature.bones
        for bone in bone_list:
            bone: Bone
            print(f"    {bone.name}")

#######################################################################################################
## Armature のリストを取得する関数
def get_armatures() -> List[Armature]:
    return bpy.data.armatures

#######################################################################################################
## Action のリストを取得する関数
def get_actions() -> BlendDataActions:
    return bpy.data.actions

#######################################################################################################
## OBJECT に設定する関数
def set_object_mode() -> None:
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## 状況を初期化する関数
def init(object_name: str) -> None:
    """Function to initialize the state.

    Args:
        object (string): the name of the object to edit.
    Returns:
        None
    """
    # select the object
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    # reset select
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action="DESELECT")
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Object にウエイトを設定する関数
def set_weight(object_name: str, vertex_group_name: str, verts: List[int], value: float) -> None:
    # init
    init(object_name=object_name)
    # select the object
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    # select the vertex group(bone)
    vertex_group: VertexGroup = ob.vertex_groups.get(vertex_group_name)
    ob.vertex_groups.active_index = vertex_group.index
    # select left target vertices
    bpy.ops.object.mode_set(mode="OBJECT")
    mesh: Mesh = ob.data
    for vert in verts:
        #ob.data.vertices[vert].select = True
        mesh.vertices[vert].select = True
    # set weight to vertices
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.context.scene.tool_settings.vertex_group_weight = value
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action="DESELECT")
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Object にクリースを設定する関数
def set_crease(object_name: str, verts: List[int], value: float) -> None:
    # init
    init(object_name=object_name)
    # set crease
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    mesh: Mesh = ob.data
    for vert in verts:
        #ob.data.vertices[vert].select = True
        mesh.vertices[vert].select = True
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    bpy.ops.transform.edge_crease(value=value)
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

# #######################################################################################################
# ## Object に freestyle_face を設定する関数
# #### FIXME: ※未完成: バグあり
# def set_freestyle_face(object_name: str) -> None:
#     """Function to set freestyle_face.

#     TODO: specifying edges.

#     Args:
#         object (string): the name of the object to edit.
#     Returns:
#         None
#     """
#     # init
#     init(object_name=object_name)
#     # set freestyle face
#     ob: Object = bpy.data.objects[object_name]
#     bpy.context.view_layer.objects.active = ob
#     bpy.ops.object.mode_set(mode="EDIT")
#     bpy.ops.mesh.select_all(action="SELECT")
#     bpy.ops.mesh.select_mode(type="FACE")
#     bpy.ops.mesh.mark_freestyle_face(clear=False)
#     # set OBJECT mode
#     bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Object に freestyle_face を設定する関数
#### FIXME: ※未完成: バグあり
def set_freestyle_face(object_name: str, verts: List[int] = []) -> None:
    # init
    init(object_name=object_name)
    # select the object
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    # select verts
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    # select all verts
    if len(verts) == 0:
        bpy.ops.object.mode_set(mode="EDIT", toggle=False)
        bpy.ops.mesh.select_all(action="SELECT")
    # select verts given
    else:
        mesh: Mesh = ob.data
        for vert in verts:
            mesh.vertices[vert].select = True
    # set EDIT mode and select FACE mode
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    bpy.ops.mesh.select_mode(type="FACE")
    # mark freestyle_face
    bpy.ops.mesh.mark_freestyle_face(clear=False)
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Object の局面を適用する関数
def apply_subsurf(object_name: str) -> None:
    # apply subsurf
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="subsurf")

#######################################################################################################
## Object の重複している頂点を削除する関数
def remove_double_vertices(object_name: str) -> None:
    # init
    init(object_name=object_name)
    # select the object
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    # set EDIT mode
    bpy.ops.object.mode_set(mode="EDIT")
    # select all mesh
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action="SELECT")
    # remove double vertices
    bpy.ops.mesh.remove_doubles(threshold=0.001, use_unselected=True)
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Object の頂点を指定の頂点に移動する関数
def move_vertex(object_name: str, data: Dict[int, Tuple[float, float, float]]) -> None:
    # init
    init(object_name=object_name)
    # select the object
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    # set EDIT mode
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)
    # get the mesh
    bm: BMesh = bmesh.from_edit_mesh(mesh=ob.data)
    bm.verts.ensure_lookup_table()
    # move a vert to new vert
    for key, value in data.items():
        #print(key, value)
        bmvert: BMVert = bm.verts[key]
        # Magic UV on
        bpy.context.scene.muv_texture_lock_lock = True
        bmvert.co = value
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Material のテクスチャ画像を置き換える関数
def replace_textures() -> None:
    # get path of this file
    path: str = bpy.data.filepath
    dir: str = os.path.dirname(path)
    # replace textures
    for material in bpy.data.materials:
        material: Material
        name: str = material.name
        node_tree: NodeTree = material.node_tree
        if node_tree != None:
            # Principled BSDF
            bsdf_node: ShaderNodeBsdfPrincipled = node_tree.nodes.get("Principled BSDF")
            if bsdf_node == None:
                continue
            # Alpha
            alpha_node_socket: NodeSocket = bsdf_node.inputs[18]
            for link in alpha_node_socket.links:
                link: NodeLink
                node_tree.links.remove(link=link)
            # Normal
            normal_node_socket: NodeSocket = bsdf_node.inputs[19]
            for link in normal_node_socket.links:
                link: NodeLink
                node_tree.links.remove(link=link)
            # Image Texture
            texture_node: ShaderNodeTexImage = node_tree.nodes.get("Image Texture")
            if texture_node == None:
                continue
            prefix = name.split('.')[0]
            image: Image = bpy.data.images.load(filepath=f"{dir}\\textures\\{prefix}.png")
            texture_node.image = image
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Material の現状で使用しないノードを削除する関数
def delete_unused_nodes() -> None:
    # delete unused nodes
    for material in bpy.data.materials:
        material: Material
        node_tree: NodeTree = material.node_tree
        if node_tree != None:
            for node in node_tree.nodes:
                node: Node
                # delete "Normal Map" node
                if "Normal Map" in node.name:
                    node_tree.nodes.remove(node=node)
                # delete "Image Texture.001" node
                elif "Image Texture.001" in node.name:
                    node_tree.nodes.remove(node=node)
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## 使用しないテクスチャを削除する関数
def delete_unused_images() -> None:
    # delete unused images
    for image in bpy.data.images:
        image: Image
        #if not image.users:
        if "Diffuse Texture" in image.name:
            bpy.data.images.remove(image=image)
    # set OBJECT mode
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

#######################################################################################################
## Material のシェーダーを調整する関数
def flatten_shader_or_not(value: float) -> None:
    # flatten materials
    for material in bpy.data.materials:
        material: Material
        node_tree: NodeTree = material.node_tree
        if node_tree != None:
            # get Principled BSDF
            bsdf_node: ShaderNodeBsdfPrincipled = node_tree.nodes.get("Principled BSDF")
            if bsdf_node == None:
                continue
            # set Metallic param
            metallic_node_socket: NodeSocketFloat = bsdf_node.inputs[4]
            metallic_node_socket.default_value = value
            # set Specular param
            specular_node_socket: NodeSocketFloat = bsdf_node.inputs[5]
            specular_node_socket.default_value = value

#######################################################################################################
## アクティブ Object の Bone リストを取得する関数
### MEMO: アクティブの必要がある？
def get_active_object_bones(object_name: str) -> List[Bone]:
    # select the object
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    active_object: Object = bpy.context.active_object # 必要？
    # get bones of the object
    armature: Armature = active_object.data
    bones: List[Bone] = armature.bones
    return bones

#######################################################################################################
## アクティブ Object の Pose を取得する関数
### MEMO: アクティブの必要がある？
def get_active_object_pose(object_name: str) -> Pose:
    # select the object
    ob: Object = bpy.data.objects[object_name]
    bpy.context.view_layer.objects.active = ob
    active_object: Object = bpy.context.active_object # 必要？
    # get pose of the object
    pose: Pose = active_object.pose
    return pose

#######################################################################################################
## 空の Object を削除する関数 ※再帰処理はしていない
def delete_empty_objects() -> None:
    for ob in bpy.data.objects:
        ob: Object = ob
        if ob.type == "EMPTY":
            bpy.data.objects.remove(object=ob)
    # do twice
    for ob in bpy.data.objects:
        ob: Object = ob
        if ob.type == "EMPTY":
            bpy.data.objects.remove(object=ob)

#######################################################################################################
## 孤立したデータを削除する関数
def delete_orphan_data() -> None:
    _delete_orphan_objects()
    _delete_orphan_armatures()
    _delete_orphan_meshes()
    _delete_orphan_materials()
    _delete_orphan_images()
    _delete_orphan_actions()
    # do twice
    _delete_orphan_objects()
    _delete_orphan_armatures()
    _delete_orphan_meshes()
    _delete_orphan_materials()
    _delete_orphan_images()
    _delete_orphan_actions()

def _delete_orphan_objects() -> None:
    orphan_list = [ob for ob in bpy.data.objects if ob.users == 0]
    for orphan in orphan_list:
        bpy.data.objects.remove(object=orphan)

def _delete_orphan_armatures() -> None:
    orphan_list = [armature for armature in bpy.data.armatures if armature.users == 0]
    for orphan in orphan_list:
        bpy.data.armatures.remove(armature=orphan)

def _delete_orphan_meshes() -> None:
    orphan_list = [mesh for mesh in bpy.data.meshes if mesh.users == 0]
    for orphan in orphan_list:
        bpy.data.meshes.remove(mesh=orphan)

def _delete_orphan_materials() -> None:
    orphan_list = [material for material in bpy.data.materials if material.users == 0]
    for orphan in orphan_list:
        bpy.data.materials.remove(material=orphan)

def _delete_orphan_images() -> None:
    orphan_list = [image for image in bpy.data.images if image.users == 0]
    for orphan in orphan_list:
        bpy.data.images.remove(image=orphan)

def _delete_orphan_actions() -> None:
    orphan_list = [action for action in bpy.data.actions if action.users == 0]
    for orphan in orphan_list:
        bpy.data.actions.remove(action=orphan)

#######################################################################################################
## FPS を設定する関数
def set_scene_render_fps(fps: int = 24, frame_step: int = 3) -> None:
    bpy.context.scene.render.fps = fps
    bpy.context.scene.frame_step = frame_step

#######################################################################################################
## タイムラインの終点を設定する関数
def set_scene_frame_end(frame_end: int) -> None:
     bpy.context.scene.frame_end = frame_end
     bpy.context.scene.frame_preview_end = frame_end

#######################################################################################################
## タイムラインのマーカーを全て削除する関数
def delete_scene_timeline_markers() -> None:
    bpy.context.scene.timeline_markers.clear()

#######################################################################################################
## タイムラインにマーカーを設定する関数
def set_scene_timeline_marker_to(name: str, frame: int) -> None:
    bpy.context.scene.timeline_markers.new(name=name, frame=frame)

#######################################################################################################
## シーケンサーに画像を設定する関数
def add_sequencer_image(name: str, file_path: str, channel: int, frame_start: int, frame_end: int, blend_type: str, 
    fade_duration_seconds: float = 0.0, fade_in_duration_seconds: float = 0.0, fade_out_duration_seconds: float = 0.0) -> None: #, num: int = 0
    #if num is not 0: # シフト用に番号付加
    #    name = f"{name}_{int(num)}"
    sequence: Sequence = bpy.context.scene.sequence_editor.sequences.new_image(name=name, filepath=file_path, channel=channel, frame_start=frame_start)
    sequence.frame_final_start = frame_start
    sequence.frame_final_end = frame_end # 実際には下の処理で +1 される
    sequence.frame_final_duration = frame_end - frame_start + 1 # +1 で次の開始に重なる
    sequence.blend_type = blend_type
    if fade_duration_seconds != 0.0 or fade_in_duration_seconds != 0.0 or fade_out_duration_seconds != 0.0:
        bpy.context.scene.sequence_editor.active_strip = sequence
        if fade_duration_seconds != 0.0:
            bpy.ops.sequencer.fades_add(duration_seconds=fade_duration_seconds, type="IN_OUT")
        if fade_in_duration_seconds != 0.0:
            bpy.ops.sequencer.fades_add(duration_seconds=fade_in_duration_seconds, type="IN")
        if fade_out_duration_seconds != 0.0:
            bpy.ops.sequencer.fades_add(duration_seconds=fade_out_duration_seconds, type="OUT")
    sequence.select = False # 重要

#######################################################################################################
## シーケンサーにシーンを設定する関数
def add_sequencer_scene(name: str, scene_name: str, channel: int, frame_start: int, frame_end: int, blend_type: str) -> None:
    bpy.context.scene.render.line_thickness = 2.5
    bpy.context.scene.render.film_transparent = True
    bpy.ops.scene.new(type="FULL_COPY")
    scene: Scene = bpy.data.scenes[scene_name]
    sequence: Sequence = bpy.context.scene.sequence_editor.sequences.new_scene(name=name, scene=scene, channel=channel, frame_start=frame_start)
    sequence.frame_final_start = frame_start
    sequence.frame_final_end = frame_end # 実際には下の処理で +1 される
    sequence.frame_final_duration = frame_end - frame_start + 1 # +1 で次の開始に重なる
    sequence.blend_type = blend_type

#######################################################################################################
## ファイルの存在を確認する関数
def exists_file(file_path: str) -> bool:
    is_file: bool = os.path.isfile(path=file_path)
    return is_file

#######################################################################################################
## この .blend ファイルのディレクトリを取得する関数
def get_current_dir() -> str:
    current_path: str = bpy.data.filepath
    current_dir: str = os.path.dirname(current_path)
    return current_dir

#######################################################################################################
## 現在のフレーム値を取得する関数
def get_current_frame() -> int:
    frame: int = bpy.context.scene.frame_current
    return frame

#######################################################################################################
## 引数値のフレームを選択する関数
def set_current_frame(frame: int) -> int:
    bpy.context.scene.frame_set(frame)

#######################################################################################################
## デフォルトのカメラを取得する関数
def get_default_camera() -> Object:
    camera: Object = bpy.data.objects["Camera"]
    return camera

#######################################################################################################
## start_frame からカットの end_frame を計算して返す関数
# def get_cut_end_frame(start_frame: int, cut_duration_and_start_frame_list: List[Tuple[int, int]]) -> int:
#     fps: float = 24.0 # FIXME:
#     for idx, value in enumerate(cut_duration_and_start_frame_list):
#         cut_duration: int = value[0]
#         cut_start_frame: int = value[1]
#         if start_frame == cut_start_frame:
#             return start_frame + ((cut_duration * fps) - 1)

# #######################################################################################################
# ## 補完曲線を一定に設定する関数
# def _set_curve_constant(action_name: str) -> None:
#     bpy.data.scenes["Scene"].frame_set(frame)
#     action: Action = bpy.data.actions["CameraAction"]
#     fcurves: ActionFCurves = action.fcurves
#     for fcurve in fcurves:
#         fcurve: FCurve
#         print(fcurve.data_path + " channel " + str(fcurve.array_index))
#         for keyframe in fcurve.keyframe_points:
#             keyframe: Keyframe
#             keyframe.interpolation = "CONSTANT"
