## Blender Addon for STUDIO MeowToon
###### created: 2022-06-18
###### updated: 2022-08-20

from typing import List
from typing import Tuple

import bpy
from bpy.props import EnumProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty
from bpy.types import Scene
from mathutils import Vector

#import ptvsd
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

import json
import global_value
import utils
import camera
import armature
import tools_base
# don't import "bpy" directly

#######################################################################################################
# Information
bl_info = {
    "name": "Comic Tools 4",
    "author": "Hiroyuki Adachi from STUDIO MeowToon",
    "version": (1, 2, 1),
    "blender": (2, 80, 0),
    "description": "Addon for STUDIO MeowToon Comic",
    "category": "STUDIO MeowToon",
    "support": "TESTING",
}

#######################################################################################################
# Operator
class SMT_OT_camera_come_from(tools_base.SMT_OT_base):
    bl_idname = "smt.camera_come_from"
    def _get_vector_by(self, type: str) -> Vector:
        if type == "backward":
            return (0, 0, 1)
        if type == "forward":
            return (0, 0, -1)
        if type == "left":
            return (-1, 0, 0)
        if type == "right":
            return (1, 0, 0)
        if type == "up":
            return (0, 1, 0)
        if type == "down":
            return (0, -1, 0)
        if type == "left_forward":
            return (-1, 0, -1)
        if type == "right_forward":
            return (1, 0, -1)
    def execute(self, context):
        scene: Scene = context.scene
        vector_type: str = scene.camera_come_from_vector_type
        vector: Vector = self._get_vector_by(type=vector_type)
        move_amount: float = scene.camera_come_from_move_amount
        frame_shift: int = scene.camera_come_from_frame_shift
        camera.come_from(vector=vector, move_amount=move_amount, frame_shift=frame_shift)
        self.report({"INFO"}, "camera_come_from: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_camera_zoom_to(tools_base.SMT_OT_base):
    bl_idname = "smt.camera_zoom_to"
    def _get_vector_by(self, type: str) -> Vector:
        if type == "backward":
            return (0, 0, 1)
        if type == "forward":
            return (0, 0, -1)
    def execute(self, context):
        scene: Scene = context.scene
        vector_type: str = scene.camera_zoom_to_vector_type
        vector: Vector = self._get_vector_by(type=vector_type)
        move_amount: float = scene.camera_zoom_to_move_amount
        cut_duration: int = scene.camera_zoom_to_cut_duration
        camera.zoom_to(vector=vector, move_amount=move_amount, cut_duration=cut_duration)
        self.report({"INFO"}, "camera_zoom_to: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_armature_set_breath_motion(tools_base.SMT_OT_base):
    bl_idname = "smt.armature_set_breath_motion"
    def _get_cut_duration_and_start_frame_list(self) -> List[Tuple[int, int]]: # FIXME: to utils
        if len(global_value.cut_duration_and_start_frame_list) != 0:
            return global_value.cut_duration_and_start_frame_list
        else:
            file_path: str = f"{utils.get_current_dir()}/cut_duration_and_start_frame_list.json"
            with open(file_path, "r") as fp:
                cut_duration_and_start_frame_list: List[Tuple[int, int]] = json.load(fp)
                return cut_duration_and_start_frame_list
    def execute(self, context):
        armature.set_breath_motion(cut_duration_and_start_frame_list=self._get_cut_duration_and_start_frame_list())
        self.report({"INFO"}, "armature_set_breath_motion: completed!")
        return {"FINISHED"}

#######################################################################################################
# Panel
class SMT_PT_tools_4_menu_1(tools_base.SMT_PT_view_3d_ui_base_4):
    bl_label = "拡縮効果"
    def draw(self, context):
        layout = self.layout
        scene: Scene = context.scene
        layout.label(text=f"{utils.get_current_frame()} フレーム")
        layout.prop(scene, "camera_zoom_to_vector_type", text="方向")
        layout.prop(scene, "camera_zoom_to_cut_duration", text="カット長さ")
        layout.prop(scene, "camera_zoom_to_move_amount", text="移動量")
        layout.operator(operator=SMT_OT_camera_zoom_to.bl_idname, text="挿入")

#######################################################################################################
# Panel
class SMT_PT_tools_4_menu_2(tools_base.SMT_PT_view_3d_ui_base_4):
    bl_label = "切替効果"
    def draw(self, context):
        layout = self.layout
        scene: Scene = context.scene
        layout.label(text=f"{utils.get_current_frame()} フレーム")
        layout.prop(scene, "camera_come_from_vector_type", text="方向")
        layout.prop(scene, "camera_come_from_frame_shift", text="フレーム長さ")
        layout.prop(scene, "camera_come_from_move_amount", text="移動量")
        layout.operator(operator=SMT_OT_camera_come_from.bl_idname, text="挿入")

#######################################################################################################
# Panel
class SMT_PT_tools_4_menu_3(tools_base.SMT_PT_view_3d_ui_base_4):
    bl_label = "呼吸モーション"
    def draw(self, context):
        layout = self.layout
        layout.operator(operator=SMT_OT_armature_set_breath_motion.bl_idname, text="挿入")

#######################################################################################################
# Property
def init_props():
    scene: Scene = bpy.types.Scene
    scene.camera_come_from_frame_shift = IntProperty(
        name="frame_shift",
        description="frame_shift",
        default=12,
        min=1,
        max=48
    )
    scene.camera_come_from_move_amount = FloatProperty(
        name="move_amount",
        description="move_amount",
        default=0.25,
        min=0.0,
        max=1.0
    )
    scene.camera_come_from_vector_type = EnumProperty(
        name="vector_type",
        description="vector_type",
        items=[
            ("backward", "後ろから", "(0, 0, 1)"),
            ("forward", "前から", "(0, 0, -1)"),
            ("left", "左から", "(-1, 0, 0)"),
            ("right", "右から",  "(1, 0, 0)"),
            ("up", "上から", "(0, 1, 0)"),
            ("down", "下から", "(0, -1, 0)"),
            ("left_forward", "左前から", "(-1, 0, -1)"),
            ("right_forward", "右前から", "(1, 0, -1)"),
        ],
        default="left"
    )
    scene.camera_zoom_to_cut_duration = IntProperty(
        name="cut_duration",
        description="cut_duration",
        default=2,
        min=1,
        max=8
    )
    scene.camera_zoom_to_move_amount = FloatProperty(
        name="move_amount",
        description="move_amount",
        default=0.125,
        min=0.0,
        max=1.0
    )
    scene.camera_zoom_to_vector_type = EnumProperty(
        name="vector_type",
        description="vector_type",
        items=[
            ("backward", "後へ", "(0, 0, 1)"),
            ("forward", "前へ", "(0, 0, -1)"),
        ],
        default="forward"
    )

def clear_props():
    scene = bpy.types.Scene
    del scene.camera_come_from_frame_shift
    del scene.camera_come_from_move_amount
    del scene.camera_come_from_vector_type
    del scene.camera_zoom_to_cut_duration
    del scene.camera_zoom_to_move_amount
    del scene.camera_zoom_to_vector_type

#######################################################################################################
# classes to register
classes = [
    SMT_OT_camera_come_from,
    SMT_OT_camera_zoom_to,
    SMT_OT_armature_set_breath_motion,
    SMT_PT_tools_4_menu_1,
    SMT_PT_tools_4_menu_2,
    SMT_PT_tools_4_menu_3,
]

#######################################################################################################
# register
def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)
    init_props()

# unregister
def unregister():
    clear_props()
    for clazz in classes:
        bpy.utils.unregister_class(clazz)

#######################################################################################################
# script entry
if __name__ == "__main__":
    register()
