import datetime
import shutil
from moviepy.editor import VideoFileClip, vfx
import os
from moviepy.video.fx.all import crop


class ShortVideoMaker:
    def __init__(self, video_path) -> None:
        self.video = video_path
        if not os.path.exists("../media/shorts/"):
            os.makedirs("../media/shorts/")

    def make_video(self):
        try:
            # Load the input video clip
            input_clip = VideoFileClip(self.video)

            # Create a 60-second video clip (you can replace this with your own video or image)
            video_duration = input_clip.duration

            if video_duration >= 60:
                # Create a 60-second video clip starting from the end
                output_clip = input_clip.subclip(
                    video_duration - 90, video_duration-7)
                (w, h) = output_clip.size
                crop_width = h * 9/16
                x1, x2 = (w - crop_width)//2, (w+crop_width)//2
                y1, y2 = 0, h
                output_clip = crop(output_clip, x1=x1, y1=y1, x2=x2, y2=y2)
                output_clip = output_clip.fx(vfx.speedx, 1.5)
                # Write the final video to the specified output path
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Construct the new filename with the current date and time
                new_video_filename = f"short_video_{current_datetime}.mp4"
                output_video_path = f"../media/shorts/{new_video_filename}"
                # output_video_path = "../media/shorts/short_video.mp4"
                output_clip.write_videofile(
                    output_video_path, codec='libx264', threads=10, preset='ultrafast')
                input_clip.close()  # Explicitly close the input clip
                return output_video_path
            else:
                input_clip.close()  # Explicitly close the input clip
                return "Input video is less than 60 seconds in duration."
        except Exception as e:
            input_clip.close()  # Explicitly close the input clip
            return str(e)


if __name__ == "__main__":
    input_video_path = r"D:\Bots\LOL Heaven X\media\uploaded\test.mp4"
    input_video_path = input("Enter video path: ")
    short_video_maker = ShortVideoMaker(input_video_path)
    short_video_abs_path = short_video_maker.make_video()

    print(f"Short video created at: {short_video_abs_path}")
