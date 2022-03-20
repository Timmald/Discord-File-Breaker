import json
import sqlite3


def get_db_connection():
    return sqlite3.connect('filePieces.sqlite')


with open('filePieces.json', 'r') as json_reader:
    filePieces = json.load(json_reader)
testServerFiles = filePieces["Test"]
nickServerFiles = filePieces["Nick's"]
for file in testServerFiles:
    conn = get_db_connection()
    cur = conn.cursor()
    nameDate = file[0]
    name, date = nameDate.split('; Uploaded at ')
    numPieces = file[1]
    conn.execute(f'INSERT INTO Test_Server_Files (file_name, upload_time, num_pieces) VALUES (?, ?, ?)', (name, date, numPieces))
    conn.commit()
    conn.close()
for file in nickServerFiles:
    conn = get_db_connection()
    cur = conn.cursor()
    nameDate = file[0]
    name, date = nameDate.split('; Uploaded at ')
    numPieces = file[1]
    conn.execute(f'INSERT INTO "Nick\'s_Server_Files" (file_name, upload_time, num_pieces) VALUES (?, ?, ?)', (name, date, numPieces))
    conn.commit()
    conn.close()
