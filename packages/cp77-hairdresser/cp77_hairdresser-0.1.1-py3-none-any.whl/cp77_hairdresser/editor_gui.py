import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
#from ui import resource
from .editor import Core

class HaircutDialog(QDialog):
    def __init__(self,):
        QDialog.__init__(self)

        self.core = Core()
        self.preload_images()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'editor.ui'), self)

        self._gender = None
        self.pix_current = None
        self.pix_new = None

        self.ui.cb_gender.currentTextChanged.connect(self.set_gender)

        self.ui.pb_open.clicked.connect(self.open_file)
        self.ui.cb_backup.stateChanged.connect(self._update_auto_backup_state)

        for style in self.core.styles:
            self.ui.cb_style.addItem(
                'Hairstyle {:02d}'.format(
                    style.id
                ),
                style
            )
        self.ui.cb_style.currentIndexChanged.connect(
            lambda x: self.update_new()
        )

        self.ui.pb_apply.clicked.connect(self.apply_and_save)
        self.ui.pb_refresh.clicked.connect(self.reload_file)

    def apply_and_save(self):
        if self.core.hexdata:
            try:
                self.core.apply(self.ui.cb_style.currentData())
                self.core.save()
                self.ui.lbl_status.setText('Save File stored successfully!')
            except Exception as e:
                print(str(e))
            self.reload_file()

    def reload_file(self):
        if self.core.path:
            try:
                self.core.load(self.core.path)
                self.update_current()
            except Exception as e:
                self.ui.lbl_status.setText(str(e))
            self.redraw()

    def _update_auto_backup_state(self, b):
        self.core.auto_backup = self.ui.cb_backup.isChecked()
        self.ui.lbl_status.setText('Auto backup {}!'.format(
            'enabled' if self.core.auto_backup else 'disabled'
        ))

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(filter="Save Game Files (*.dat)")
        if file:
            try:
                self.core.load(file)
                self.ui.lbl_status.setText('Opened file {}'.format(file))
                self.update_current()
            except Exception as e:
                self.ui.lbl_status.setText(str(e))

    @property
    def gender(self):
        if self._gender is None:
            self.set_gender(self.ui.cb_gender.currentText())
        return self._gender

    def set_gender(self, gender):
        self._gender = gender
        self.update_current()
        self.update_new()

    def update_current(self):
        if self.core.hexdata:
            cur = self.core.current_hairstyle()
            self.pix_current = getattr(cur.resource, self.gender)
            self.redraw()

    def update_new(self):
        cur = self.ui.cb_style.currentData()
        self.pix_new = getattr(cur.resource, self.gender)
        self.redraw()

    def redraw(self):
        if self.pix_current:
            self.ui.img_current.setPixmap(
                self.pix_current.scaledToWidth(
                    self.ui.img_current.width()-2,
            ))
        if self.pix_new:
            self.ui.img_new.setPixmap(
                self.pix_new.scaledToWidth(
                    self.ui.img_new.width()-2,
            ))

    def resizeEvent(self, QResizeEvent):
        self.redraw()

    def preload_images(self):
        class Resource:
            def __init__(self):
                self.female = None
                self.male = None
        dirname = os.path.dirname(__file__)
        for style in self.core.styles:
            resource_path = os.path.join(
                dirname,
                'ui', 'images'
            )
            resource = Resource()
            resource.female = QPixmap(os.path.join(
                resource_path,
                'female',
                'female{:02d}.png'.format(style.id)
            ))
            resource.male = QPixmap(os.path.join(
                resource_path,
                'male',
                'male{:02d}.png'.format(style.id)
            ))
            setattr(style, 'resource', resource)

    @staticmethod
    def show_dialog():
        linker_core = None

        dlg = HaircutDialog()
        dlg.show()
        result = dlg.exec_()
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    HaircutDialog.show_dialog()
    exit()