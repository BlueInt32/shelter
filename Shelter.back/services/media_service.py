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
from domain.enums import PersistanceType

def build_element(payload, element_type):
    tags_associated = resolve_tags(payload['tags'])
    new_element = Element(
        payload['title'], payload['text'], tags_associated, element_type, '')
    return new_element

def update_element(payload, existing_element, element_type):
    tags_associated = resolve_tags(payload['tags'])
    existing_element.title = payload['title']
    existing_element.text = payload['text']
    existing_element.link_url = payload['linkUrl']
    existing_element.tags = tags_associated
    existing_element.type = element_type

def persist_element(element, persistance_type):
    if persistance_type == PersistanceType.CREATE:
        db.session.add(element)
    db.session.commit()


def generate_thumbnail_for_image(element):
    # thumbnail generation
    if element.attached_file is not None:
        stream = io.BytesIO(element.attached_file)
        im = Image.open(stream)
        im.thumbnail((128, 128))
        imgByteArr = io.BytesIO()
        im.convert('RGB').save(imgByteArr, "JPEG")
        element.attached_thumb = imgByteArr.getvalue()

def generate_thumbnail_for_video(element, youtube_dl_json_output, original_media_abs_path):
    if youtube_dl_json_output is not None \
       and youtube_dl_json_output.extractor == 'Reddit' \
       and hasattr(youtube_dl_json_output, 'thumbnail'):
        response = urllib.request.urlopen(youtube_dl_json_output.thumbnail)
        request_data = response.read()
        element.attached_thumb = request_data
    else:
        # file upload OR 'Gfycat' link 'Imgur' link
        template_call = Template(
            "$ffmpeg_path -y -i \"$input_path\" -ss 00:00:00.000 -vframes 1 -filter:v scale=\"-1:300\" tempyoudl/temp.jpg")
        call = template_call.substitute(
            ffmpeg_path=Config.ffmpeg_path,
            input_path=original_media_abs_path)
        subprocess.run(call)
        in_file = open("tempyoudl/temp.jpg", "rb")

        element.attached_thumb = in_file.read()
        in_file.close()
        os.remove(original_media_abs_path)
        os.remove("tempyoudl/temp.jpg")


def save_element_with_image_file(persistanceType, request_data):
    parsed_payload = request_data['payload'][0]

    if parsed_payload is not None:
        payload = json.loads(parsed_payload.read().decode("utf-8"))

    element_type = 'image_file'
    if persistanceType == PersistanceType.CREATE:
        element = build_element(payload, element_type)
    else:
        element = Element.query.get_or_404(payload.id)
        update_element(payload, element, element_type)

    # file uploaded in form
    if 'file' in request_data:
        imageFile = request_data['file'][0]
        element.attached_file = imageFile.stream.read()

    generate_thumbnail_for_image(element)

    persist_element(element, persistanceType)
    return element

def save_element_with_image_link(persistanceType, payload):
    element_type = 'image_link'
    if persistanceType == PersistanceType.CREATE:
        element = build_element(payload, element_type)
    else:
        element = Element.query.get_or_404(payload.id)
        update_element(payload, element, element_type)

    if payload['linkUrl'] != '':
        response = urllib.request.urlopen(payload['linkUrl'])
        request_data = response.read()
        element.attached_file = request_data

    generate_thumbnail_for_image(element)

    new_element = persist_element(element, persistanceType)
    return new_element

def save_element_with_video_file(persistanceType, request_data):
    parsed_payload = request_data['payload'][0]
    script_dir = os.path.dirname(__file__)
    abs_file_path = ''
    payload = json.loads(parsed_payload.read().decode("utf-8"))

    element_type = 'video_file'
    if persistanceType == PersistanceType.CREATE:
        element = build_element(payload, element_type)
    else:
        element = Element.query.get_or_404(payload.id)
        update_element(payload, element, element_type)

    # file uploaded in form
    if 'file' in request_data:
        imageFile = request_data['file'][0]
        element.attached_file = imageFile.stream.read()
        abs_file_path = os.path.join(script_dir, '../tempyoudl/temp.binary')
        ofile = open(abs_file_path, 'w+b')
        ofile.write(element.attached_file)
        ofile.close()

    generate_thumbnail_for_video(element, None, abs_file_path)
    persist_element(element, persistanceType)
    return element

def save_element_with_video_link(persistanceType, payload):
    script_dir = os.path.dirname(__file__)
    youtube_dl_json_output = None

    element_type = 'video_link'
    if persistanceType == PersistanceType.CREATE:
        element = build_element(payload, element_type)
    else:
        element = Element.query.get_or_404(payload.id)
        update_element(payload, element, element_type)

    if payload['linkUrl'] != '':
        # get reddit video info
        out = subprocess.check_output(
            [Config.youtube_dl_path, payload['linkUrl'], "-j"])
        youtube_dl_json_output = json.loads(out, object_hook=lambda d: Namespace(**d))
        t = Template('../tempyoudl/$title.$ext')
        clean_title = re.sub(r'\W+', '', youtube_dl_json_output.title)
        rel_file_path = t.substitute(title=clean_title, ext='mkv')
        abs_file_path = os.path.join(
            script_dir, t.substitute(title=clean_title, ext='mkv'))
        subprocess.run(
            [Config.youtube_dl_path, payload['linkUrl'], "-o", abs_file_path, "--merge-output-format", "mkv"])
        in_file = open(abs_file_path, "rb")
        element.attached_file = in_file.read()
        in_file.close()

    generate_thumbnail_for_video(element, youtube_dl_json_output, abs_file_path)
    persist_element(element, persistanceType)
    return element

def save_element_with_web_link(persistanceType, payload):
    element_type = 'web_link'
    if persistanceType == PersistanceType.CREATE:
        element = build_element(payload, element_type)
    else:
        element = Element.query.get_or_404(payload.id)
        update_element(payload, element, element_type)

    new_element = persist_element(element, PersistanceType.CREATE)
    return new_element
