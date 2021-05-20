from datetime import datetime
import ffmpeg
from pathlib import Path

BASE_DIR = Path(__file__).resolve()
mp4_dir = BASE_DIR.joinpath("mysql")
output_dir = BASE_DIR.joinpath("output")
# output_dir.mkdir(exist_ok=True)


def filter_xml(filename):
    extension = str(filename).split(".")[-1]
    if extension != "xml":
        return filename


def get_mp4_list():
    mp4_filter = filter(filter_xml, list(mp4_dir.iterdir()))
    mp4 = list(mp4_filter)
    return mp4


def get_video(filename):
    episode = filename.name.split(".")[-2][-3:-1]
    if episode == "00":
        return filename


def get_audio(filename):
    episode = filename.name.split(".")[-2][-3:-1]
    if episode == "01":
        return filename


def video_audio_input(all_video, all_audio):
    for video_file, audio_file in zip(all_video, all_audio):
        yield video_file, audio_file


def set_filename(file):
    filename = file.name.split(".")
    filename = [
        filename[-2].strip()[:-5],
        datetime.now().strftime("%H%M%S"),
        filename[-1],
    ]
    return ".".join(filename)


def merge(video, audio, all_mp4_list):
    episode_video_list = list(filter(video, all_mp4_list()))
    episode_audio_list = list(filter(audio, all_mp4_list()))

    for video, audio in video_audio_input(
        episode_video_list, episode_audio_list
    ):
        input_video = ffmpeg.input(video)
        input_audio = ffmpeg.input(audio)
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
            str(output_dir.joinpath(set_filename(video)))
        ).run()


# merge(get_video, get_audio, get_mp4_list)
print(BASE_DIR)