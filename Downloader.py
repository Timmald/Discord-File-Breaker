import json
import os
import ssl

from installCerts import installCerts
import discord
import sys
from datetime import datetime, timezone

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return os.path.join(os.path.dirname(sys.argv[0]),relative_path)


client = discord.Client()
command = sys.argv[1]
userName=os.path.normpath(sys.argv[0]).split(os.path.sep)[2]
with open(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json', 'r') as json_file:
    userInfo = json.load(json_file)

@client.event
async def on_ready():
    print('yo')
    if command == 'query':
        botChannel = await client.fetch_channel(userInfo["botChannel"])
        await botChannel.send('$downloadList')
    if command == 'download':
        print("yo")
        botChannel = await client.fetch_channel(userInfo["botChannel"])
        fileName=sys.argv[2]
        pieceNum=int(sys.argv[3])
        fileData=fileName.split(';_Uploaded_at_')
        fileData[1]=datetime.strptime(fileData[1].replace('_',' '), '%c').astimezone(timezone.utc)
        pieceNames=[f'{fileData[0]} piece {i}.txt'.replace(' ','_') for i in range(1,pieceNum+1)]
        print(f'now is {datetime.now().strftime("%c")} in UTC')
        print(f'code thinks it is {fileData[1].strftime("%c")}')
        async for message in botChannel.history(around=fileData[1]):
            if len(message.attachments)==1:
                print("one attachment")
                print(pieceNames)
                print(message.attachments[0].filename)
                if message.attachments[0].filename in pieceNames:
                    print("has a target name")
                    if not os.path.exists(f'{userInfo["downloadsFolder"]}/Discord File Pieces'):
                        print("making directory")
                        os.mkdir(f'{userInfo["downloadsFolder"]}/Discord File Pieces')
                    await message.attachments[0].save(f'{userInfo["downloadsFolder"]}/Discord File Pieces/{message.attachments[0].filename}')
                    print(f'saved {message.attachments[0].filename}')
        sys.exit()



@client.event
async def on_message(message):
    if message.author.id==937444289208778782:
        downloadChoices=message.content
        currentChoicesPath = f'/Users/{userName}/Library/Application Support/FileBreakerApp/currentChoices.json'
        with open(currentChoicesPath,'w') as json_file:
            json.dump(json.loads(downloadChoices),json_file,indent=0)

        sys.exit()

#TODO: put the below line in a try block, then except the ClientConnectorCertificateError and if you catch it run installCertificates.command and then run the bot
try:
    client.run('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
except ssl.SSLCertVerificationError:
    os.system('/Applications/Python\ 3.8/Install\ Certificates.command')
    sys.exit(4)