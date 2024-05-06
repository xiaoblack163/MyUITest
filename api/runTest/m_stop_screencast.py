from os.path import sep
from pathlib import Path
from shutil import rmtree
from time import sleep, time



def stop(self, video_name=None):
    """停止录屏
    :param video_name: 视频文件名，为None时以当前时间名命
    :return: 文件路径
    """
    if video_name and not video_name.endswith('webm'):
        video_name = f'{video_name}.webm'
    name = f'{time()}.webm' if not video_name else video_name
    path = f'{self._path}{sep}{name}'

    self._enable = False
    while self._running:
        sleep(.1)

    if not str(self._path).isascii():
        raise TypeError('转换成视频仅支持英文路径和文件名。')

    try:
        from cv2 import VideoWriter, imread, VideoWriter_fourcc
        from numpy import fromfile, uint8
    except ModuleNotFoundError:
        raise ModuleNotFoundError('请先安装cv2，pip install opencv-python')

    pic_list = Path(self._tmp_path or self._path).glob('*.jpg')
    img = imread(str(next(pic_list)))
    imgInfo = img.shape
    size = (imgInfo[1], imgInfo[0])

    videoWrite = VideoWriter(path, VideoWriter_fourcc(*"VP80"), 5, size)

    for i in pic_list:
        img = imread(str(i))
        videoWrite.write(img)

    rmtree(self._tmp_path)
    self._tmp_path = None
    return f'{self._path}{sep}{name}'
