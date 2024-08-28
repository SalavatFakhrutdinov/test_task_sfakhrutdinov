from django.shortcuts import render
from django.http import HttpResponse
from moviepy.editor import *
from .models import TextRequest
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


FONT_PATH = "/Users/sfakhrutdinov/PycharmProjects/test_task_sfakhrutdinov/other-formats/Monocraft.ttf"


def create_frame(text, width=400, height=100, frame_number=0, total_frames=0):
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Загружаем шрифт
    font = ImageFont.truetype(FONT_PATH, 20)

    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    # Вычисляем x координату для бегущей строки
    # Текст начнёт за границами изображения (по правой стороне)
    text_x = width - (frame_number * (width + text_width) // total_frames)

    # Если текст полностью вышел за пределы, возвращаем его обратно.
    if text_x < -text_width:
        text_x = width

    # Рисуем текст на изображении
    draw.text((text_x, (height - bbox[3] + bbox[1]) // 2), text, font=font, fill=(0, 0, 0))

    return np.array(image)


def make_text_movie(text, duration=5, fps=24):
    clips = []
    width, height = 400, 100  # Размеры видео
    frame_count = duration * fps

    for i in range(frame_count):
        frame = create_frame(text, width, height, i, frame_count)
        clip = ImageClip(frame).set_duration(1 / fps)
        clips.append(clip)

    video = concatenate_videoclips(clips)
    return video


def index(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        duration = int(request.POST.get('duration', 3))
        video = make_text_movie(text, duration)
        video_filename = "running_str.mp4"
        video.write_videofile(video_filename, fps=24)

        # Сохранение запроса в БД
        text_request = TextRequest(text=text, duration=duration)
        text_request.save()

        with open(video_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="running_str.mp4"'
            return response

    return render(request, 'running_str_app/index.html')
