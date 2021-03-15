from base64 import b64encode
import json
import requests


class HttpClient:
    def __init__(self,
                 api: str,
                 apikey: str):
        self.api = api
        self.apikey = apikey

    def main_entry(self,
                   public_id: str,
                   tag: int,
                   frame: str ,
                   latitude: float = None,
                   longitude: float = None,
                   height: float = None):
        timeout = 10
        if(frame == str()):
            frame = str()
        else:
            frame = frame
        params = {
            'public_id': public_id,
            'tag': tag,
            'frame': frame,
            'latitude': latitude,
            'longitude': longitude,
            'height': height,
        }
        print(f'Post body sent to server: {json.dumps(params)}')
        try:
            resp = requests.post(
                url=self.api,
                json=params,
                headers={
                    'x-api-key': self.apikey
                },
                timeout=timeout
            )
            content = resp.content and resp.content.decode()
            status_code = resp.status_code
            if 200 <= status_code < 300:
                print(f'Response received from server: {content}')
                return json.loads(content)
            else:
                print(f'Bad response: {status_code}: {content}')
        except Exception:
            print(f'Request timeout')
        return None






