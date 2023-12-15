import qrand
from qrand import QRNG
#Cipher
from cryptography.fernet import Fernet
#Generate Quantum Random Encryption Seed
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
#Normal AES Algorithm
class QuantumAES(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)
    def decrypt_with_seed(self, encrypted_text, seed):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        try:
            cipher = AES.new(hashlib.sha256(seed.encode()).digest(), AES.MODE_CBC, iv)
            plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
            return self.__unpad(plain_text)
        except:
            print("Unable to decypt, key does not match")

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]
#Generate Encryption Object

#Generate QRN
Quantum_Number = QRNG()
#Create encryption object with QRN as the Key
QuantumAESObject = QuantumAES(str(Quantum_Number.generate_binary_array(10, True)))
enc_text = QuantumAESObject.encrypt(input("Enter Text To Encrypt: "))
print(QuantumAESObject.decrypt_with_seed(enc_text, input("Enter Decryption Key: ")))

'''try:
    #Encrypt and Immeadiately Decrypt Text
    print(QuantumAESObject.decrypt(QuantumAESObject.encrypt(input("Enter Text To Encrypt: "))))
except:
    print("Unable to Decrypt")
    '''