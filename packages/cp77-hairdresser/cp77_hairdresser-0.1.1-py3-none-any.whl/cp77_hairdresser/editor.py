import argparse
from binascii import hexlify, unhexlify
import os
from datetime import datetime
from shutil import copyfile
import random
import json

from .json2obj import Json2Obj

class Core:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'hairstyles.json')) as f:
            self.styles = Json2Obj(json.load(f)).styles
            for style in self.styles:
                style.code = hexlify(unhexlify(style.code))
        self.auto_backup = True
        self.hexdata = None
        self.path = None
        self._hairstyle_idx = None

    @property
    def data_idx(self):
        if self._hairstyle_idx is None:
            self.current_hairstyle()
        return self._hairstyle_idx

    def load(self, path):
        if not os.path.exists(path):
            raise FileExistsError('Save file does not exist on provided location.')
        self.path = path
        with open(path, 'rb') as f:
            self.hexdata = hexlify(f.read())
        return True

    def save(self):
        hexdata = unhexlify(self.hexdata)
        if self.auto_backup:
            self.backup(self.path)
        with open(self.path, 'wb') as f:
            f.write(hexdata)

    @staticmethod
    def backup(f):
        fdir = os.path.dirname(f)
        fname = os.path.basename(f)
        copyfile(
            f,
            os.path.join(
                fdir, datetime.now().strftime('%Y%m%d_%H_%M_%S_sav.dat')
            )
        )

    def current_hairstyle(self):
        for style in self.styles:
            match = self.hexdata.find(style.code)
            if match >= 0:
                self._hairstyle_idx = match
                return style
        if match < 0:
            return None

    def apply(self, new_style):
        self.hexdata = self.hexdata[:self.data_idx] + new_style.code + self.hexdata[self.data_idx+16::]

    def get_hairstyle(self, id):
        return [style for style in self.styles if style.id == id][0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='savefile',
        help='Fill this field if you want custom export/import directory for .dxf file. Default is ...project/products/lidar/las/mva.dxf')
    parser.add_argument('-n', '--haircut_number', dest='haircut', type=int,
        help='Haircut number (see readme)')
    parser.add_argument('-b', '--no_backup', dest='backup', action='store_false',
        help='Provide -b switch to disable auto backup.')
    args, unknown = parser.parse_known_args()

    #args.haircut = random.randrange(15)

    core = Core()
    core.auto_backup = args.backup
    core.load(args.savefile)
    print('Old hairstyle:', core.current_hairstyle().id)
    if core.current_hairstyle().id != args.haircut:
        core.apply(core.get_hairstyle(args.haircut))
        core.save()
        print('New hairstyle:', core.current_hairstyle().id)
    else:
        print('Same haircut selected - no change.')
