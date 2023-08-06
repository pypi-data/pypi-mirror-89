import queue
import textwrap
import threading
import time
import urllib.parse
import pychromecast

def create_notify_url(text: str, lang: str, ttsspeed: float):
    payload = {
            "ie": "UTF-8",
            "q": text,
            "tl": lang,
            "total": 1,
            "idx": 0,
            "textlen": len(text),
            "client": "tw-ob",
            "prev": "input",
            "ttsspeed" : ttsspeed
            }
    params = urllib.parse.urlencode(payload, quote_via = urllib.parse.quote)
    url = "https://translate.google.com/translate_tts?{}".format(params)
    return url


def split_text(text: str, lang: str):
    max_split_text_len = 200
    return textwrap.wrap(text, width = max_split_text_len)


class GoogleHome(pychromecast.Chromecast):
    def __init__(self, host, port = None, device = None):
        self.thread = None
        self.mp3_url_queue = queue.Queue()
        super().__init__(host, port, device)

    def _play_mp3(self, timeout: int):
        if self.mp3_url_queue.empty():
            self.thread = None
            return

        url = self.mp3_url_queue.get()
        self.media_controller.play_media(url, "audio/mp3")
        # wait start playing
        time.sleep(1)
        self._block_while_playing_queue(timeout)

        # play next mp3
        self._play_mp3(timeout)

    def _block_while_playing_queue(self, timeout: int):
        self.media_controller.block_until_active()
        t1 = time.time()
        while True:
            status = self.media_controller.status
            player_state = status.player_state
            if player_state != "PLAYING":
                break
            if timeout > 0:
                t2 = time.time()
                if t2 - t1 >= timeout:
                    break
            time.sleep(0.5)

    def notify(self, text: str, lang: str = "en", ttsspeed: float = 1.0, timeout: int = 0):
        for line in split_text(text, lang):
            url = create_notify_url(line, lang, ttsspeed)
            self.mp3_url_queue.put(url)

        if self.thread == None:
            self.thread = threading.Thread(target = self._play_mp3, args = ([timeout]))
            self.thread.start()

    def play(self, url: str, timeout: int = 0):
        if url != None:
            self.mp3_url_queue.put(url)

        if self.thread == None:
            self.thread = threading.Thread(target = self._play_mp3, args = ([timeout]))
            self.thread.start()

    def pause(self):
        self.media_controller.pause()

    def resume(self):
        self.media_controller.play()

    def block_while_playing(self, timeout: int = 0):
        t1 = time.time()
        while not self.mp3_url_queue.empty():
            if timeout > 0:
                t2 = time.time()
                elapsed_t = t2 - t1
                if elapsed_t >= timeout:
                    break
            else:
                pass
        if self.thread != None:
            self.thread.join()

    def is_playing(self):
        if not self.mp3_url_queue.empty():
            return True
        if self.thread != None:
            return self.thread.is_alive()
        return False

def get_googlehomes(
    friendly_name = None,
    ipaddr = None,
    uuid = None,
    tries = None,
    retry_wait = None,
    timeout = None
):
    if ipaddr != None:
        # get from ipaddress
        googlehome = GoogleHome(ipaddr)
        # check friendly_name and uuid
        if friendly_name != None and googlehome.name != friendly_name:
            return []
        if uuid != None and str(googlehome.uuid) != uuid:
            return []
        return [googlehome]

    ccs, browser = pychromecast.get_chromecasts(tries, retry_wait, timeout)
    googlehomes = []
    for cc in ccs:
        # check friendly_name and uuid
        if friendly_name != None and cc.name != friendly_name:
            return []
        if uuid != None and str(cc.uuid) != uuid:
            return []
        cc.wait()
        googlehome = GoogleHome(
                host = cc.socket_client.host,
                port = cc.socket_client.port,
                device = cc.device,
                )
        googlehomes.append(googlehome)

    return googlehomes

