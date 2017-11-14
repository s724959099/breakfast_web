from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(
    ['zip', 'txt', 'pdf', 'doc', 'docx',
     'ppt', 'pptx', 'png', 'jpg', 'jpeg',
     'gif', 'wav', 'mp3', 'aif', 'aiff',
     'aifc', 'flac', 'ape', 'wv', 'wma',
     'm4a', 'tta', 'tak', 'ogg', 'aac',
     'TXT', 'PDF', 'DOC', 'DOCX',
     'PPT', 'PPTX', 'PNG', 'JPG',
     'JPEG', 'GIF', 'WAV', 'MP3',
     'AIF', 'AIFF', 'AIFC', 'FLAC',
     'APE', 'WV', 'WMA', 'M4A', 'TTA', 'TAK',
     'OGG', 'AAC'
     ]
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class flaskUpload:
    def __init__(self, request):
        """
        you can get:
        allow_to_upload: check file can upload
        FileName:
        Format:
        file: real file
        size: size of file
        """
        self.request = request
        self.allow_to_upload = self.__allow_to_upload()
        if self.allow_to_upload:
            self.sFileName = secure_filename(self.file.filename)
            self.FileName = self.sFileName.split('.')[0]
            self.Format = self.sFileName.split('.')[1]
            self.size = len(self.file)

    def __allow_to_upload(self):
        if self.request.method != 'POST':
            return False
        if 'file' not in self.request.files:
            return False
        self.file = self.request.files['file']

        if self.file.filename == '':
            return False

        if self.file and allowed_file(self.file.filename):
            return True
        else:
            return False
