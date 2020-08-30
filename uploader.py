import hashlib
import mss.tools
import redis

import sys
import time

from datetime import datetime
from pytz import timezone
from pytz import utc
from slack import WebClient

from settings import CAPTURE_WIDTH
from settings import CAPTURE_HEIGHT
from settings import CAPTURE_LEFT
from settings import CAPTURE_TOP
from settings import CAPTURE_FILEPATH
from settings import SLACK_CHANNELS
from settings import SLACK_FILE_TITLE
from settings import SLACK_TOKEN


def capture_image(top, left, width, height):
    """이미지를 캡쳐한다.

    Returns:
        스크린샷(mss.ScreenShot)
    """
    with mss.mss() as sct:
        return sct.grab({
            'top': top,
            'left': left,
            'width': width,
            'height': height,
        })


def hash_exists(hash_value):
    """해시값이 DB에 이미 있는 값인지 확인한다."""
    r = redis.Redis(host='localhost', port=6379, db=0)

    if r.get(hash_value):
        print('이미 동일한 해시가 존재합니다.')
        return True
    else:
        print('새로운 해시값이 입력되었습니다. 새로운 해시값을 저장합니다.')
        r.set(hash_value, 'dummy')
        return False


def save_image(screenshot, output=None):
    """스크린샷을 이미지 파일로 저장한다."""
    if output is None:
        now = datetime.utcnow()
        kst = timezone('Asia/Seoul')
        utc.localize(now).astimezone(kst)
        output = './screenshot-{}.png'.format(now.strftime('%y-%m-%d-%H-%M-%S'))

    mss.tools.to_png(screenshot.rgb, screenshot.size, output=output)
    return output


def slack_upload_file(filepath):
    sys.path.insert(1, './python-slackclient')
    client = WebClient(token=SLACK_TOKEN)
    client.files_upload(
        channels=SLACK_CHANNELS,
        file=filepath,
        title=SLACK_FILE_TITLE,
    )


if __name__ == '__main__':
    while True:
        image = capture_image(
            top=CAPTURE_TOP,
            left=CAPTURE_LEFT,
            width=CAPTURE_WIDTH,
            height=CAPTURE_HEIGHT,
        )
        enc = hashlib.md5()
        enc.update(image.rgb)
        hashed = enc.hexdigest()

        if not hash_exists(hashed):
            # 이미지를 저장한다.
            output_filepath = save_image(image, CAPTURE_FILEPATH)

            # 이미지를 슬랙으로 전송한다.
            slack_upload_file(output_filepath)

        time.sleep(2)
