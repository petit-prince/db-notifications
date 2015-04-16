import subprocess
import unittest
import time
import requests
import smtplib


class TestMailDump(unittest.TestCase):
    process = None

    def setUp(self):
        self.process = subprocess.Popen(["maildump"])
        time.sleep(0.5)  # Start the server
        print self.process.pid

    def tearDown(self):
        self.process.kill()


class TestSendMail(TestMailDump):
    host = '127.0.0.1'
    http_port = '1080'
    smtp_port = '1025'  # TODO put in TestMailDump
    url = 'http://' + host + ':' + http_port

    def test_get_index(self):
        res = requests.get(self.url)
        self.assertEquals(200, res.status_code)

    def test_get_messages_empty(self):
        res = requests.get(self.url + '/messages/')
        self.assertEquals(200, res.status_code)
        json = res.json()
        self.assertEquals(0, len(json.get('messages')))

    def test_send_mail(self):
        mail = smtplib.SMTP(self.host, self.smtp_port)
        msg = 'test'
        mail.sendmail('sender@test.com', 'recipient@test.com', msg)
        res = requests.get(self.url + '/messages/')
        self.assertEquals(200, res.status_code)
        json = res.json()
        self.assertEquals(1, len(json.get('messages')))

if __name__ == '__main__':
    unittest.main()