# [画像処理](https://python-climbing.com/image_resize_python/)

from multiprocessing.dummy import Array
import os
import glob
import shutil
from PIL import Image

#######################################################################################################
# アスペクト比を固定して幅が指定した値になるようリサイズする
def _scale_to_width(image: Image, width: int) -> Image:  
    height = round(image.height * width / image.width)
    return image.resize((width, height), resample=Image.NEAREST)

#######################################################################################################
# 画像を 1024 サイズに拡縮して出力する
def resize_png_to_1024(target_path: str) -> None:
    files: Array = glob.glob(f"{target_path}\\*.png")
    for file in files:
        file: str
        # copy the file as original
        dir_name: str = os.path.dirname(file)
        basename_without_extension: str = os.path.splitext(os.path.basename(file))[0]
        file_path_without_extension, extension = os.path.splitext(file)
        copy_dir_name: str = f"{dir_name}\\orig"
        copy_path: str = f"{dir_name}\\orig\\{basename_without_extension}{extension}"
        os.makedirs(name=copy_dir_name, exist_ok=True)
        shutil.copyfile(src=file, dst=copy_path)
        # resize the image
        image: Image = Image.open(file)
        resized_image: Image = _scale_to_width(image=image, width=1024)
        # save resized the image
        resized_image.save(file)

#######################################################################################################
# 実行
#target_path = "G:\\マイドライブ\\for_me\\documents\\05_X_プロジェクト\\05_業務ツール系\\Blender_Tools\\scripts\\modules"
#target_path = "G:\\マイドライブ\\for_me\\3dmodel\\2022-05-22_ねこくんとエミリー_赤水玉ビキニ_ビーチにて\\comic\\textures"
target_path = "D:\\STUDIO-MeowToon\\Archives\\Works\\01_Drawings\\2022-05-22_ねこくんとエミリー_赤水玉ビキニ_ビーチにて\\comic\\textures"
resize_png_to_1024(target_path)
print("completed!")
