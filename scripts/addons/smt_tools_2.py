## Blender Addon for STUDIO MeowToon
###### created: 2022-06-22
###### updated: 2022-08-18

from typing import List
from typing import Tuple

import bpy
from bpy.props import FloatProperty
from bpy.props import IntProperty
from bpy.props import StringProperty
from bpy.types import Scene

#import ptvsd
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

import global_value
import material
import armature
import comic
import tools_base
# don't import "bpy" directly

#######################################################################################################
# Information
bl_info = {
    "name": "Comic Tools 2",
    "author": "Hiroyuki Adachi from STUDIO MeowToon",
    "version": (1, 2, 0),
    "blender": (2, 80, 0),
    "description": "Addon for STUDIO MeowToon Comic",
    "category": "STUDIO MeowToon",
    "support": "TESTING",
}

#######################################################################################################
# Operator
class SMT_OT_material_setup_emily(tools_base.SMT_OT_base):
    bl_idname = "smt.material_setup_emily"
    def execute(self, context):
        scene: Scene = context.scene
        cut_count: int = scene.material_setup_sequence_param_cut_count
        material.setup_sequence_texture(material_name="emly_eyes") # FIXME:
        material.setup_sequence_param(material_name="emly_eyes", cut_count=cut_count) # FIXME:
        material.setup_mapping_node(material_name="emly_eyes") # FIXME:
        material.setup_sequence_texture(material_name="emly_mouth") # FIXME:
        material.setup_sequence_param(material_name="emly_mouth", cut_count=cut_count) # FIXME:
        material.setup_mapping_node(material_name="emly_mouth") # FIXME:
        self.report({"INFO"}, "material_setup_emily: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_material_setup_orange(tools_base.SMT_OT_base):
    bl_idname = "smt.material_setup_orange"
    def execute(self, context):
        scene: Scene = context.scene
        cut_count: int = scene.material_setup_sequence_param_cut_count
        material.setup_sequence_texture(material_name="orng_eyes") # FIXME:
        material.setup_sequence_param(material_name="orng_eyes", cut_count=cut_count) # FIXME:
        material.setup_mapping_node(material_name="orng_eyes") # FIXME:
        material.setup_sequence_texture(material_name="orng_mouth") # FIXME:
        material.setup_sequence_param(material_name="orng_mouth", cut_count=cut_count) # FIXME:
        material.setup_mapping_node(material_name="orng_mouth") # FIXME:
        self.report({"INFO"}, "material_setup_orange: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_armature_setup_emily(tools_base.SMT_OT_base):
    bl_idname = "smt.armature_setup_emily"
    def execute(self, context):
        armature.set_rotation_mode(object_name="Emily") # FIXME:
        armature.rename_bones(object_name="Emily", prefix="emly") # FIXME:
        self.report({"INFO"}, "armature_setup_emily: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_armature_setup_orange(tools_base.SMT_OT_base):
    bl_idname = "smt.armature_setup_orange"
    def execute(self, context):
        armature.set_rotation_mode(object_name="Orange") # FIXME:
        armature.rename_bones(object_name="Orange", prefix="orng") # FIXME:
        self.report({"INFO"}, "armature_setup_orange: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_comic_storyboard_set_anime(tools_base.SMT_OT_base):
    bl_idname = "smt.comic_storyboard_set_anime"
    def execute(self, context):
        scene: Scene = context.scene
        fps: float = scene.comic_storyboard_fps
        format: str = scene.comic_storyboard_format
        storyboard = comic.storyboard(format=format, fps=fps)
        storyboard.set_anime()
        global_value.cut_duration_and_start_frame_list = storyboard.get_cut_duration_and_start_frame_list()
        self.report({"INFO"}, "comic_storyboard_set_anime: completed!")
        return {"FINISHED"}

#######################################################################################################
# Panel
class SMT_PT_tools_2_menu_1(tools_base.SMT_PT_view_3d_ui_base_2):
    bl_label = "アーマチュア (armature)"
    def draw(self, context):
        layout = self.layout
        layout.operator(operator=SMT_OT_armature_setup_emily.bl_idname, text="Emily: ボーン setup")
        layout.operator(operator=SMT_OT_armature_setup_orange.bl_idname, text="Orange: ボーン setup")

#######################################################################################################
# Panel
class SMT_PT_tools_2_menu_2(tools_base.SMT_PT_view_3d_ui_base_2):
    bl_label = "マテリアル (material)"
    def draw(self, context):
        scene: Scene = context.scene
        layout = self.layout
        layout.prop(scene, "material_setup_sequence_param_cut_count", text="カット数")
        layout.operator(operator=SMT_OT_material_setup_emily.bl_idname, text="Emily: マテリアル setup")
        layout.operator(operator=SMT_OT_material_setup_orange.bl_idname, text="Orange: マテリアル setup")

#######################################################################################################
# Panel
class SMT_PT_tools_2_menu_3(tools_base.SMT_PT_view_3d_ui_base_2):
    bl_label = "コミック (comic)"
    def draw(self, context):
        scene: Scene = context.scene
        layout = self.layout
        layout.label(text="カット割り&アニメ")
        layout.prop(scene, "comic_storyboard_fps", text="FPS")
        layout.prop(scene, "comic_storyboard_format", text="")
        layout.operator(operator=SMT_OT_comic_storyboard_set_anime.bl_idname, text="カット割り&アニメ展開")

#######################################################################################################
# Property
def init_props():
    scene: Scene = bpy.types.Scene
    scene.material_setup_sequence_param_cut_count = IntProperty(
        name="cut_count",
        description="カット数を設定します",
        default=6,
        min=1,
        max=70
    )
    scene.comic_storyboard_fps = FloatProperty(
        name="fps",
        description="FPS を設定します",
        default=24.0,
        min=24.0,
        max=24.0
    )
    scene.comic_storyboard_format = StringProperty(
        name="format",
        description="format",
        default="[2][2][2][1:1][2][1:1]",
    )

def clear_props():
    scene = bpy.types.Scene
    del scene.material_setup_sequence_param_cut_count
    del scene.comic_storyboard_fps
    del scene.comic_storyboard_format

#######################################################################################################
# classes to register
classes = [
    SMT_OT_material_setup_emily,
    SMT_OT_material_setup_orange,
    SMT_OT_armature_setup_emily,
    SMT_OT_armature_setup_orange,
    SMT_OT_comic_storyboard_set_anime,
    SMT_PT_tools_2_menu_1,
    SMT_PT_tools_2_menu_2,
    SMT_PT_tools_2_menu_3,
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
