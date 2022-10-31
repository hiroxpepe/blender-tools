## Blender Python Script エミリー用
###### created: 2022-05-10
###### updated: 2022-05-18

from typing import List
from typing import Tuple

import utils
# don't import "bpy" directly

# #######################################################################################################
# ## emly_Head                                                                                         ##
# #######################################################################################################

# #######################################################################################################
# # クリース設定

# #### あご
# utils.set_crease("emly_Head", [72,75,76], 1.0)


# #######################################################################################################
# ## emly_Body                                                                                         ##
# #######################################################################################################

# #######################################################################################################
# # 曲面適用
# utils.apply_subsurf("emly_Body")

# #######################################################################################################
# # ウエイト設定

# #### 左肩
# # 1段目: 11頂点
# verts_l1: List[int] = [1955,1957,1960,1961,2375,2377,3669,3670,3876,3877,3889]
# # 2段目: 8頂点
# verts_l2: List[int] = [407,408,409,657,1888,2371,2373,2385]
# # 3段目: 7頂点
# verts_l3: List[int] = [1887,1889,2372,3648,3872,3874,3886]

# #### 右肩
# # 1段目: 11頂点
# verts_r1: List[int] = [2646,2647,2648,2651,3051,3052,4023,4024,4230,4231,4243]
# # 2段目: 8頂点
# verts_r2: List[int] = [747,748,749,975,2585,3046,3049,3061]
# # 3段目: 7頂点
# verts_r3: List[int] = [2584,2586,3048,4002,4226,4228,4240]

# #### 左:UpperArm
# # 1段目:0
# # 2段目:0
# # 3段目:0.55
# utils.set_weight("emly_Body", "LeftUpperArm", verts_l1, 0)
# utils.set_weight("emly_Body", "LeftUpperArm", verts_l2, 0)
# utils.set_weight("emly_Body", "LeftUpperArm", verts_l3, 0.55)

# #### 右:UpperArm
# # 1段目:0
# # 2段目:0
# # 3段目:0.55
# utils.set_weight("emly_Body", "RightUpperArm", verts_r1, 0)
# utils.set_weight("emly_Body", "RightUpperArm", verts_r2, 0)
# utils.set_weight("emly_Body", "RightUpperArm", verts_r3, 0.55)

# #### 左:Shoulder
# # 1段目:0.55～1 ※場合による
# # 2段目:※保留
# utils.set_weight("emly_Body", "LeftShoulder", verts_l1, 1)

# #### 右:Shoulder
# # 1段目:0.55～1 ※場合による
# # 2段目:※保留
# utils.set_weight("emly_Body", "RightShoulder", verts_r1, 1)


#######################################################################################################
## emly_Bustier_v1_Inner ※長袖ビスチェインナー                                                      ##
#######################################################################################################

#######################################################################################################
# 曲面適用
utils.apply_subsurf("emly_Bustier_v1_Inner")

#######################################################################################################
# ウエイト設定

#### 左肩
# 1段目: 11頂点
verts_l1: List[int] = [425,464,466,468,470,472,1162,1163,1164,1165,1174]
# 2段目: 8頂点
verts_l2: List[int] = [12,13,14,46,388,446,449,463]
# 3段目: 7頂点
verts_l3: List[int] = [387,389,447,1131,1150,1152,1159]

#### 右肩
# 1段目: 11頂点
verts_r1: List[int] = [805,841,843,846,848,850,1346,1347,1348,1349,1358]
# 2段目: 8頂点
verts_r2: List[int] = [211,212,213,237,772,823,827,842]
# 3段目: 7頂点
verts_r3: List[int] = [771,773,825,1315,1334,1336,1343]

#### 左:UpperArm
# 1段目:0
# 2段目:0
# 3段目:5.5
utils.set_weight("emly_Bustier_v1_Inner", "LeftUpperArm", verts_l1, 0)
utils.set_weight("emly_Bustier_v1_Inner", "LeftUpperArm", verts_l2, 0)
utils.set_weight("emly_Bustier_v1_Inner", "LeftUpperArm", verts_l3, 0.55)

#### 右:UpperArm
# 1段目:0
# 2段目:0
# 3段目:5.5
utils.set_weight("emly_Bustier_v1_Inner", "RightUpperArm", verts_r1, 0)
utils.set_weight("emly_Bustier_v1_Inner", "RightUpperArm", verts_r2, 0)
utils.set_weight("emly_Bustier_v1_Inner", "RightUpperArm", verts_r3, 0.55)

#### 左:Shoulder
# 1段目:0.55※保留
# 2段目:※保留
#utils.set_weight("emly_Bustier_v1_Inner", "LeftShoulder", verts_l1, 0.55)

#### 右:Shoulder
# 1段目:0.55※保留
# 2段目:※保留
#utils.set_weight("emly_Bustier_v1_Inner", "RightShoulder", verts_r1, 0.55)


#######################################################################################################
## emly_Bustier_v2_Inner ※半袖ビスチェインナー                                                      ##
#######################################################################################################

#######################################################################################################
# 曲面適用 
utils.apply_subsurf("emly_Bustier_v2_Inner")

#######################################################################################################
# ウエイト設定

#### 左肩
# 1段目: 11頂点
verts_l1: List[int] = [327,366,368,370,372,374,860,861,862,863,864]
# 2段目: 8頂点
verts_l2: List[int] = [12,13,14,46,290,348,351,365]
# 3段目: 7頂点
verts_l3: List[int] = [289,291,349,829,848,850,857]

#### 右肩
# 1段目: 11頂点
verts_r1: List[int] = [549,585,587,590,592,594,967,968,969,970,971]
# 2段目: 8頂点
verts_r2: List[int] = [138,139,140,164,516,567,571,586]
# 3段目: 7頂点
verts_r3: List[int] = [515,517,569,936,955,957,964]

#### 左:UpperArm
# 1段目:0
# 2段目:0
# 3段目:5.5
utils.set_weight("emly_Bustier_v2_Inner", "LeftUpperArm", verts_l1, 0)
utils.set_weight("emly_Bustier_v2_Inner", "LeftUpperArm", verts_l2, 0)
utils.set_weight("emly_Bustier_v2_Inner", "LeftUpperArm", verts_l3, 0.55)

#### 右:UpperArm
# 1段目:0
# 2段目:0
# 3段目:5.5
utils.set_weight("emly_Bustier_v2_Inner", "RightUpperArm", verts_r1, 0)
utils.set_weight("emly_Bustier_v2_Inner", "RightUpperArm", verts_r2, 0)
utils.set_weight("emly_Bustier_v2_Inner", "RightUpperArm", verts_r3, 0.55)

#### 左:Shoulder
# 1段目:0.55※保留
# 2段目:※保留
#utils.set_weight("emly_Bustier_v2_Inner", "LeftShoulder", verts_l1, 0.55)

#### 右:Shoulder
# 1段目:0.55※保留
# 2段目:※保留
#utils.set_weight("emly_Bustier_v2_Inner", "RightShoulder", verts_r1, 0.55)


#######################################################################################################
# エミリー:emly_JK1v2_Blouse:曲面適用 ※長袖ブラウス
utils.apply_subsurf("emly_JK1v2_Blouse")

#######################################################################################################
## emly_JK1v2_Blouse                                                                                 ##
#######################################################################################################

#######################################################################################################
# ウエイト設定

#### 左肩
# 1段目: 11頂点
verts_l1: List[int] = [555,579,693,697,701,705,1231,1233,1235,1237,1255]
# 2段目: 8頂点
verts_l2: List[int] = [73,74,75,118,486,561,564,578]
# 3段目: 7頂点
verts_l3: List[int] = [485,487,562,1126,1154,1156,1166]

#### 右肩
# 1段目: 11頂点
verts_r1: List[int] = [651,674,689,695,699,703,1230,1232,1234,1236,1254]
# 2段目: 8頂点
verts_r2: List[int] = [128,129,130,162,589,656,660,675]
# 3段目: 7頂点
verts_r3: List[int] = [588,590,658,1172,1200,1202,1212]

#### 左:UpperArm
# 1段目:0
# 2段目:0
# 3段目:5.5
utils.set_weight("emly_JK1v2_Blouse", "LeftUpperArm", verts_l1, 0)
utils.set_weight("emly_JK1v2_Blouse", "LeftUpperArm", verts_l2, 0)
utils.set_weight("emly_JK1v2_Blouse", "LeftUpperArm", verts_l3, 0.55)

#### 右:UpperArm
# 1段目:0
# 2段目:0
# 3段目:5.5
utils.set_weight("emly_JK1v2_Blouse", "RightUpperArm", verts_r1, 0)
utils.set_weight("emly_JK1v2_Blouse", "RightUpperArm", verts_r2, 0)
utils.set_weight("emly_JK1v2_Blouse", "RightUpperArm", verts_r3, 0.55)

#### 左:Shoulder
# 1段目:0.55～1 ※場合による
utils.set_weight("emly_JK1v2_Blouse", "RightShoulder", verts_l1, 1)

#### 右:Shoulder
# 1段目:0.55～1 ※場合による
utils.set_weight("emly_JK1v2_Blouse", "RightShoulder", verts_r1, 1)


#######################################################################################################
## emly_Blouse ※旧半袖ブラウス                                                                      ##
#######################################################################################################

#######################################################################################################
# クリース設定

#### 左襟
utils.set_crease("emly_Blouse", [205,206,208], 1.0)

#### 右襟
utils.set_crease("emly_Blouse", [203,204,207], 1.0)

#######################################################################################################
# 曲面適用 
utils.apply_subsurf("emly_Blouse")

#######################################################################################################
# ウエイト設定

#### 左肩
# 1段目: 11頂点
verts_l1: List[int] = [409,433,547,551,555,559,801,803,805,807,825]
# 2段目: 8頂点
verts_l2: List[int] = [73,74,75,118,340,415,418,432]
# 3段目: 7頂点
verts_l3: List[int] = [339,341,416,696,724,726,736]

#### 右肩
# 1段目: 11頂点
verts_r1: List[int] = [505,528,543,549,553,557,800,802,804,806,824]
# 2段目: 8頂点
verts_r2: List[int] = [128,129,130,162,443,510,514,529]
# 3段目: 7頂点
verts_r3: List[int] = [442,444,512,742,770,772,782]

#### 左:UpperArm
# 1段目:0
# 2段目:0.25
# 3段目:0.55
utils.set_weight("emly_Blouse", "LeftUpperArm", verts_l1, 0)
utils.set_weight("emly_Blouse", "LeftUpperArm", verts_l2, 0.25)
utils.set_weight("emly_Blouse", "LeftUpperArm", verts_l3, 0.55)

#### 右:UpperArm
# 1段目:0
# 2段目:0.25
# 3段目:0.55
utils.set_weight("emly_Blouse", "RightUpperArm", verts_r1, 0)
utils.set_weight("emly_Blouse", "RightUpperArm", verts_r2, 0.25)
utils.set_weight("emly_Blouse", "RightUpperArm", verts_r3, 0.55)

#### 左:Shoulder
# 1段目:0.55～1 ※場合による
#utils.set_weight("emly_Blouse", "RightShoulder", verts_l1, 1)

#### 右:Shoulder
# 1段目:0.55～1 ※場合による
#utils.set_weight("emly_Blouse", "RightShoulder", verts_r1, 1)


#######################################################################################################
## emly_Skirt                                                                                        ##
#######################################################################################################

#######################################################################################################
# 曲面適用 
utils.apply_subsurf("emly_Skirt")

#######################################################################################################
# ウエイト設定

#### 上端前
skirt_verts: List[int] = [48,62,181,183,185,186,219,220,282,283,300,301]

#### SkirtBase
utils.set_weight("emly_Skirt", "SkirtBase", skirt_verts, 0.15)
