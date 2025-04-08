from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_subtitle(video_path, subtitle_text, output_path,
                 fontsize=48, color='white', font='Arial',
                 position='center', duration=5):
    """
    给视频添加静态字幕。

    Args:
        video_path: 视频文件路径。
        subtitle_text: 字幕文本。
        output_path: 输出视频文件路径。
        fontsize: 字幕字体大小。
        color: 字幕颜色。
        font: 字幕字体。
        position: 字幕位置 (可以是 'center', 'top', 'bottom', 或者坐标元组)。
        duration: 字幕显示持续时间 (秒)。

    """
    clip = VideoFileClip(video_path)

    txt_clip = TextClip(subtitle_text, fontsize=fontsize, color=color, font=font)
    txt_clip = txt_clip.set_pos(position).set_duration(duration)

    final_clip = CompositeVideoClip([clip, txt_clip])

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    clip.close()
    final_clip.close()

# 示例用法
video_path = "input_video.mp4"
output_path = "output_video_with_subtitle.mp4"
subtitle_text = "This is a sample subtitle."

add_subtitle(video_path, subtitle_text, output_path)