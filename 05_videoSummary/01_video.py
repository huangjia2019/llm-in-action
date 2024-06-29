import os
import cv2
import base64
import time
import openai
from moviepy.editor import VideoFileClip
from tqdm import tqdm

# 创建OpenAI客户端
from openai import OpenAI 
client = OpenAI()

# 提取视频帧和音频的函数
def extract_frames_and_audio(video_file, interval=2):
    encoded_frames = []
    file_name, _ = os.path.splitext(video_file)

    video_capture = cv2.VideoCapture(video_file)
    total_frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    frames_interval = int(frame_rate * interval)
    current_frame = 0

    while current_frame < total_frame_count - 1:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        success, frame = video_capture.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_frames.append(base64.b64encode(buffer).decode("utf-8"))
        current_frame += frames_interval
    video_capture.release()

    audio_output = f"{file_name}.mp3"
    video_clip = VideoFileClip(video_file)
    video_clip.audio.write_audiofile(audio_output, bitrate="32k")
    video_clip.audio.close()
    video_clip.close()

    return encoded_frames, audio_output

# 生成视频总结的函数
def generate_summary(frames, transcript, model='gpt-4o'):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你正在生成视频的总结。请提供视频的总结，并以Markdown格式回应。"},
            {"role": "user", "content": [
                "这些是视频的帧。",
                *map(lambda x: {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, frames),
                {"type": "text", "text": f"音频转录内容是: {transcript}"}
            ]}
        ],
        temperature=0,
    )
    return response.choices[0].message.content

# 主函数
def main():
    video_directory = "10_Applications/06_VideoCaption"  # 请设置视频文件夹路径
    output_directory = "10_Applications/06_VideoCaption/output"  # 请设置输出文件夹路径
    os.makedirs(output_directory, exist_ok=True)

    video_files = [f for f in os.listdir(video_directory) if f.endswith(('.mp4', '.avi', '.mkv'))]
    
    for video_file in tqdm(video_files, desc="Processing videos", unit="file"):
        video_path = os.path.join(video_directory, video_file)
        print(f"\n正在处理视频文件: {video_path}")

        frames, audio_path = extract_frames_and_audio(video_path, interval=2)
        
        # 使用Whisper模型转录音频
        transcription_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=open(audio_path, "rb")
        )
        print('\n'+transcription_response)  

        transcript = transcription_response.text
        
        summary = generate_summary(frames, transcript)
        
        # 将结果保存为Markdown文件
        md_filename = os.path.join(output_directory, f"{os.path.splitext(video_file)[0]}.md")
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(summary)
        
        print(f"视频文件 {video_file} 处理完成。总结已保存到 {md_filename}")

if __name__ == "__main__":
    main()

