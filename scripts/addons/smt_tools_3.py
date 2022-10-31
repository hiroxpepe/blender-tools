## Blender Addon for STUDIO MeowToon
###### created: 2022-06-16
###### updated: 2022-08-19

#import ptvsd
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

import bpy
from bpy.props import BoolProperty
from bpy.props import IntProperty
from bpy.types import Scene

#import ptvsd
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

import utils
import camera
import object
import plant
import emily
import orange
import tools_base
# don't import "bpy" directly

#######################################################################################################
# Information
bl_info = {
    "name": "Comic Tools 3",
    "author": "Hiroyuki Adachi from STUDIO MeowToon",
    "version": (1, 2, 1),
    "blender": (2, 80, 0),
    "description": "Addon for STUDIO MeowToon Comic",
    "category": "STUDIO MeowToon",
    "support": "TESTING",
}

#######################################################################################################
# Operator
class SMT_OT_emily_hide_from(tools_base.SMT_OT_base):
    bl_idname = "smt.emily_hide_from"
    def execute(self, context):
        scene: Scene = context.scene
        start_frame: int = utils.get_current_frame()
        value: bool = scene.emily_hide_from_value
        emily.hide_from(start_frame=start_frame, value=value)
        self.report({"INFO"}, "emily_hide_from: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_orange_hide_from(tools_base.SMT_OT_base):
    bl_idname = "smt.orange_hide_from"
    def execute(self, context):
        scene: Scene = context.scene
        start_frame: int = utils.get_current_frame()
        value: bool = scene.orange_hide_from_value
        orange.hide_from(start_frame=start_frame, value=value)
        self.report({"INFO"}, "orange_hide_from: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_plant_hide_from(tools_base.SMT_OT_base):
    bl_idname = "smt.plant_hide_from"
    def execute(self, context):
        scene: Scene = context.scene
        start_frame: int = utils.get_current_frame()
        value: bool = scene.plant_hide_from_value
        plant.hide_from(start_frame=start_frame, value=value)
        self.report({"INFO"}, "plant_hide_from: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_object_hide_from(tools_base.SMT_OT_base):
    bl_idname = "smt.object_hide_from"
    def execute(self, context):
        scene: Scene = context.scene
        start_frame: int = utils.get_current_frame()
        value: bool = scene.object_hide_from_value
        object.hide_from(start_frame=start_frame, value=value)
        self.report({"INFO"}, "object_hide_from: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_emily_select_bone_hips(tools_base.SMT_OT_base):
    bl_idname = "smt.emily_select_bone_hips"
    def execute(self, context):
        emily.select_bone_hips()
        self.report({"INFO"}, "emily_select_bone_hips: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_emily_keyframe_insert(tools_base.SMT_OT_base):
    bl_idname = "smt.emily_keyframe_insert"
    def execute(self, context):
        scene: Scene = context.scene
        cut_duration: int = scene.chara_keyframe_insert_cut_duration
        emily.keyframe_insert_hips(cut_duration=cut_duration)
        self.report({"INFO"}, "emily_keyframe_insert: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_orange_select_bone_hips(tools_base.SMT_OT_base):
    bl_idname = "smt.orange_select_bone_hips"
    def execute(self, context):
        orange.select_bone_hips()
        self.report({"INFO"}, "orange_select_bone_hips: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_orange_keyframe_insert(tools_base.SMT_OT_base):
    bl_idname = "smt.orange_keyframe_insert"
    def execute(self, context):
        scene: Scene = context.scene
        cut_duration: int = scene.chara_keyframe_insert_cut_duration
        orange.keyframe_insert_hips(cut_duration=cut_duration)
        self.report({"INFO"}, "orange_keyframe_insert: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_camera_keyframe_insert(tools_base.SMT_OT_base):
    bl_idname = "smt.camera_keyframe_insert"
    def execute(self, context):
        camera.keyframe_insert()
        self.report({"INFO"}, "camera_keyframe_insert: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_camera_keyframe_delete(tools_base.SMT_OT_base):
    bl_idname = "smt.camera_keyframe_delete"
    def execute(self, context):
        camera.keyframe_delete()
        self.report({"INFO"}, "camera_keyframe_delete: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_camera_set_curve_constant(tools_base.SMT_OT_base):
    bl_idname = "smt.camera_set_curve_constant"
    def execute(self, context):
        camera.set_curve_constant()
        self.report({"INFO"}, "camera_set_curve_constant: completed!")
        return {"FINISHED"}

#######################################################################################################
# Panel
class SMT_PT_tools_3_menu_1(tools_base.SMT_PT_view_3d_ui_base_3):
    bl_label = "Emily(エミリー)"
    bl_options = {"DEFAULT_CLOSED"}
    def draw(self, context):
        layout = self.layout
        scene: Scene = context.scene
        layout.label(text=f"{utils.get_current_frame()} フレームからミュート")
        layout.prop(scene, "emily_hide_from_value", text="有効")
        layout.operator(operator=SMT_OT_emily_hide_from.bl_idname, text="設定")

#######################################################################################################
# Panel
class SMT_PT_tools_3_menu_2(tools_base.SMT_PT_view_3d_ui_base_3):
    bl_label = "Orange(オレンジ)"
    bl_options = {"DEFAULT_CLOSED"}
    def draw(self, context):
        layout = self.layout
        scene: Scene = context.scene
        layout.label(text=f"{utils.get_current_frame()} フレームからミュート")
        layout.prop(scene, "orange_hide_from_value", text="有効")
        layout.operator(operator=SMT_OT_orange_hide_from.bl_idname, text="設定")

#######################################################################################################
# Panel
class SMT_PT_tools_3_menu_3(tools_base.SMT_PT_view_3d_ui_base_3):
    bl_label = "Plant(植物)"
    bl_options = {"DEFAULT_CLOSED"}
    def draw(self, context):
        layout = self.layout
        scene: Scene = context.scene
        layout.label(text=f"{utils.get_current_frame()} フレームからミュート")
        layout.prop(scene, "plant_hide_from_value", text="有効")
        layout.operator(operator=SMT_OT_plant_hide_from.bl_idname, text="設定")

#######################################################################################################
# Panel
class SMT_PT_tools_3_menu_4(tools_base.SMT_PT_view_3d_ui_base_3):
    bl_label = "Object(物体)"
    bl_options = {"DEFAULT_CLOSED"}
    def draw(self, context):
        layout = self.layout
        scene: Scene = context.scene
        layout.label(text=f"{utils.get_current_frame()} フレームからミュート")
        layout.prop(scene, "object_hide_from_value", text="有効")
        layout.operator(operator=SMT_OT_object_hide_from.bl_idname, text="設定")

#######################################################################################################
# Panel
class SMT_PT_tools_3_menu_5(tools_base.SMT_PT_view_3d_ui_base_3):
    bl_label = "カメラ -> Scene"
    def draw(self, context):
        layout = self.layout
        layout.operator(operator=SMT_OT_camera_keyframe_insert.bl_idname, text=f"{utils.get_current_frame()} にキーフレーム挿入")
        layout.operator(operator=SMT_OT_camera_keyframe_delete.bl_idname, text=f"{utils.get_current_frame()} のキーフレーム削除")
        layout.operator(operator=SMT_OT_camera_set_curve_constant.bl_idname, text="全ての補間カーブ：一定")

#######################################################################################################
# Panel
class SMT_PT_tools_3_menu_6(tools_base.SMT_PT_view_3d_ui_base_3):
    bl_label = "キャラ -> Scene"
    def draw(self, context):
        layout = self.layout
        scene: Scene = context.scene
        layout.prop(scene, "chara_keyframe_insert_cut_duration", text="カット長さ")
        layout.operator(operator=SMT_OT_emily_select_bone_hips.bl_idname, text="Emily Hips 選択")
        layout.operator(operator=SMT_OT_emily_keyframe_insert.bl_idname, text=f"{utils.get_current_frame()} に Emily Hips キーフレーム挿入")
        layout.operator(operator=SMT_OT_orange_select_bone_hips.bl_idname, text="Orange Hips 選択")
        layout.operator(operator=SMT_OT_orange_keyframe_insert.bl_idname, text=f"{utils.get_current_frame()} に Orange Hips キーフレーム挿入")

#######################################################################################################
# Property
def init_props():
    scene: Scene = bpy.types.Scene
    scene.emily_hide_from_value = BoolProperty(
        name="value",
        description="value",
        default=True
    )
    scene.orange_hide_from_value = BoolProperty(
        name="value",
        description="value",
        default=True
    )
    scene.object_hide_from_value = BoolProperty(
        name="value",
        description="value",
        default=True
    )
    scene.plant_hide_from_value = BoolProperty(
        name="value",
        description="value",
        default=True
    )
    scene.chara_keyframe_insert_cut_duration = IntProperty(
        name="chara_keyframe_insert_cut_duration",
        description="chara_keyframe_insert_cut_duration",
        default=2,
        min=1,
        max=4
    )

def clear_props():
    scene = bpy.types.Scene
    del scene.emily_hide_from_value
    del scene.orange_hide_from_value
    del scene.object_hide_from_value
    del scene.plant_hide_from_value
    del scene.chara_keyframe_insert_cut_duration

#######################################################################################################
# classes to register
classes = [
    SMT_OT_emily_hide_from,
    SMT_OT_orange_hide_from,
    SMT_OT_object_hide_from,
    SMT_OT_plant_hide_from,
    SMT_OT_emily_select_bone_hips,
    SMT_OT_emily_keyframe_insert,
    SMT_OT_orange_select_bone_hips,
    SMT_OT_orange_keyframe_insert,
    SMT_OT_camera_keyframe_insert,
    SMT_OT_camera_keyframe_delete,
    SMT_OT_camera_set_curve_constant,
    SMT_PT_tools_3_menu_1,
    SMT_PT_tools_3_menu_2,
    SMT_PT_tools_3_menu_3,
    SMT_PT_tools_3_menu_4,
    SMT_PT_tools_3_menu_5,
    SMT_PT_tools_3_menu_6,
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
