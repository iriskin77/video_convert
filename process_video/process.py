import os
import logging
import ffmpeg
import shutil
from .models import VideoFile


logger = logging.getLogger('main')


def get_width_height_video(file_path: str) -> tuple[int, int]:
    try:
        logger.info(f"Fn get_width_height_video has started")
        probe = ffmpeg.probe(file_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        logger.info(f"Fn get_width_height_video has finished successfully")
        return width, height

    except Exception as ex:
        logger.warning(f"Fn get_width_height_video has finished incorrectly: {ex}")


def change_video_resolution(file_path: str, update_width: int, update_height: int, pk) -> None:
    try:
        logger.info("Fn change_video_resolution has started")
        path_original = str(file_path)
        dir_copy = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"media/video_copy/")

        path_to_copy_file = shutil.copy(path_original, dir_copy)

        stream = ffmpeg.input(str(path_to_copy_file))
        stream = stream.filter('scale', w=update_width, h=update_height)
        stream = ffmpeg.output(stream, path_original)
        VideoFile.objects.filter(pk=pk).update(is_processing=True)
        ffmpeg.run(stream, overwrite_output=True)
        os.remove(path_to_copy_file)
        VideoFile.objects.filter(pk=pk).update(processing_success=True,
                                               is_processing=False,
                                               width=update_width,
                                               height=update_height)
        logger.info("Fn change_video_resolution has finished successfully")
    except Exception as ex:
        VideoFile.objects.filter(pk=pk).update(processing_success=False, is_processing=False)
        logger.warning(f"Fn change_video_resolution has finished incorrectly: {ex}")

