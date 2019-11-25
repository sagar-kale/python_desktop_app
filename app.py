import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import urllib.request


class Downloader(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = QVBoxLayout()
        self.url = QLineEdit()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        download = QPushButton("download")
        browse = QPushButton("Browse")

        self.url.setPlaceholderText("Enter Url")
        self.save_location.setPlaceholderText("Enter File save location")
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        self.setFocus()

        layout.addWidget(self.url)
        layout.addWidget(self.save_location)
        layout.addWidget(self.progress)
        layout.addWidget(browse)
        layout.addWidget(download)

        self.setLayout(layout)
        self.setWindowTitle("Downloader")

        download.clicked.connect(self.download)
        browse.clicked.connect(self.browse_file)

    def download(self):
        url = self.url.text()
        path = self.save_location.text()
        try:
            urllib.request.urlretrieve(url, path, self.report)
        except Exception as e:
            QMessageBox.warning(self, "Warning", "Download failed")
            return
        QMessageBox.information(self, "Information", "Download is complete")
        self.progress.setValue(0)
        self.save_location.setText("")
        self.url.setText("")

    def report(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            self.progress.setValue(percent)

    def browse_file(self):
        save_file = QFileDialog.getSaveFileName(self, caption="save file as", directory=".", filter="All Files (*.*)")
        self.save_location.setText(QDir.toNativeSeparators(save_file))


app = QApplication(sys.argv)
dl = Downloader()
dl.show()
app.exec_()
