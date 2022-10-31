## Blender Addon for STUDIO MeowToon
###### created: 2022-06-01
###### updated: 2022-08-18

import bpy

#import ptvsd
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

import utils
import material
import chara
import plant
import tools_base
# don't import "bpy" directly

#######################################################################################################
# Information
bl_info = {
    "name": "Comic Tools 1",
    "author": "Hiroyuki Adachi from STUDIO MeowToon",
    "version": (1, 2, 0),
    "blender": (2, 80, 0),
    "description": "Addon for STUDIO MeowToon Comic",
    "category": "STUDIO MeowToon",
    "support": "TESTING",
}

#######################################################################################################
# Operator
class SMT_OT_utils_show_verts(tools_base.SMT_OT_base):
    bl_idname = "smt.utils_show_verts"
    def execute(self, context):
        utils.show_verts()
        self.report({"INFO"}, "utils_show_verts: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_utils_delete_empty_objects(tools_base.SMT_OT_base):
    bl_idname = "smt.utils_delete_empty_objects"
    def execute(self, context):
        utils.delete_empty_objects()
        self.report({"INFO"}, "utils_delete_empty_objects: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_utils_delete_orphan_data(tools_base.SMT_OT_base):
    bl_idname = "smt.utils_delete_orphan_data"
    def execute(self, context):
        utils.delete_orphan_data()
        self.report({"INFO"}, "utils_delete_orphan_data: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_chara_emily_setup(tools_base.SMT_OT_base):
    bl_idname = "smt.chara_emily_setup"
    def execute(self, context):
        chara.emily.set_crease()
        chara.emily.set_freestyle()
        self.report({"INFO"}, "chara_emily_setup: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_chara_orange_setup(tools_base.SMT_OT_base):
    bl_idname = "smt.chara_orange_setup"
    def execute(self, context):
        chara.orange.set_crease()
        chara.orange.set_freestyle()
        self.report({"INFO"}, "chara_orange_setup: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_plant_setup(tools_base.SMT_OT_base):
    bl_idname = "smt.plant_setup"
    def execute(self, context):
        plant.set_crease()
        plant.set_freestyle()
        self.report({"INFO"}, "plant_setup: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_material_init(tools_base.SMT_OT_base):
    bl_idname = "smt.material_init"
    def execute(self, context):
        material.init()
        self.report({"INFO"}, "material_init: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_material_flat(tools_base.SMT_OT_base):
    bl_idname = "smt.material_flat"
    def execute(self, context):
        material.flat()
        self.report({"INFO"}, "material_flat: completed!")
        return {"FINISHED"}

#######################################################################################################
# Operator
class SMT_OT_material_unflat(tools_base.SMT_OT_base):
    bl_idname = "smt.material_unflat"
    def execute(self, context):
        material.unflat()
        self.report({"INFO"}, "material_unflat: completed!")
        return {"FINISHED"}

#######################################################################################################
# Panel
class SMT_PT_tools_1_menu_1(tools_base.SMT_PT_view_3d_ui_base_1):
    bl_label = "不要削除"
    #bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout
        layout.operator(operator=SMT_OT_utils_show_verts.bl_idname, text="頂点番号表示")
        layout.operator(operator=SMT_OT_utils_delete_empty_objects.bl_idname, text="空オブジェクト削除")
        layout.operator(operator=SMT_OT_utils_delete_orphan_data.bl_idname, text="孤立したデータ削除")

#######################################################################################################
# Panel
class SMT_PT_tools_1_menu_2(tools_base.SMT_PT_view_3d_ui_base_1):
    bl_label = "クリース・フリースタイル"
    #bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout
        layout.operator(operator=SMT_OT_chara_emily_setup.bl_idname, text="Emily: setup")
        layout.operator(operator=SMT_OT_chara_orange_setup.bl_idname, text="Orange: setup")
        layout.operator(operator=SMT_OT_plant_setup.bl_idname, text="Plant: setup")

#######################################################################################################
# Panel
class SMT_PT_tools_1_menu_3(tools_base.SMT_PT_view_3d_ui_base_1):
    bl_label = "マテリアル"
    #bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout
        layout.operator(operator=SMT_OT_material_init.bl_idname, text="初期化")
        layout.operator(operator=SMT_OT_material_flat.bl_idname, text="フラット")
        layout.operator(operator=SMT_OT_material_unflat.bl_idname, text="アンフラット")

#######################################################################################################
# classes to register
classes = [
    SMT_OT_utils_show_verts,
    SMT_OT_utils_delete_empty_objects,
    SMT_OT_utils_delete_orphan_data,
    SMT_OT_material_init,
    SMT_OT_material_flat,
    SMT_OT_material_unflat,
    SMT_OT_chara_emily_setup,
    SMT_OT_chara_orange_setup,
    SMT_OT_plant_setup,
    SMT_PT_tools_1_menu_1,
    SMT_PT_tools_1_menu_2,
    SMT_PT_tools_1_menu_3,
]

#######################################################################################################
# register
def register():
    for clazz in classes:
        bpy.utils.register_class(clazz)

# unregister
def unregister():
    for clazz in classes:
        bpy.utils.unregister_class(clazz)

#######################################################################################################
# script entry
if __name__ == "__main__":
    register()
