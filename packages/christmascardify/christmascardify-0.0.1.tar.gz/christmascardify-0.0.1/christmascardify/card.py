from tools import cardCreate
from PIL import Image
import os

FILE_PATH = os.path.dirname(__file__)
FONT_PATH = os.environ.get('FONT_PATH', os.path.join(FILE_PATH, 'Brusher.ttf'))
BG_PATH = os.environ.get('BG_PATH', os.path.join(FILE_PATH, 'defaultbg.png'))

class cardmaker():
    def __init__(self, lastName, toWhom, photoPath, savePath='./', style=1, photoType='sketch',
                 fontPath = None, bgPath = None):
        self.style = style
        self.lastName = lastName
        self.photoPath = photoPath
        self.photoType = photoType
        self.toWhom = toWhom
        self.savePath = savePath

        self.fontPath = FONT_PATH if not fontPath else fontPath
        self.bgPath = BG_PATH if not bgPath else bgPath
        if not isinstance(toWhom, list):
            raise TypeError('Errno1 Parameter "toWhom" must be a list')

    def create(self):
        for name in self.toWhom:
            card = cardCreate(self.lastName, name, self.photoPath, self.style, self.photoType, self.fontPath, self.bgPath)
            card.save(self.savePath+name+'.png')


a = cardmaker('Prabhu', ['Rahul', 'Friend'], './christmascardify/pexels-rodnae-productions-6115401.jpg')
a.create()