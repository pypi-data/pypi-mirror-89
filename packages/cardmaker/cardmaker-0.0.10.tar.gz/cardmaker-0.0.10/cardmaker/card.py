import os
from .tools import cardCreate
from sketchify import sketch

FILE_PATH = os.path.dirname(__file__)
FONT_PATH = os.environ.get('FONT_PATH', os.path.join(FILE_PATH, 'Brusher.ttf'))
BG_PATH = os.environ.get('BG_PATH', os.path.join(FILE_PATH, 'defaultbg.png'))

class cardmaker():
    def __init__(self, lastName, toWhom, photoPath, savePath='./', style=1, photoType='normal', fontPath = None,
                 bgPath = None, fontColorOpening='#ffffff', fontColorMessage='#ffffff',
                 customOpening='Merry Christmas!', customMessage=None):
        self.style = style
        self.lastName = lastName
        self.photoPath = photoPath
        self.photoType = photoType
        self.toWhom = toWhom
        self.savePath = savePath
        self.fontColorOpening = fontColorOpening
        self.fontColorMessage = fontColorMessage
        self.customMessage = customMessage
        self.customOpening = customOpening

        self.fontPath = FONT_PATH if not fontPath else fontPath
        self.bgPath = BG_PATH if not bgPath else bgPath
        if not isinstance(toWhom, list):
            raise TypeError('Errno1 Parameter "toWhom" must be a list')

    def create(self):
        if self.photoType == 'sketch':
            sketch.normalsketch(self.photoPath, self.savePath, 'image')
            self.photoPath = self.savePath+'image.png'
        for name in self.toWhom:
            card = cardCreate(self.lastName, name, self.photoPath, self.style, self.fontPath, self.bgPath,
                              self.fontColorOpening, self.fontColorMessage, self.customOpening, self.customMessage)
            card.save(self.savePath+name+'.png')
