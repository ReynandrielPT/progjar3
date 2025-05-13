import socket
import json
import base64
import logging
import os

server_address = ('0.0.0.0', 8889)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning("sending message")
        sock.sendall(command_str.encode())
        sock.sendall(b"\r\n")

        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break

        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving")
        return False
      
def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {hasil['data_namafile']} berhasil didownload")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    if not os.path.exists(filename):
        print(f"File {filename} tidak ditemukan")
        return False

    try:
        with open(filename, 'rb') as fp:
            isifile = base64.b64encode(fp.read()).decode()
        base_filename = os.path.basename(filename)
        command_str = f"UPLOAD {base_filename} {isifile}"
        hasil = send_command(command_str)
        if (hasil['status']=='OK'):
            print(f"File {hasil['data_namafile']} berhasil diupload")
            return True
        else:
            print("Gagal")
            return False
    except Exception as e:
        print(f"Gagal upload")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"File {hasil['data_namafile']} berhasil didelete")
        return True
    else:
        print("Gagal")
        return False

if __name__ == '__main__':
    server_address = ('172.16.16.101', 8889)
    remote_list()
    remote_get('donalbebek.jpg')
    remote_upload('/home/jovyan/work/tugas3/progjar3/files/pok123.jpg')
    remote_delete('pokijan.jpg')
