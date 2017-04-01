from config import Config
import os
from PIL import Image
import requests
import json
import re


def _convert_pdf_to_image(input_file):
    print 'Converting pdf to image...'

    os.system('%s %s' % (Config.Paths.pdf2bmp, input_file))

    file_parts = input_file.split('.')
    return file_parts[0] + '_000001.bmp'


def _crop_amount_from_bill(input_file, output_file):
    print 'Cropping image...'

    bill_image = Image.open(input_file)
    amount_image = bill_image.crop(Config.OCR.amount_crop_bouns)
    amount_image.save(output_file)
    return amount_image


def _convert_image_to_float(input_file):
    print 'Parsing image...'

    payload = {'isOverlayRequired': False, 'apikey': Config.OCR.api_key, 'language': 'eng'}

    with open(input_file, 'rb') as f:
        response = requests.post(Config.OCR.api_url, files={'filename': f}, data=payload)

    response_json = json.loads(response.content)
    amount_raw_text = response_json['ParsedResults'][0]['ParsedText']

    amount_text = re.compile(r'[\s,]+').sub('', amount_raw_text)
    amount_value = float(amount_text)
    return amount_value


def extract_amount_from_pdf(input_file):
    bmp_file = _convert_pdf_to_image(input_file)
    bmp_file_cropped = bmp_file.split('.')[0] + '_cropped.bmp'
    _crop_amount_from_bill(bmp_file, bmp_file_cropped)
    amount = _convert_image_to_float(bmp_file_cropped)
    return amount

