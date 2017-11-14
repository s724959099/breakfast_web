from azure.storage.blob import BlockBlobService, PublicAccess, ContentSettings
from flask import Response
import io
import zipfile
import datetime

blob_account = 'cloudesignblob'
blob_key = 'LgUF/eFLexmvg4e2QQvvrLdvJepQ9MImiFwbqUymYdNKB/Be4DMghgoSxUALA69s3sXgtkIPFNsdCOoDPtDefg=='
blobUrl = 'https://cloudesignblob.blob.core.windows.net/'

"""
container is tenant
blob is CompanyId/uuid
so Pictureurl is tenant/CompanyId/uui to store
"""


class AzureBlob:
    def __init__(self):
        # self.container_name = container_name.lower()
        self._azureblob=BlockBlobService(account_name=blob_account, account_key=blob_key)

    def isExist(self,containerName,blobName):
        return self._azureblob.exists(containerName,blobName)

    def save_from_byte(self, container,blobName, blobByte, contentType):
        size = len(blobByte)
        self._azureblob.create_container(container.lower())
        self._azureblob.create_blob_from_bytes(container.lower(), blobName.lower(),
                                    blobByte,
                                    content_settings=ContentSettings(content_type=contentType),
                                    count=size
                                    )

    def save_from_file(self, containerName, blobName, file):
        blobByte = file.read()
        #TODO: not sure file.content_type
        self.save_from_byte(containerName,blobName,blobByte,file.content_type)

    def pic_to_url(self,PictureUrl,seconds=50):
        split=PictureUrl.split("/",1)
        containerName=split[0]
        blobName=split[1]
        return self.make_blob_url(containerName,blobName,seconds)

    def make_blob_url(self,containerName,blobName,seconds=50):
        deviation = 10
        containerName = containerName.lower()
        blobName = blobName.lower()
        access_signature = self._azureblob.generate_blob_shared_access_signature(
            containerName, blobName,
            'rl',
            datetime.datetime.utcnow() + datetime.timedelta(seconds=(seconds + deviation)),
            start=datetime.datetime.utcnow() - datetime.timedelta(seconds=deviation)
        )
        blob_url = self._azureblob.make_blob_url(containerName, blobName, 'https', access_signature)
        return blob_url


class __AzureBlob(BlockBlobService):
    def __init__(self, container_name=None):
        if container_name is not None:
            self.container_name = container_name.lower()
        super().__init__(account_name=blob_account, account_key=blob_key)


    def download_muti_file_in_zip_by_tracks(self, downloadTracks,zipName="downloads"):
        res = Response()
        # https://tracksterblob.blob.core.windows.net/2bwkwyqu9fd6pv5/a18se4mozqozji7.mp3
        res.mimetype = 'application/zip'
        res.headers['Content-Disposition'] = 'attachment;filename={}.zip'.format(zipName)
        zipstream = io.BytesIO()
        zip_file = zipfile.ZipFile(zipstream, 'w', zipfile.ZIP_DEFLATED)
        fileName_array = []
        for t in downloadTracks:
            # get file from blob
            fileUrl = t['file']
            fileUrl = fileUrl.split(blobUrl)[1]
            contentName = fileUrl.split('/')[0]
            blobName = t['BlobFileName']
            # if file name is same then  add xxx(1).format
            origin_FileName = t['trackName']
            if origin_FileName in fileName_array:
                count = fileName_array.count(origin_FileName)
                origin_FileName += "({})".format(count)

            file_format = ".{}".format(t["Format"])
            if origin_FileName.endswith(file_format):
                fileName = origin_FileName
            else:
                fileName = "{}{}".format(origin_FileName, file_format)
            fileName_array.append(t['trackName'])

            blobName = blobName.lower()
            if super().exists(contentName, blobName):
                b = self.get_blob_to_bytes(contentName, blobName)
                zip_file.writestr(fileName, b.content)
        zip_file.close()

        temp = zipstream.seek(0)
        value = zipstream.getvalue()
        res.data = value
        return res

    def download_single_file(self, blobName, fileName):
        res = Response()
        res.mimetype = 'application/zip'
        res.headers['Content-Disposition'] = 'attachment;filename={}'.format(fileName)
        b = self.get_blob_to_bytes(self.container_name, blobName.lower())

        res.data = b.content
        return res

    def check_blob_exist(self, blobName):
        try:
            self.get_blob_to_bytes(self.container_name, blobName)
            return True
        except:
            return False

    def exists(self, blob_name=None):
        return super().exists(self.container_name, blob_name.lower())

    def svae_from_stream(self, blobName, file):
        blob = file.read()
        size = len(blob)

        self.create_container(self.container_name)
        self.create_blob_from_bytes(self.container_name.lower(), blobName.lower(),
                                    blob,
                                    content_settings=ContentSettings(content_type='audio/wav'),
                                    count=size
                                    )
        return size

    def save_from_byte(self, blobName, blob, contentType):
        size = len(blob)
        self.create_container(self.container_name.lower())
        self.create_blob_from_bytes(self.container_name.lower(), blobName.lower(),
                                    blob,
                                    content_settings=ContentSettings(content_type=contentType),
                                    count=size
                                    )


    @property
    def block_blob_service(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'azure_block_blob_service'):
                ctx.azure_block_blob_service = self.account.create_block_blob_service()
            return ctx.azure_block_blob_service


def make_blob_urL(container, blob, seconds=50):
    """
    date:1114
    get blob signature and return new url
    :param container:
    :param blob:
    :param seconds:
    :return:
    """
    deviation = 10
    a = AzureBlob()
    container = container.lower()
    blob = blob.lower()
    access_signature = a.generate_blob_shared_access_signature(
        container, blob,
        'rl',
        datetime.datetime.utcnow() + datetime.timedelta(seconds=(seconds + deviation)),
        start=datetime.datetime.utcnow() - datetime.timedelta(seconds=deviation)
    )
    blob_url = a.make_blob_url(container, blob, 'https', access_signature)
    return blob_url


def trackToUrl(TrackId):
    tk = db.session.query(Tracks).filter(
        Tracks.TrackId == TrackId
    ).scalar()
    url = make_blob_urL(tk.UserId, tk.BlobFileName)
    return url


if __name__ == '__main__':
    import io

    a = AzureBlob('testing')
    io = io.BytesIO()
    g = a.get_blob_to_stream("testing", "testing.mp3", io)
    print("done")



    # b=a.get_blob_to_bytes('testing','g1')


    # zipstream=io.BytesIO()
    # zip_file = zipfile.ZipFile(zipstream, 'w', zipfile.ZIP_DEFLATED)
    # zip_file.writestr('test.jpg',b.content)
    # zip_file.close()
    #
    # temp=zipstream.seek(0)
    # value=zipstream.getvalue()
    # print('test')
