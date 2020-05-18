import json
from services.tags_service import resolve_tags
from models import db, Element, Tag
import subprocess
import urllib.request
import io
from PIL import Image
from types import SimpleNamespace as Namespace
from string import Template
import os
from config import Config
import re
import string

def handle_web_link(request_data):
    parsed = request_data
    tags_associated = resolve_tags(parsed['tags'])
    new_element = Element(
        parsed['title'], parsed['text'], tags_associated, 'web_link', parsed['linkUrl'])
    db.session.add(new_element)
    db.session.commit()
    return new_element


def handle_image_file(request_data):
    payload = request_data['payload'][0]

    if payload is not None:
        parsed = json.loads(payload.read().decode("utf-8"))
        print(parsed['title'])

    tags_associated = resolve_tags(parsed['tags'])
    new_element = Element(
        parsed['title'], parsed['text'], tags_associated, 'image', '')

    # file uploaded in form
    if 'file' in request_data:
        imageFile = request_data['file'][0]
        new_element.attached_file = imageFile.stream.read()

    # otherwise file in a link

    # thumbnail generation

    if new_element.attached_file is not None:
        stream = io.BytesIO(new_element.attached_file)
        im = Image.open(stream)
        im.thumbnail((128, 128))
        # im.save(outfile, "JPEG")
        imgByteArr = io.BytesIO()
        im.convert('RGB').save(imgByteArr, "JPEG")
        new_element.attached_thumb = imgByteArr.getvalue()

    db.session.add(new_element)
    db.session.commit()
    return new_element

def handle_image_link(request_data):
    parsed = request_data

    tags_associated = resolve_tags(parsed['tags'])
    new_element = Element(
        parsed['title'], parsed['text'], tags_associated, 'image', parsed['linkUrl'])

    if parsed['linkUrl'] != '':
        # download media
        response = urllib.request.urlopen(parsed['linkUrl'])
        request_data = response.read()
        new_element.attached_file = request_data

    # thumbnail generation

    if new_element.attached_file is not None:
        stream = io.BytesIO(new_element.attached_file)
        im = Image.open(stream)
        im.thumbnail((500, 500))
        # im.save(outfile, "JPEG")
        imgByteArr = io.BytesIO()
        im.convert('RGB').save(imgByteArr, "JPEG")
        new_element.attached_thumb = imgByteArr.getvalue()

    db.session.add(new_element)
    db.session.commit()
    return new_element


def handle_video_file(request_data):
    payload = request_data['payload'][0]
    script_dir = os.path.dirname(__file__)
    abs_file_path = ''
    x = None

    if payload is not None:
        parsed = json.loads(payload.read().decode("utf-8"))
        print(parsed['title'])

    tags_associated = resolve_tags(parsed['tags'])
    new_element = Element(
        parsed['title'], parsed['text'], tags_associated, 'video', '')

    # file uploaded in form
    if 'file' in request_data:
        imageFile = request_data['file'][0]
        new_element.attached_file = imageFile.stream.read()
        abs_file_path = os.path.join(script_dir, '../tempyoudl/temp.binary')
        ofile = open(abs_file_path, 'w+b')
        ofile.write(new_element.attached_file)
        ofile.close()

    # thumbnail retrieval
    if x is not None and x.extractor == 'Reddit':
        response = urllib.request.urlopen(x.thumbnail)
        request_data = response.read()
        new_element.attached_thumb = request_data
    else:
        # x.extractor == 'Gfycat' or x.extractor == 'Imgur':
        print(Config.ffmpeg_path)
        template_call = Template(
            "$ffmpeg_path -y -i \"$input_path\" -ss 00:00:00.000 -vframes 1 -filter:v scale=\"-1:300\" tempyoudl/temp.jpg")
        call = template_call.substitute(
            ffmpeg_path=Config.ffmpeg_path,
            input_path=abs_file_path)
        print(call)
        subprocess.run(call)
        in_file = open("tempyoudl/temp.jpg", "rb")

        new_element.attached_thumb = in_file.read()
        in_file.close()
        os.remove(abs_file_path)
        os.remove("tempyoudl/temp.jpg")

    db.session.add(new_element)
    db.session.commit()
    return new_element

def handle_video_link(request_data):
    parsed = request_data
    script_dir = os.path.dirname(__file__)
    abs_file_path = ''
    x = None

    tags_associated = resolve_tags(parsed['tags'])
    new_element = Element(
        parsed['title'], parsed['text'], tags_associated, 'video', parsed['linkUrl'])

    # otherwise file in a link
    if parsed['linkUrl'] != '':
        # get reddit video info
        out = subprocess.check_output(
            [Config.youtube_dl_path, parsed['linkUrl'], "-j"])
        x = json.loads(out, object_hook=lambda d: Namespace(**d))
        t = Template('../tempyoudl/$title.$ext')
        clean_title = re.sub(r'\W+', '', x.title)
        rel_file_path = t.substitute(title=clean_title, ext='mkv')
        abs_file_path = os.path.join(
            script_dir, t.substitute(title=clean_title, ext='mkv'))
        subprocess.run(
            [Config.youtube_dl_path, parsed['linkUrl'], "-o", abs_file_path, "--merge-output-format", "mkv"])
        in_file = open(abs_file_path, "rb")
        new_element.attached_file = in_file.read()

    # thumbnail retrieval
    if x is not None and x.extractor == 'Reddit':
        response = urllib.request.urlopen(x.thumbnail)
        request_data = response.read()
        new_element.attached_thumb = request_data
    else:
        # x.extractor == 'Gfycat' or x.extractor == 'Imgur':
        print(Config.ffmpeg_path)
        template_call = Template(
            "$ffmpeg_path -y -i \"$input_path\" -ss 00:00:00.000 -vframes 1 -filter:v scale=\"-1:300\" tempyoudl/temp.jpg")
        call = template_call.substitute(
            ffmpeg_path=Config.ffmpeg_path,
            input_path=abs_file_path)
        print(call)
        subprocess.run(call)
        in_file = open("tempyoudl/temp.jpg", "rb")

        new_element.attached_thumb = in_file.read()
        in_file.close()
        os.remove(abs_file_path)
        os.remove("tempyoudl/temp.jpg")

    db.session.add(new_element)
    db.session.commit()
    return new_element
