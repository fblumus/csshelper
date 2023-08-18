import json
import sys
import tempfile
import subprocess
import extract_msg
import os
import re


def extract_mail_header_info(msg):
    headers = msg.header

    result = {
        'from': headers.get('from', None),
        'to': headers.get('to', None),
        'cc': headers.get('cc', None),
        'bcc': headers.get('bcc', None),
        'subject': headers.get('subject', None),
        'date': msg.date,
        'message_id': headers.get('message-id', None),
        'received': headers.get('received', []),
        'content_type': headers.get('content-type', None),
        'mime_version': headers.get('mime-version', None),
        'reply-to': headers.get('reply-to', None),
        'in-reply-to': headers.get('in-reply-to', None),
        'references': headers.get('references', None),
        'x-mailer': headers.get('x-mailer', None),
        'x-originating-ip': headers.get('x-originating-ip', None),
        'x-priority': headers.get('x-priority', None),
        'dkim-signature': headers.get('dkim-signature', None),
        'x-spam-status': headers.get('x-spam-status', None),
        'x-spam-score': headers.get('x-spam-score', None),
        'return-path': headers.get('return-path', None),
        'sender': headers.get('sender', None),
        'x-received': headers.get('x-received', None),
        'Authentication-Results': headers.get("Authentication-Results", None),
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Bitte geben Sie den Pfad zur .msg-Datei an.")
        return

    file_path = sys.argv[1]
    msg = extract_msg.Message(file_path)
    data = extract_mail_header_info(msg)
    subject_folder = re.sub(r'[^\w\-_]', '_', data['subject']) if data['subject'] else "Unknown_Subject"

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp:
        tmp.write("===== Header =====\n")
        tmp.write(json.dumps(data, indent=4))
        tmp.write("\n\n===== Body =====\n")
        tmp.write(msg.body)

        if msg.attachments:
            tmp.write("\n\n===== Attachments =====\n")

            attachments_path = os.path.join(os.getcwd(), f"Attachments_{subject_folder}")
            if not os.path.exists(attachments_path):
                os.makedirs(attachments_path)

            for attachment in msg.attachments:
                attachment_filename = attachment.longFilename or attachment.shortFilename
                tmp.write(f"- {attachment_filename}\n")

                attachment_path = os.path.join(attachments_path, attachment_filename)
                with open(attachment_path, 'wb') as file:
                    file.write(attachment.data)

    subprocess.Popen(["xdg-open", tmp.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()
