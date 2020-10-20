from Crypto.Cipher import AES


def read_file(path):
    with open(path, 'rb') as file:
        return file.read()


def write_file(path, data):
    with open(path, 'wb') as file:
        file.write(data)
    print('Write completed.')


if __name__ == "__main__":
    key = read_file("/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab02/2020_09_25_10_31_48_santiago.del.rey.key")
    enc_message = read_file(
        "/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab02/2020_09_25_10_31_48_santiago.del.rey.enc")

    aes = AES.new(key, AES.MODE_CBC, enc_message[:16])
    dec_message = aes.decrypt(enc_message[16:])

    write_file("/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab02/decrypted_image_santiago.jpeg", dec_message)
