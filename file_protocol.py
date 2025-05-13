import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
    def proses_string(self, string_datamasuk=''):
        logging.warning(f"String diterima: {string_datamasuk}")
        c = shlex.split(string_datamasuk.lower())

        try:
            c_request = c[0].strip()
            logging.warning(f"memproses request: {c_request}")
            params = [x for x in c[1:]]

            if c_request == 'upload':
                if len(params) < 2:
                    return json.dumps(dict(status='ERROR', data='Format UPLOAD tidak sesuai'))

                filename = params[0]
                file_content = ' '.join(params[1:])  # Jika base64 mengandung spasi

                logging.warning(f"Proses upload file: {filename}, ukuran konten: {len(file_content)} karakter")

                c1 = self.file.upload([filename, file_content])
                return json.dumps(c1)

            elif c_request in ['list', 'get', 'delete']:
                c1 = getattr(self.file, c_request)(params)
                return json.dumps(c1)

        except Exception as e:
            logging.error(f"Terjadi kesalahan saat memproses: {str(e)}")
            return json.dumps(dict(status='ERROR', data=str(e)))


if __name__ == '__main__':
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))



