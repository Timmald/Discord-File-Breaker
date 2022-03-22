import json
import sqlite3


def get_db_connection():
    return sqlite3.connect('filePieces.sqlite')


conn = get_db_connection()
conn.row_factory = sqlite3.Row
filePieces = conn.execute('SELECT * FROM File_Pieces').fetchall()
for entry in range(filePieces):
    conn.execute('UPDATE File_Pieces SET file_name = ? WHERE id = ?', (entry['file_name'].replace(' ', '_'), entry['id']))
    conn.commit()
conn.close()

# with open('filePieces.json', 'r') as json_reader:
#     filePieces = json.load(json_reader)
#
# filePiecesSum = filePieces["Test"] + filePieces["Nick's"]
# conn = get_db_connection()
# conn.execute(
#     'CREATE TABLE File_Pieces (file_name text, upload_time text, num_pieces int, server_name text, id integer primary key autoincrement)')
# for file in filePiecesSum:
#     isNicks = filePiecesSum.index(file) >= len(filePieces["Test"])
#     serverName = "Nick's" if isNicks else "Test"
#     nameDate = file[0]
#     name, date = nameDate.split('; Uploaded at ')
#     numPieces = file[1]
#     conn.execute(f'INSERT INTO File_Pieces (file_name, upload_time, num_pieces, server_name) VALUES (?, ?, ?, ?)',
#                  (name, date, numPieces, serverName))
# conn.commit()
# conn.close()
# for file in testServerFiles:
#    conn = get_db_connection()
#    cur = conn.cursor()
#    nameDate = file[0]
#    name, date = nameDate.split('; Uploaded at ')
#    numPieces = file[1]
#    conn.execute(f'INSERT INTO Test_Server_Files (file_name, upload_time, num_pieces) VALUES (?, ?, ?)', (name, date, numPieces))
#    conn.commit()
#    conn.close()
# for file in nickServerFiles:
#    conn = get_db_connection()
#    cur = conn.cursor()
#    nameDate = file[0]
#    name, date = nameDate.split('; Uploaded at ')
#    numPieces = file[1]
#    conn.execute(f'INSERT INTO "Nick\'s_Server_Files" (file_name, upload_time, num_pieces) VALUES (?, ?, ?)', (name, date, numPieces))
#    conn.commit()
#    conn.close()
# TODO: Make all filenames have underscores
# TODO: remove piece_num
