from cudatext import *
from cudatext_cmd import *
import sys
import json
from urllib.request import urlopen
from urllib.parse import urlencode

URL_W3C = 'http://validator.w3.org/check'
URL_CSS = 'http://jigsaw.w3.org/css-validator/validator'

def do_validate(ed, format, validator_url):
    text = ed.get_text_all()
    params = {'fragment': text, 'parser': format, 'output': 'json'}
    encoded_params = urlencode(params).encode('utf-8')
    
    output = urlopen(validator_url, encoded_params).read()
    output = output.decode('utf-8')
    results = json.loads(output)

    app_log(LOG_SET_PANEL, LOG_PANEL_VALIDATE)
    app_log(LOG_CLEAR, '')

    if not results['messages']:
        msg_box('Document successfully checked as %s' % format, MB_OK+MB_ICONINFO)
        return

    app_log(LOG_SET_REGEX, r'Line (\d+):.+')
    app_log(LOG_SET_LINE_ID, '1')
    app_log(LOG_SET_NAME_ID, '0')
    app_log(LOG_SET_FILENAME, ed.get_filename())
    app_log(LOG_SET_ZEROBASE, '0') 
    
    app_log(LOG_ADD, 'Errors found while checking document as %s:' % format)
    app_log(LOG_ADD, '')
    for message in results['messages']:
        app_log(LOG_ADD, 'Line %s: %s' % (message['lastLine'], message['message']))
        
    ed.focus()
    ed.cmd(cmd_ShowPanelValidate)

class Command:
    def validate_html5(self):
        do_validate(ed, 'html5', URL_W3C)
    def validate_html4_strict(self):
        do_validate(ed, 'html4', URL_W3C)
    def validate_html4_tran(self):
        do_validate(ed, 'html4tr', URL_W3C)
