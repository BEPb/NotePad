"""
Python 3.9 программа консоли блокнота (текстовый редактор)
Название файла main.py

Version: 0.1
Author: Andrej Marinchenko
Date: 2022-04-16
"""
import sys, os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QAction,
    QPlainTextEdit,
    QToolBar,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence
from PyQt5.QtPrintSupport import QPrintDialog


class Notepad(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Notepad 2.0")
        self.screen_width, self.screen_height = (
            self.geometry().width(),
            self.geometry().height(),
        )
        self.resize(self.screen_width, self.screen_height)
        self.setWindowIcon(QIcon("images/notepad.png"))
        self.show()

        self.filterTypes = "Text Document (*.txt);; Python (*.py);; Markdown (*.md)"
        self.path = None

        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedFont.setPointSize(12)
        mainlayout = QVBoxLayout()

        # Editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixedFont)
        mainlayout.addWidget(self.editor)

        # statusBar
        self.statusBar = self.statusBar()

        # app container
        container = QWidget()
        container.setLayout(mainlayout)
        self.setCentralWidget(container)

        # File menus
        filemenu = self.menuBar().addMenu("&File")

        # Edit menu
        editmenu = self.menuBar().addMenu('&Edit')
        # file Toolbar
        file_toolbar = QToolBar()
        file_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)
        self.update_title()

        # Edit Toolbar
        edit_toolbar = QToolBar()
        edit_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)

        """
        Undo, Redo actions
        """
        undo_action = self.create_action(
            self,
            'images/undo.png',
            'Undo',
            'Undo',
            QKeySequence.Undo,
            self.editor.undo
        )
        redo_action = self.create_action(
            self,
            'images/redo.png',
            'Redo',
            'Redo',
            QKeySequence.Redo,
            self.editor.redo
        )
        # clear action
        clear = self.create_action(
            self,
            'images/clean.png',
            'Clear',
            'Clear',
            'ctrl+shift+c',
            self.editor.clear
        )
        editmenu.addActions([undo_action, redo_action, clear])
        edit_toolbar.addActions([undo_action,redo_action, clear])

        # cut, copy, paste, select all
        cut_action=self.create_action(
            self,
            'images/cut.png',
            'Cut',
            'Cut',
            QKeySequence.Cut,
            self.editor.cut
        )
        copy_action=self.create_action(
            self,
            'images/copy.png',
            'Copy',
            'Copy',
            QKeySequence.Copy,
            self.editor.copy
        )
        paste_action=self.create_action(
            self,
            'images/paste.png',
            'Paste',
            'Paste',
            QKeySequence.Paste,
            self.editor.paste
        )
        select_action=self.create_action(
            self,
            'images/selectall.png',
            'Select All',
            'Select All',
            QKeySequence.SelectAll,
            self.editor.selectAll
        )
        # Wrap text action
        wrap_action=self.create_action(
            self,
            'images/wrap.png',
            'Wrap Text',
            'Wrap Text',
            'ctrl+shift+W',
            lambda : self.editor.setLineWrapMode(not self.editor.lineWrapMode())
        )
        edit_toolbar.addActions([cut_action,copy_action,paste_action,select_action, wrap_action])
        editmenu.addActions([cut_action,copy_action,paste_action,select_action, wrap_action])

        
        """
        open, save, saveAs
        """
        file_open = self.create_action(
            self,
            "images/file_open1.png",
            "Open File",
            "Open File",
            QKeySequence.Open,
            self.file_open,
        )
        file_save = self.create_action(
            self,
            "images/file_save1.png",
            "Save",
            "Save File",
            QKeySequence.Save,
            self.file_save,
        )
        file_saveas = self.create_action(
            self,
            "images/file_saveas1.png",
            "Save As",
            "Save As",
            QKeySequence.SaveAs,
            self.file_saveas,
        )
        file_print = self.create_action(
            self,
            "images/file_print1.png",
            "Print File",
            "Print File",
            QKeySequence.Print,
            self.file_print,
        )
        filemenu.addActions([file_open, file_save, file_saveas, file_print])
        file_toolbar.addActions([file_open, file_save, file_saveas, file_print])
    def file_save(self):
        if self.path is None:
            self.file_saveas()
        else:
            try:
                text= self.editor.toPlainText()
                with open(self.path,'w') as f:
                    f.write(text)
                self.dialog_message(f'File saved succesfully at {self.path}', QMessageBox.Information)
            except Exception as e:
                self.dialog_message(e, QMessageBox.Critical)
            else:
                pass
    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            '',
            self.filterTypes
        )
        text= self.editor.toPlainText()
        try:
            with open(path,'w') as f:
                f.write(text)
            self.dialog_message(f'File saved succesfully at {path}', QMessageBox.Information)
        except Exception as e:
            self.dialog_message(e, QMessageBox.Critical)
        else:
            self.path=path
            self.update_title()


    def file_open(self):
        path,_=QFileDialog.getOpenFileName(
            self,
            caption='Open File',
            directory='',
            filter=self.filterTypes
        )
        if path:
            try:
                with open(path, 'r') as f:
                    text=f.read()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path= path
                self.editor.setPlainText(text)
                self.update_title()
                self.editor.update()
    def file_print(self):
        printDlg= QPrintDialog()
        if printDlg.exec_():
            self.editor.print(printDlg.printer())
        pass
    def update_title(self):
        self.setWindowTitle('{} - Notepad 2.0'.format(os.path.basename(self.path) if self.path is not None else 'Unititled'))
    
    def dialog_message(self, message,type):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(type)
        dlg.show()

    def create_action(
        self, parent, icon, action_name, status_tip, shortcut, triggered_method
    ):
        action = QAction(QIcon(icon), action_name, parent)
        action.setStatusTip(status_tip)
        action.triggered.connect(triggered_method)
        action.setShortcut(shortcut)
        return action

    def save_file(self):
        pass


app = QApplication(sys.argv)
notepad = Notepad()
sys.exit(app.exec_())