
import dbm
import json
import os
from typing import Mapping
from flask import request
from pkg import server

def getFileExtension(filename):
    if '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()

ALLOWED_EXTENSIONS = {'csv', '.accdb'}

@server.route('/upload', methods=['POST'])
def uploadFiles():
    mappings = request.form.get('mapping')
    if mappings is None:
        return "400"
    mappings:dict = json.loads(mappings)
    
    for file in request.files.getlist('file'):
        if file is None:
            return "400"
        
        if getFileExtension(file.filename) not in ALLOWED_EXTENSIONS:
            return "400"
        
       

        mapping = mappings[file.filename]
        filePath = os.path.join(os.getcwd(), 'core', 'storage', 'uploads', file.filename)
        file.save(filePath)

        m = Mapping(dbm)
        try:
            m.ProcessCsv(filePath,mapping)
        except Exception as e:
            return str(e)
        finally:
            os.remove(filePath)

    return "200"

