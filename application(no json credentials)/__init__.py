import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui
import sys
import speech_recognition
import win32com.client
import os
import pypandoc


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# noinspection PyAttributeOutsideInit
class MyWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.labels = []
        self.curr_offset = 0, 0
        self.button = None
        self.label = None
        self.speech_text = []
        self.cleared = False
        self.previous_text = ""

        self.bold_format = PyQt5.QtGui.QTextCharFormat()
        self.bold_format.setFontWeight(PyQt5.QtGui.QFont.Bold)

        self.italics_format = PyQt5.QtGui.QTextCharFormat()
        self.italics_format.setFontItalic(True)

        self.underline_format = PyQt5.QtGui.QTextCharFormat()
        self.underline_format.setFontUnderline(True)
        PyQt5.QtWidgets.QApplication.setStyle(
            PyQt5.QtWidgets.QStyleFactory.create('Fusion'))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(PyQt5.QtGui.QIcon(resource_path("app_logo.png")))
        MainWindow.resize(931, 628)
        MainWindow.setStyleSheet("PyQt5.QtWidgets.QMainWindow{\n"
                                 "border-left: 1px solid #a0a0a0;\n"
                                 "border-bottom: 1px solid #a0a0a0;\n"
                                 "border-right: 1px solid #a0a0a0;\n"
                                 "margin: 0px;\n"
                                 "padding: 10px;\n"
                                 "background: rgb(255, 255, 255);\n"
                                 "}")
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(PyQt5.QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = PyQt5.QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget{\n"
                                         "border-left: 1px solid #a0a0a0;\n"
                                         "border-bottom: 1px solid #a0a0a0;\n"
                                         "border-right: 1px solid #a0a0a0;\n"
                                         "margin: 0px;\n"
                                         "padding: 10px;\n"
                                         "background: rgb(255, 255, 255);\n"
                                         "}")
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = PyQt5.QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(PyQt5.QtCore.QRect(1, 0, 671, 545))
        self.textEdit.viewport().setProperty("cursor", PyQt5.QtGui.QCursor(
            PyQt5.QtCore.Qt.IBeamCursor))
        self.textEdit.setStyleSheet("background: rgb(255, 255, 255);\n"
                                    "")
        self.textEdit.setObjectName("textEdit")
        SpeechHandler.textEditor = self.textEdit

        self.label = PyQt5.QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(PyQt5.QtCore.QRect(675, 0, 256, 43))
        self.label.setStyleSheet(u"background: rgb(255, 255, 255);\n"
                                 "border: 0px;\n"
                                 "font: 11pt \"Segoe UI Semilight\";")

        OptionsListWidget.textEditor = self.textEdit
        self.label.setObjectName("label")
        self.listWidget = OptionsListWidget(self.centralwidget)
        self.listWidget.setGeometry(PyQt5.QtCore.QRect(671, 42, 260, 503))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setWordWrap(True)
        self.listWidget.setSpacing(15)
        self.listWidget.itemClicked.connect(self.listWidget.item_clicked)

        SpeechHandler.listWidget = self.listWidget
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = PyQt5.QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = PyQt5.QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(PyQt5.QtCore.QRect(0, 0, 931, 26))
        self.menubar.setObjectName("menubar")

        self.menuFile = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuAbout = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")

        self.menuAccents = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menuAccents.setObjectName("menuAccents")

        MainWindow.setMenuBar(self.menubar)

        self.toolBar = PyQt5.QtWidgets.QToolBar(MainWindow)
        self.toolBar.setStyleSheet("background: rgb(220, 220, 220);")
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(PyQt5.QtCore.Qt.TopToolBarArea, self.toolBar)

        self.actionOpen_File = PyQt5.QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionOpen_File.triggered.connect(self.open_file)

        self.actionSave = PyQt5.QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.save_file)

        self.actionNigerian = PyQt5.QtWidgets.QAction(MainWindow)
        self.actionNigerian.setObjectName("actionNigerian")
        self.actionNigerian.triggered.connect(lambda: SpeechHandler.set_accent(1))

        self.actionNorthAmerican = PyQt5.QtWidgets.QAction(MainWindow)
        self.actionNigerian.setObjectName("actionNorthAmerican")
        self.actionNorthAmerican.triggered.connect(lambda: SpeechHandler.set_accent(0))

        self.actionInfo = PyQt5.QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.actionInfo.triggered.connect(self.about_info)

        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionSave)

        self.menuAccents.addAction(self.actionNigerian)
        self.menuAccents.addAction(self.actionNorthAmerican)

        self.menuAbout.addAction(self.actionInfo)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAccents.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.init_formatbar()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"Speak+Write",
                                                    None))
        self.actionOpen_File.setText(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"Open File", None))
        self.actionSave.setText(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionNigerian.setText(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"Nigerian", None))
        self.actionNorthAmerican.setText(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"North American", None))
        self.actionInfo.setText(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"App Info", None))
        self.textEdit.setHtml(PyQt5.QtCore.QCoreApplication.translate("MainWindow",
                                                                      u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                                      "p, li { white-space: pre-wrap; }\n"
                                                                      "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                                      "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>",
                                                                      None))
        self.label.setText(PyQt5.QtCore.QCoreApplication.translate("MainWindow",
                                                                   u"Speech-to-Text Options",
                                                                   None))
        self.menuFile.setTitle(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"File", None))
        self.menuAbout.setTitle(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"About", None))
        self.menuAccents.setTitle(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"Accents", None))
        self.toolBar.setWindowTitle(
            PyQt5.QtCore.QCoreApplication.translate("MainWindow", u"toolBar", None))
        # retranslateUi

    def init_formatbar(self):
        self.toolBar.setIconSize(PyQt5.QtCore.QSize(24, 24))
        undo_button = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("undo.png")),
                                              "Undo", self)
        undo_button.triggered.connect(self.textEdit.undo)
        self.toolBar.addAction(undo_button)

        redo_button = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("redo.png")),
                                              "redo", self)
        redo_button.triggered.connect(self.textEdit.redo)
        self.toolBar.addAction(redo_button)

        self.toolBar.addSeparator()

        font_box = PyQt5.QtWidgets.QFontComboBox(self)
        font_box.currentFontChanged.connect(self.change_font)
        font_box.setEditable(False)
        font_box.setStyleSheet("combobox-popup: 0;")
        font_box.setFontFilters(PyQt5.QtWidgets.QFontComboBox.ScalableFonts)

        self.toolBar.addWidget(font_box)

        self.font_size = PyQt5.QtWidgets.QComboBox(self)
        self.font_size.setEditable(True)
        self.font_size.setMinimumContentsLength(3)
        self.font_size.activated.connect(self.change_font_size)
        self.font_sizes = ['9', '10', '11', '12', '13', '14',
                           '15', '16', '18', '20', '22', '24', '26', '28',
                           '32', '36', '40', '44', '48', '54', '60', '66',
                           '72', '80', '88', '96']
        for size in self.font_sizes:
            self.font_size.addItem(size)
        self.toolBar.addWidget(self.font_size)

        self.toolBar.addSeparator()

        font_colour = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(
            resource_path("text_fontcolour.png")),
            "Change font colour", self)
        font_colour.triggered.connect(self.change_font_colour)
        self.toolBar.addAction(font_colour)

        background_colour = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(
            resource_path("font_highlight.png")),
            "Change highlight colour", self)
        background_colour.triggered.connect(self.change_font_highlight)
        self.toolBar.addAction(background_colour)

        self.toolBar.addSeparator()

        text_bold = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("text_bold.png")),
                                            "Set bold", self)
        text_bold.triggered.connect(self.change_text_bold)
        text_bold.setShortcut(PyQt5.QtGui.QKeySequence.Bold)
        self.toolBar.addAction(text_bold)

        text_italics = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("text_italics.png")),
                                               "Set italics", self)
        text_italics.triggered.connect(self.change_text_italics)
        text_italics.setShortcut(PyQt5.QtGui.QKeySequence.Italic)
        self.toolBar.addAction(text_italics)

        text_underline = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(
            resource_path("text_underline.png")),
            "Set underline", self)
        text_underline.triggered.connect(self.change_text_underline)
        text_underline.setShortcut(PyQt5.QtGui.QKeySequence.Underline)
        self.toolBar.addAction(text_underline)

        self.toolBar.addSeparator()

        left_align = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("left_align.png")),
                                             "Left Align", self)
        left_align.triggered.connect(self.left_align_text)
        self.toolBar.addAction(left_align)

        centre_align = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("centre_align.png")),
                                               "Centre Align", self)
        centre_align.triggered.connect(self.centre_align_text)
        self.toolBar.addAction(centre_align)

        right_align = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("right_align.png")),
                                              "Right Align", self)
        right_align.triggered.connect(self.right_align_text)
        self.toolBar.addAction(right_align)

        justify_align = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(
            resource_path("justify_align.png")),
            "Justify Align", self)
        justify_align.triggered.connect(self.justify_align_text)
        self.toolBar.addAction(justify_align)

        self.toolBar.addSeparator()

        indent_action = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("indent.png")),
                                                "Increase Indent",
                                                self)
        indent_action.triggered.connect(self.indent_text)
        self.toolBar.addAction(indent_action)

        unindent_action = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("unindent.png")),
                                                  "Decrease Indent",
                                                  self)
        unindent_action.triggered.connect(self.unindent_text)
        self.toolBar.addAction(unindent_action)

        self.toolBar.addSeparator()
        mic_action = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(resource_path("microphone.png")),
                                             "Listen",
                                             self)
        mic_action.triggered.connect(self.record_speech)
        self.toolBar.addAction(mic_action)

    def change_font(self, new_font):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            curr_font_size = cursor.charFormat().fontPointSize()
            font_format = PyQt5.QtGui.QTextCharFormat()
            font_format.setFont(new_font)
            font_format.setFontPointSize(int(curr_font_size))
            cursor.mergeCharFormat(font_format)

        else:
            self.textEdit.setFont(new_font)

    def change_font_size(self, new_font_size):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            size_format = PyQt5.QtGui.QTextCharFormat()
            size_format.setFontPointSize(int(self.font_size.currentText()))
            cursor.mergeCharFormat(size_format)
        else:
            self.textEdit.setFontPointSize(int(self.font_size.currentText()))

    def change_font_colour(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            colour = PyQt5.QtWidgets.QColorDialog.getColor()
            colour_format = PyQt5.QtGui.QTextCharFormat()
            colour_format.setForeground(colour)
            cursor.mergeCharFormat(colour_format)
        else:
            colour = PyQt5.QtWidgets.QColorDialog.getColor()
            self.textEdit.setTextColor(colour)

    def change_font_highlight(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            colour = PyQt5.QtWidgets.QColorDialog.getColor()
            colour_format = PyQt5.QtGui.QTextCharFormat()
            colour_format.setBackground(colour)
            cursor.mergeCharFormat(colour_format)
        else:
            colour = PyQt5.QtWidgets.QColorDialog.getColor()
            self.textEdit.setTextBackgroundColor(colour)

    def change_text_bold(self):
        cursor = self.textEdit.textCursor()

        if cursor.hasSelection():
            if cursor.charFormat().fontWeight() == PyQt5.QtGui.QFont.Bold:
                temp_format = cursor.charFormat()
                temp_format.setFontWeight(PyQt5.QtGui.QFont.Normal)
                cursor.setCharFormat(temp_format)
            else:
                cursor.mergeCharFormat(self.bold_format)
        else:
            if self.textEdit.fontWeight() == PyQt5.QtGui.QFont.Bold:
                self.textEdit.setFontWeight(PyQt5.QtGui.QFont.Normal)
            else:
                self.textEdit.setFontWeight(PyQt5.QtGui.QFont.Bold)

    def change_text_italics(self):
        cursor = self.textEdit.textCursor()

        if cursor.hasSelection():
            if cursor.charFormat().fontItalic():
                temp_format = cursor.charFormat()
                temp_format.setFontItalic(False)
                cursor.setCharFormat(temp_format)
            else:
                cursor.mergeCharFormat(self.italics_format)
        else:
            if self.textEdit.fontItalic():
                self.textEdit.setFontItalic(False)
            else:
                self.textEdit.setFontItalic(True)

    def change_text_underline(self):
        cursor = self.textEdit.textCursor()

        if cursor.hasSelection():
            if cursor.charFormat().fontUnderline():
                temp_format = cursor.charFormat()
                temp_format.setFontUnderline(False)
                cursor.setCharFormat(temp_format)
            else:
                cursor.mergeCharFormat(self.underline_format)
        else:
            if self.textEdit.fontUnderline():
                self.textEdit.setFontUnderline(False)
            else:
                self.textEdit.setFontUnderline(True)

    def align_text(self, align_type):
        cursor = self.textEdit.textCursor()
        paragraph_format = PyQt5.QtGui.QTextBlockFormat()
        options = [PyQt5.QtCore.Qt.AlignLeft, PyQt5.QtCore.Qt.AlignRight,
                   PyQt5.QtCore.Qt.AlignCenter, PyQt5.QtCore.Qt.AlignJustify]
        curr_option = 0
        if align_type == 'left':
            curr_option = 0
        elif align_type == 'right':
            curr_option = 1
        elif align_type == 'centre':
            curr_option = 2
        elif align_type == 'justify':
            curr_option = 3
        paragraph_format.setAlignment(options[curr_option])

        if cursor.hasSelection():
            cursor.mergeBlockFormat(paragraph_format)
        else:
            self.textEdit.setAlignment(options[curr_option])

    def left_align_text(self):
        self.align_text('left')

    def right_align_text(self):
        self.align_text('right')

    def centre_align_text(self):
        self.align_text('centre')

    def justify_align_text(self):
        self.align_text('justify')

    def indent_text(self):
        cursor = self.textEdit.textCursor()
        indent_format = PyQt5.QtGui.QTextBlockFormat()
        if cursor.hasSelection():
            indent_format.setIndent(cursor.blockFormat().indent() + 1)
            cursor.mergeBlockFormat(indent_format)
        else:
            prev_pos = cursor.position()
            cursor.movePosition(PyQt5.QtGui.QTextCursor.StartOfBlock)
            cursor.movePosition(PyQt5.QtGui.QTextCursor.EndOfBlock, cursor.KeepAnchor)
            indent_format.setIndent(cursor.blockFormat().indent() + 1)
            cursor.mergeBlockFormat(indent_format)
            cursor.movePosition(prev_pos)

    def unindent_text(self):
        cursor = self.textEdit.textCursor()
        indent_format = PyQt5.QtGui.QTextBlockFormat()
        if cursor.hasSelection():
            indent_format.setIndent(cursor.blockFormat().indent() - 1)
            cursor.mergeBlockFormat(indent_format)
        else:
            prev_pos = cursor.position()
            cursor.movePosition(PyQt5.QtGui.QTextCursor.StartOfBlock)
            cursor.movePosition(PyQt5.QtGui.QTextCursor.EndOfBlock, cursor.KeepAnchor)
            indent_format.setIndent(cursor.blockFormat().indent() - 1)
            cursor.mergeBlockFormat(indent_format)
            cursor.movePosition(prev_pos)

    def record_speech(self):
        if not SpeechHandler.running:
            SpeechHandler.running = True
            self.thread = PyQt5.QtCore.QThread()
            self.worker = SpeechHandler()
            self.worker.textEditor = self.textEdit

            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()

    # def clearText(self):
    #     if not self.cleared:
    #         self.previous_text = self.textEdit.toPlainText()
    #         self.textEdit.setText("")
    #         self.cleared = True
    #
    # def undoClearText(self):
    #     if self.cleared:
    #         self.textEdit.setText(self.previous_text)
    #         self.cleared = False
    #
    # def quitThread(self):
    #     if isinstance(self.thread, PyQt5.QtCore.QThread):
    #         self.thread.quit()

    def open_file(self):
        file_name = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                                                'c:\\',
                                                                "Text files (*.txt *.doc *.docx *.spwr)")
        if file_name[0] != '':
            actual_name = str(os.path.basename(file_name[0]))
            file_ext = str(os.path.splitext(actual_name)[1])
            if file_ext == '.docx' or file_ext == '.doc':
                try:
                    doc = win32com.client.GetObject(
                        os.getcwd() + '\\' + actual_name)
                    doc.SaveAs(FileName=os.getcwd() + "\\temp.html",
                               FileFormat=8)
                    doc.Close()
                    fp = open("temp.html", 'r')
                    self.textEdit.setHtml(fp.read())
                    fp.close()
                except:
                    output = pypandoc.convert_file(file_name[0], 'html')
                    self.textEdit.setHtml(output)
            elif file_ext == '.spwr':
                orig_file = open(file_name[0], 'r')
                self.textEdit.setHtml(orig_file.read())
            elif file_ext == '.txt':
                orig_file = open(file_name[0], 'r')
                self.textEdit.setPlainText(orig_file.read())
            else:
                PyQt5.QtWidgets.QMessageBox.warning(self, "File Error",
                                                    "Something went wrong")

    def save_file(self):
        file_name = PyQt5.QtWidgets.QFileDialog.getSaveFileName(self, "Save File",
                                                                'c:\\',
                                                                "Microsoft Word File(Lose text formatting!) (*.docx);; Speak+Write File (*.spwr);; Plain Text File(*.txt);;")
        if file_name[0] != '':
            file_ext = str(os.path.splitext(file_name[0])[1])
            if file_ext == '.docx':
                pypandoc.convert_text(self.textEdit.toHtml(), 'docx',
                                      format='html', outputfile=file_name[0])
            elif file_ext == '.spwr':
                s_file = open(file_name[0], 'w')
                s_file.write(self.textEdit.toHtml())
                s_file.close()
            elif file_ext == '.txt':
                s_file = open(file_name[0], 'w')
                s_file.write(self.textEdit.toPlainText())
                s_file.close()

    def about_info(self):
        PyQt5.QtWidgets.QMessageBox.information(self, "Info", "Made by Daniel Adesina: danieladesina999@hotmail.com\n"
                                                               "All .spwr files can be opened in Microsoft Word")


class OptionsListWidget(PyQt5.QtWidgets.QListWidget):
    textEditor = None

    def item_clicked(self, item):
        self.textEditor.append(item.text())
        self.clear()


class SpeechHandler(PyQt5.QtCore.QObject):
    finished = PyQt5.QtCore.pyqtSignal()
    textEditor = None
    listWidget = None
    running = False
    accents = ['north-american', 'nigerian']
    curr_accent = 0

    def run(self):
        self.listWidget.clear()
        temp = check_speech(self.accents[self.curr_accent])
        if temp is not None:
            if 'results' in temp:
                for i in temp['results']:
                    self.listWidget.addItem(i['alternatives'][0]['transcript'])
            else:
                for item in [result['transcript'] for result in
                             temp['alternative']]:
                    self.listWidget.addItem(item)
        else:
            self.listWidget.addItem("ERROR: Didn't quite catch that?")
        self.finished.emit()

    @staticmethod
    def set_accent(num):
        SpeechHandler.curr_accent = num


def check_speech(curr_accent):
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    with mic as source:
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=15)
            recognizer.dynamic_energy_threshold = False
            recognizer.energy_threshold = 400
            # recognizer.adjust_for_ambient_noise(source)
            try:
                if curr_accent == 'north-american':
                    curr = recognizer.recognize_google(audio, show_all=True)
                else:
                    curr = recognizer.recognize_google_cloud(audio, language="en-NG", show_all=True)
                SpeechHandler.running = False
                if not curr:
                    return None
                else:
                    return curr
            except:
                SpeechHandler.running = False
                return None
        except:
            SpeechHandler.running = False
            return None


if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = resource_path("credentials.json")
    # recognizer = speech_recognition.Recognizer()
    # mic = speech_recognition.Microphone()
    # with mic as source:
    #     print("listening...")
    #     audio = recognizer.listen(source, timeout=3, phrase_time_limit=15)
    #     recognizer.dynamic_energy_threshold = False
    #     recognizer.energy_threshold = 400
    #     curr = recognizer.recognize_google_cloud(audio, language="en-NG", show_all=True)
    run = True
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    MainWindow = PyQt5.QtWidgets.QMainWindow()

    ui = MyWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
