import os
from .models import VideoFile
import ffmpeg
import shutil


def get_width_height_video(file_path: str) -> tuple[int, int]:
    try:
        path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"media/video_files/{str(file_path)}")
        print(path_to_file)
        probe = ffmpeg.probe(path_to_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return width, height

    except Exception as ex:
        print(f'Error {ex}')


def change_video_resolution(file_path: str, update_weight: int, update_height: int, pk) -> None:
    try:

        path_original = str(file_path)
        dir_copy = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"media/video_copy/")

        path_to_copy_file = shutil.copy(path_original, dir_copy)

        stream = ffmpeg.input(str(path_to_copy_file))
        stream = stream.filter('scale', w=update_weight, h=update_height)
        stream = ffmpeg.output(stream, path_original)
        VideoFile.objects.filter(pk=pk).update(is_processing=True)
        ffmpeg.run(stream, overwrite_output=True)
        os.remove(path_to_copy_file)
        VideoFile.objects.filter(pk=pk).update(processing_success=True,
                                               is_processing=False,
                                               weight=update_weight,
                                               height=update_height)
    except Exception as ex:
        VideoFile.objects.filter(pk=pk).update(processing_success=False, is_processing=False)
        print(f'Error {ex}')

