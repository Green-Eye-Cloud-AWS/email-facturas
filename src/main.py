import boto3 # type: ignore
from email.header import decode_header
from email import message_from_string
from dotenv import load_dotenv
import dropbox
import os

load_dotenv()

dbox_token = os.getenv('DBOX')
to_folder = os.getenv('TO_FOLDER')

dbox = dropbox.Dropbox(dbox_token)


def existe_en_dbox(path):

    try:
        dbox.files_get_metadata(str(path))
        return True
    except:
        return False


def process(contents):

    message = message_from_string(contents)

    subject, encoding = decode_header(message['subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
    print(subject)
    
    if not message.is_multipart():
        print('Message is not multipart!')
        return
    
    for part in message.walk():
        if part.get_content_disposition() != 'attachment':
            continue
        
        filename = part.get_filename()

        filename, encoding = decode_header(filename)[0]
        if isinstance(filename, bytes):
            filename = filename.decode(encoding)

        if filename is None:
            continue

        print(filename)
        
        filename_lst = filename.split('.')

        path = str(to_folder + '/' + filename)
        
        i = 1
        while existe_en_dbox(path):
            path = str(to_folder + '/' + filename_lst[0] + '_' + str(i) + '.' + filename_lst[1])
            i += 1

        data = part.get_payload(decode=True)       

        dbox.files_upload(data, path, mode=dropbox.files.WriteMode('add'))   

    print('SES Email received and processed!')


def lambda_handler(event, context):
   
    s3 = boto3.client('s3')
    
    data = s3.get_object(Bucket=event['Records'][0]['s3']['bucket']['name'], Key=event['Records'][0]['s3']['object']['key'])
    contents = data['Body'].read().decode('utf-8')

    process(contents)
    

if __name__ == '__main__':

    with open(r'E:\HUB\cloud\email-facturas\test\7mna7gcl8io4c7a62j7f4q293ftbikl43vrmamo1', 'rb') as f:
        contents = f.read().decode('utf-8')

    process(contents)