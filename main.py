import datetime
import random
import hashlib
import base64
import datetime
import requests
from chardet.universaldetector import UniversalDetector



username = 'アカウント名'
api_key  = 'API鍵'
blogname = 'xxxx.hatenablog.com'
author = 'ミナピピン(https://tkstock.site/)'

title = 'test'
post_data = '<h2>test</h2><p>テスト投稿です</p>'

def main(title, post_data, draft_flg=True):
    if draft_flg:
        draft_yn = 'yes'
    else:
        draft_yn = 'no'
    tdatetime = datetime.datetime.now()
    tstr = tdatetime.strftime('%Y/%m/%d')
    data = create_data(title, post_data, tstr, draft_yn)
    post_hatena(data)

def wsse(username, api_key):
    created = datetime.datetime.now().isoformat() + "Z"
    b_nonce = hashlib.sha1(str(random.random()).encode()).digest()
    b_digest = hashlib.sha1(b_nonce + created.encode() + api_key.encode()).digest()
    c = 'UsernameToken Username="{0}", PasswordDigest="{1}", Nonce="{2}", Created="{3}"'
    return c.format(username, base64.b64encode(b_digest).decode(), base64.b64encode(b_nonce).decode(), created)

def create_data(title,body, tstr, draft_yn):
    
    template = """<?xml version="1.0" encoding="utf-8"?>
    <entry xmlns="http://www.w3.org/2005/Atom"
           xmlns:app="http://www.w3.org/2007/app">
      <title>{0}</title>
      <author><name>{1}</name></author>
      <content type="text/plain">{2}</content>
      <updated>{3}</updated>
      <app:control>
        <app:draft>{4}</app:draft>
      </app:control>
    </entry>
    """
    data = template.format(title,author, body, tstr, draft_yn).encode()
    return data

def parse_ｔext(file, charset):
    with open(file, encoding=charset) as f:
        obj = f.readlines()
        title = ""
        body  = ""
        for i, line in enumerate(obj):
            if i == 0:
                title = line
            else:
                body = body + line
    return title, body

def check_encoding(file):
    detector = UniversalDetector()
    with open(file, mode='rb') as f:
        for binary in f:
            detector.feed(binary)
            if detector.done:
                break
    detector.close()
    charset = detector.result['encoding']
    return charset

def post_hatena(data):
    headers = {'X-WSSE': wsse(username, api_key)}
    url = 'http://blog.hatena.ne.jp/{0}/{1}/atom/entry'.format(username, blogname)
    r = requests.post(url, data=data, headers=headers)
    if r.status_code != 201:
        sys.stderr.write('Error!\n' + 'status_code: ' + str(r.status_code) + '\n' + 'message: ' + r.text)


main(title, post_data, False)
print('投稿完了しました')
