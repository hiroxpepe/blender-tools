## Blender Addon Base for STUDIO MeowToon
###### created: 2022-06-16
###### updated: 2022-08-18

import bpy
from bpy.props import *
from bpy.types import Operator, Panel

# don't import "bpy" directly

#######################################################################################################
# Base Operator
class SMT_OT_base(Operator):
    bl_label = ""

#######################################################################################################
# Base Panel
class SMT_PT_view_3d_ui_base_1(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "★初期化"

#######################################################################################################
# Base Panel
class SMT_PT_view_3d_ui_base_2(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "★コンテ展開"

#######################################################################################################
# Base Panel
class SMT_PT_view_3d_ui_base_3(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "★カメラアングル"

#######################################################################################################
# Base Panel
class SMT_PT_view_3d_ui_base_4(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "★カメラ効果"
