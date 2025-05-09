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
        logging.warning(f"string diproses: {string_datamasuk}")
        
        # For upload command, we need to handle it differently because it contains base64 content
        if string_datamasuk.lower().startswith('upload '):
            # Extract the command, filename, and file content
            parts = string_datamasuk.split(' ', 2)  # Split only on first two spaces
            if len(parts) != 3:
                return json.dumps(dict(status='ERROR', data='Format UPLOAD tidak sesuai'))
                
            c_request = parts[0].lower().strip()
            filename = parts[1].strip()
            file_content = parts[2].strip()
            
            params = [filename, file_content]
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)
        else:
            # For other commands, use the standard shlex.split
            try:
                c = shlex.split(string_datamasuk.lower())
                c_request = c[0].strip()
                logging.warning(f"memproses request: {c_request}")
                params = [x for x in c[1:]]
                cl = getattr(self.file, c_request)(params)
                return json.dumps(cl)
            except Exception:
                return json.dumps(dict(status='ERROR', data='request tidak dikenali'))

if __name__=='__main__':
    #contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))
