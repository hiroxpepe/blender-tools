## Blender Python Script for Character
###### created: 2022-06-21
###### updated: 2022-06-21

import emily
import orange

# FIXME: Orangeのフリースタイルを修正してクリース・フリースタイルを統合する

#######################################################################################################
## クリースを設定する関数
def set_crease() -> None:
    emily.set_crease()
    #orange.set_crease()

#######################################################################################################
## フリースタイルを設定する関数
def set_freestyle() -> None:
    #emily.set_freestyle()
    orange.set_freestyle()
