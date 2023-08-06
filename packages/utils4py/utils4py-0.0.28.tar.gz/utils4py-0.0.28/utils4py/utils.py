#!/usr/bin/env python
# coding: utf-8

import base64
import datetime
import hashlib
import hmac
import os
import random
import re
import time
from io import BytesIO

from captcha.image import ImageCaptcha
from Crypto import Random
from Crypto.Cipher import AES
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from sqlalchemy import Date, DateTime, Numeric


def md5bytes(bs):
    """
    md5bytes
    @param bs bytes
    """
    m = hashlib.md5()
    m.update(bs)
    return m.hexdigest()


def md5(strs):
    """
    md5
    """
    return md5bytes(strs.encode(encoding="utf-8"))


def sha256bytes(bs):
    """
    sha256
    """
    hash = hashlib.sha256()
    hash.update(bs)
    return hash.hexdigest()


def sha256(strs):
    return sha256bytes(strs.encode("utf-8"))


def extension(filename):
    """
    file extension
    """
    ext = os.path.splitext(filename)[1]
    if ext == "":
        ext = os.path.splitext(filename)[0]
    if ext.startswith("."):
        ext = ext[1:]
    return ext


def check_phone_number(phone_number):
    """
    check if the phone number valid
    """
    return True if re.match("^1[3-9]{1}[0-9]{9}$", phone_number) else False


def model_to_dict(model):
    """
    model to dict
    """

    def convert_datetime(value):
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ""

    data = {}
    for col in model.__table__.columns:
        value = getattr(model, col.name)
        if isinstance(col.type, DateTime) and isinstance(value, DateTime):
            value = convert_datetime(value)
        elif isinstance(col.type, Numeric):
            value = str(value)
             
        data[col.name] = value

    return data


def random_string(len=5):
    """
    random string
    0-9 a-z A-Z
    """
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(len):
        chars.append(random.choice(ALPHABET))

    return "".join(chars)


pad = lambda s: (s + (
    AES.block_size
    - (
        16
        if (len(s) % AES.block_size == 0 and len(s) != 0)
        else (len(s) % AES.block_size)
    )
) * chr(0)).encode("utf-8")


def encrypt(content, key="1234567890", expires=0):
    """
    加密
    @param content 加密内容
    @param key 
    @param expires 过期时间
    """
    iv = Random.new().read(AES.block_size)
    cryptor = AES.new(pad(key), AES.MODE_CBC, iv)
    ciphertext = cryptor.encrypt(pad(content))

    return base64.urlsafe_b64encode(
        iv
        + (str(int(time.time() + expires)) if expires else str(0) * 10).encode()
        + ciphertext
    ).decode()


def decrypt(content, key="1234567890"):
    """
    解密
    @param 解密内容
    @param key
    """
    ciphertext = base64.urlsafe_b64decode(content)
    iv = ciphertext[0 : AES.block_size]
    expires = int(ciphertext[AES.block_size : AES.block_size + 10])
    if expires and expires <= int(time.time()):
        return ""

    ciphertext = ciphertext[AES.block_size + 10 : len(ciphertext)]
    cryptor = AES.new(pad(key), AES.MODE_CBC, iv)
    plaintext = cryptor.decrypt(ciphertext).decode()

    return plaintext.rstrip(chr(0))


def get_items(items) -> list:
    """
    get all items
    """

    def calculate(lst):
        t = type(lst)
        if t in [list, tuple]:
            for item in lst:
                calculate(item)
        elif t == dict:
            for _, item in lst.items():
                calculate(item)
        else:
            result.append(lst)
            return

    result = []
    calculate(items)
    return result


def captcha(size=4, width=240, height=60, font=None, font_size=36, noise=True):
    """
    验证码
    @param width default: 240
    @param height default: 60
    """
    image = Image.new("RGB", (width, height), (255, 255, 255))
    font = ImageFont.truetype(
        font=font
        if font
        else os.path.join(os.path.abspath(os.path.dirname(__file__)), "Arial.ttf"),
        size=font_size,
    )
    draw = ImageDraw.Draw(image)
    if noise:
        for x in range(width):
            for y in range(height):
                if random.randint(0, 1):
                    draw.point(
                        (x, y),
                        fill=(
                            random.randint(64, 255),
                            random.randint(64, 255),
                            random.randint(64, 255),
                        ),
                    )
    code = []
    remainder = width % size
    unit = int((width - remainder) / size)
    y = int((height - font_size) / 2)
    offset_x = int(remainder / 2)
    for t in range(size):
        c = random_string(1)
        code.append(c)
        draw.text(
            (unit * t + offset_x, y),
            c,
            font=font,
            fill=(
                random.randint(32, 127),
                random.randint(32, 127),
                random.randint(32, 127),
            ),
        )
    image = image.filter(ImageFilter.BLUR)

    img_io = BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)

    return "".join(code), img_io


def captcha2():
    code = random_string(4)
    image = ImageCaptcha().generate_image(code)

    img_io = BytesIO()
    image.save(img_io, "JPEG", quality=70)
    img_io.seek(0)

    return code, img_io
