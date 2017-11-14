import base64

try:
    from Crypto.Cipher import AES
    from Crypto import Random
except:
    pass

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode("utf-8")


if __name__ == "__main__":
    API_KEY="mysecretpassword"
    private_key = "SiniBestgoodgood"
    print(len(API_KEY))
    cipher = AESCipher(private_key)
    encrypted = cipher.encrypt('Secret Message A')

    # ciper2=AESCipher(private_key)
    # encrypted2=ciper2.encrypt(encrypted)
    # decrypted2=ciper2.decrypt(encrypted)


    decrypted = cipher.decrypt("\x3145486b65587630626c6e322b38467971324f6868546c33423364352f2f5a6b446f466d456979357438413d")

    # cipher2=AESCipher('mysecretpassword2')
    # decrypted2=cipher2.decrypt(encrypted)
    print(str(encrypted))
    print(decrypted)
    # print(decrypted2)
    # print(decrypted2)
