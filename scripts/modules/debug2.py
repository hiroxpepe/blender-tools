#import ptvsd
#ptvsd.enable_attach()
#ptvsd.wait_for_attach()

from typing import List
from typing import Tuple

import bpy
from bpy.types import Object

import importlib
import utils
import camera
import armature
importlib.reload(utils)
importlib.reload(camera)
importlib.reload(armature)

from mathutils import Matrix, Vector

#_debug_fps: float = 24.0

#storyboard = comic.storyboard(format=f"[4][4][4][4]", fps=_debug_fps)
#storyboard.execute()

#backward_vector: Vector = (0, 0, 1)
#forward_vector: Vector = (0, 0, -1)
#left_vector: Vector = (-1, 0, 0)
#right_vector: Vector = (1, 0, 0)
#up_vector: Vector = (0, 1, 0)
#down_vector: Vector = (0, -1, 0)
#left_forward_vector: Vector = (-1, 0, -1)
#right_forward_vector: Vector = (1, 0, -1)

# X軸: 左右
# Y軸: 前後
# Z軸: 上下

#frame: int = utils.get_current_frame()
#print(f"frame: {frame}")
#camera.come_from1(vector=left_vector, amount=0.5, frame=frame)
#camera.come_from(vector=left_forward_vector, move_amount=0.25, frame_shift=12)
#camera.zoom_to(vector=forward_vector, move_amount=0.25, cut_duration=4)

#verts: List[int] = [81, 82, 83, 101,106]
#utils.set_freestyle_face(object_name="emly_Head", verts=verts)

print("completed!")
