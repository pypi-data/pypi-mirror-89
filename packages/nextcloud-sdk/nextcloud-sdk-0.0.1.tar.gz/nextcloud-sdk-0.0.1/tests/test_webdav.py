from webdav.basic import Basic
import unittest

class TestWebDAVMethods(unittest.TestCase):
    def test_list(self):
        b = Basic(host='https://pan.ynunique.com:543', username='ynqz', password='qq446162')
        # print(b.list(username='ynqz'))
        # filecontent = b.download(path_to_file='/remote.php/dav/files/ynqz/Reasons%20to%20use%20Nextcloud.pdf')
        # file = open('./exmaple.pdf', 'wb')
        # file.write(filecontent.read())
        filebytes = open('exmaple.pdf', 'rb')
        resp = b.upload(filebytes, 'ynqz', '/Empty/test.pdf')
        print(resp)
        filebytes.close()

if __name__ == "__main__":
    unittest.main()