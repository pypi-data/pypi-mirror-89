import os
import io
import logging
import time
from textcli.spider import Spider
import socketio
    
class Textcli:

    def __init__(self, url_key, token, live_update, isWatch):

        self.sio = socketio.Client()

        self.url_key = url_key
        self.token = token
        self.domain = "https://api.rqn9.com/data/1.0/textvn/"
        self.spider = Spider(self.url_key, self.token)
        self.pad_key = self.spider.pad_key

        self.content = self.spider.content
        self.haspw = self.spider.hspass
        self.isWatch = isWatch

        self.filepath = ''
        self.file_stamp = 0
        self.socket_url = 'https://live.textvn.com'

        self.io = None
        
        if live_update:
            self.sio.connect('https://live.textvn.com:443', namespaces=['/'])
            self.join_room()
            #self.current_hash = self.spider.detech_change()
            #self.update_tab()

    def join_room(self):
        self.sio.sleep(1)
        self.sio.emit('join_room', self.url_key, namespace='/')

    def publish(self, content):

        text_data = dict()

        text_data['name'] = self.url_key
        text_data['text'] = content
        text_data['cursor_location'] = len(content)

        self.sio.emit('editing', text_data, namespace='/')

        if self.isWatch is False:
            self.sio.sleep(0.5)
            self.sio.disconnect();

    def update_tab(self):
        # Todo
        while 1:
            if self.spider.detech_change() == self.current_hash:
                pass
            elif self.spider.detech_change() == False:
                print("Something wrong!")
                break
            else:
                self.current_hash = self.spider.detech_change()
                break
            time.sleep(5)

    def get_file_content(self, file_path):

        content = ''

        with io.open(file_path, mode="r", encoding="utf-8") as f:
            content = f.read()

        return content


    def check_file_change(self):

        new_file_stamp = os.stat(self.filepath).st_mtime

        if(new_file_stamp != self.file_stamp):
            return True
        return False


    def save_to_file(self, filename, overwrite):
        

        with io.open(filename, mode="w", encoding="utf-8") as f:
            if self.content is None:
                content = f.write("")
            else:
                content = f.write(self.content)

        return


    def save_file(self, filepath, overwrite):

        file_content = self.get_file_content(filepath)

        self.filepath = filepath
        self.file_stamp = os.stat(filepath).st_mtime

        self.content = ''
        if overwrite and file_content is not None:
            self.content = file_content
        elif file_content is not None:
            self.content += file_content
        else:
            self.content = ''

        if self.sio:
            self.publish(self.content)

        self.spider.save(self.content)

        return

    def view_file(self):
        return self.content
