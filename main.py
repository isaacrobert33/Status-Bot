from PyQt5.QtWidgets import *
from multiprocessing import Process
from threading import Thread
from app import Scraper
from ui_app import *
import sys, os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ICON = resource_path("assets/code.ico")
print(ICON)

class Dialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("A minute!")

		QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel 

		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.save)
		self.buttonBox.rejected.connect(self.cancel)

		self.layout = QVBoxLayout()
		self.message = QLabel("Enter a path to your chrome driver")
		self.input_ = QLineEdit()
		self.input_.setGeometry(QRect(10, 10, 200, 30))
		self.layout.addWidget(self.message)
		self.layout.addWidget(self.input_)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)
		self.show()

	def save(self):
		print("saving..")
		with open(os.path.join(os.getenv("APPDATA"), "driver_path.txt"), "w") as f:
			f.write(self.input_.text())
		self.close()

	def cancel(self):
		print("cancelling...")
		sys.exit()

class MainWindow(QMainWindow):
	def __init__(self) -> None:
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.setWindowTitle("Web Automator")
		self.setWindowIcon(QIcon(ICON))
		self.ui.start_btn.clicked.connect(self.initialize_scraper)
		self.ui.user_input.returnPressed.connect(self.user_entry)
		self.driver_path_fname = os.path.join(os.environ["APPDATA"], "driver_path.txt")
		self.current_event = None

		self.show()
	
	def initialize_scraper(self):
		if not os.path.exists(self.driver_path_fname):
			dlg = Dialog(self)
			if not dlg.exec():
				print("Dialog closed!")
				
				self.scraper = Scraper
				scr = Thread(target=self.scraper, args=(self, self.driver_path_fname))
				scr.start()
				self.ui.start_btn.setEnabled(False)
		else:
			self.scraper = Scraper
			scr = Thread(target=self.scraper, args=(self, self.driver_path_fname))
			scr.start()
			self.ui.start_btn.setEnabled(False)
    	
	def user_entry(self, dt=None):
		try:
			self.__setattr__(self.current_event, True)
		except TypeError:
			self.ui.user_input.setText("")
    
	def set_event(self, evtname):
		print(evtname)
		setattr(self, evtname, None)
		self.current_event = evtname
		

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
