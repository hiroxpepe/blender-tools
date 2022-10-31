import ptvsd
ptvsd.enable_attach()
ptvsd.wait_for_attach()

import importlib
import bpy
import utils
import material
import armature
import camera
import emily
import orange
import hibiscus
import leaves
import comic

importlib.reload(utils)
importlib.reload(material)
importlib.reload(armature)
importlib.reload(camera)
importlib.reload(emily)
importlib.reload(orange)
importlib.reload(hibiscus)
importlib.reload(leaves)
importlib.reload(comic)

# debug code here
print("completed!")
