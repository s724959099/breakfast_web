from libs.flask_get import *
import base64
from PIL import Image
import io

class flaskImg:
    def __init__(self):
        pass
    def croppic_to_base64(self):
        img = form_get('img')
        imgUrl = form_get('imgUrl')
        imgInitW = form_get('imgInitW')
        imgInitH = form_get('imgInitH')
        imgW = form_get('imgW')
        imgH = form_get('imgH')
        imgX1 = form_get('imgX1')
        imgY1 = form_get('imgY1')
        cropW = form_get('cropW')
        cropH = form_get('cropH')
        contentType = imgUrl.split(';')[0].split('data:')[1]
        # original size
        imgInitW, imgInitH = int(imgInitW), int(imgInitH)
        # Adjusted size
        imgW, imgH = int(float(imgW)), int(float(imgH))
        # bias
        imgY1, imgX1 = int(imgY1), int(imgX1)
        # crop w and h
        cropW, cropH = int(cropW), int(cropH)

        img_data = imgUrl
        ext = img_data.split('base64,')[0].split('/')[1].split(';')[0]
        img_data = img_data.split('base64,')[1]
        title = imgUrl.split('base64,')[0] + 'base64,'
        imgData = base64.b64decode(img_data)

        source_image = Image.open(io.BytesIO(imgData))

        # create new crop image
        source_image = source_image.resize((imgW, imgH), Image.ANTIALIAS)
        box = (imgX1, imgY1, imgX1 + cropW, imgY1 + cropH)
        newImg = source_image.crop(box)
        imgByteArr = io.BytesIO()
        newImg.save(imgByteArr, format=ext)
        imgByteArr = imgByteArr.getvalue()
        imgbase = base64.b64encode(imgByteArr).decode('ascii')
        encode64 = title + imgbase

        return encode64

    def base64_to_byte(self,base64Data):
        self.base64Data = base64Data
        self.contentType = base64Data.split(';')[0].split('data:')[1]
        self.ext = base64Data.split('base64,')[0].split('/')[1].split(';')[0]
        base64_data = base64Data.split('base64,')[1]
        self.title = base64Data.split('base64,')[0] + 'base64,'
        self.byteimageData = base64.b64decode(base64_data)