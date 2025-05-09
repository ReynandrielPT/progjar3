import os
import json
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.chdir('files/')
        
    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
            
    def get(self, params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}", 'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def upload(self, params=[]):
        try:
            filename = params[0]
            file_content = params[1]
            
            # Decode base64 content
            isifile = base64.b64decode(file_content)
            
            # Write the file
            fp = open(filename, 'wb+')
            fp.write(isifile)
            fp.close()
                
            return dict(status='OK', data_namafile=filename, data_file=file_content)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def delete(self, params=[]):
        try:
            filename = params[0]
            
            # Check if file exists
            if not os.path.exists(filename):
                return dict(status='ERROR', data=f'File {filename} tidak ditemukan')
                
            # Delete the file
            os.remove(filename)
            
            return dict(status='OK', data=f'File {filename} berhasil dihapus')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
