import sys
from qtpy import QtWidgets
from PyQt5.QtCore import *
from macOS.ui.mainwindow import Ui_MainWindow
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
import time
from selenium.webdriver.common.by import By
from macOS.accountLists import testAccounts
from docx import Document
import datetime

app = QtWidgets.QApplication(sys.argv)




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentBrowser = ''
        self.currentPassword = ''
        self.newPassword = ''
        self.accounts = ''

        self.finish_dialog = QtWidgets.QMessageBox()
        self.error_dialog = QtWidgets.QMessageBox()
        self.docx_dialog = QtWidgets.QMessageBox()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        for key, value in testAccounts.items():
            self.ui.comboBox.addItem(key)

        browsers = ['Chrome', 'Firefox']
        self.ui.comboBox_2.addItems(browsers)

        self.ui.pushButton.clicked.connect(self.changePW)

    def changePW(self):
        self.currentBrowser = self.ui.comboBox_2.currentText()
        self.currentPassword = self.ui.inputCurrent.text()
        self.newPassword = self.ui.inputNew.text()
        self.accounts = self.ui.comboBox.currentText()
        self.obj = Worker(self.accounts, self.currentBrowser, self.currentPassword, self.newPassword)
        self.obj.message.connect(self.errorDialog)
        self.obj.finished.connect(self.done)
        self.obj.progress.connect(self.loadingBar)
        self.obj.docFinish.connect(self.docxDialog)
        self.obj.label4.connect(self.okay4)
        self.obj.label5.connect(self.okay5)
        self.obj.start()

    def errorDialog(self, errorText):
        print(errorText)
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_dialog.setText('Wrong Password in Account:' + errorText)
        self.error_dialog.show()

    def done(self, str):
        self.finish_dialog.setIcon(QtWidgets.QMessageBox.Information)
        self.finish_dialog.setText('Passwords changed to:   ' + str)
        self.finish_dialog.show()

    def loadingBar(self, percentage):
        print(percentage)
        self.ui.progressBar.setValue(percentage)

    def docxDialog(self, str):
        self.docx_dialog.setIcon(QtWidgets.QMessageBox.Information)
        self.docx_dialog.setText(str)
        self.docx_dialog.show()

    # dont' work properly
    def okay4(self, okay1):
        self.ui.label_4.setText(okay1)
        self.ui.label_4.show()

    def okay5(self, okay2):
        self.ui.label_5.setText(okay2)
        self.ui.label_5.show()


class Worker(QThread):
    message = pyqtSignal(str)
    finished = pyqtSignal(str)
    progress = pyqtSignal(float)
    label4 = pyqtSignal(str)
    label5 = pyqtSignal(str)
    docFinish = pyqtSignal(str)

    def __init__(self, accounts, brwser, curPass, newPass):
        QThread.__init__(self)

        self.currentBrowser = brwser
        self.currentPassword = curPass
        self.newPassword = newPass
        self.accounts = accounts

    def run(self):
        document = Document()

        table = document.add_table(rows=1, cols=2)
        document.add_paragraph(str(datetime.datetime.now()))
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'User Account'
        hdr_cells[1].text = 'Password'

        count = float(0)
        while count < 100:
            for acc, address in testAccounts.items():
                if self.accounts == acc:
                    print(acc)
                    for user in testAccounts[acc]:
                        print(acc)
                        b = len(testAccounts[acc])
                        print(b)
                        if self.currentBrowser == 'Firefox':
                            count += 100 / b
                            page = "https://de.tradingview.com"
                            options = webdriver.FirefoxOptions()
                            options.add_argument('-headless')
                            driver = webdriver.Firefox(executable_path='../windows/webdriver/geckodriver', options=options)
                            driver.implicitly_wait(30)
                            driver.minimize_window()
                            driver.get(page)
                            driver.find_element(By.XPATH, "(//a[contains(@href, '#signin')])[2]").click()
                            driver.find_element(By.NAME, "username").send_keys(user)
                            driver.find_element(By.NAME, "password").send_keys(self.currentPassword)
                            driver.find_element(By.XPATH,
                                                "//form[@id='signin-form']/div[3]/div[2]/button/span[2]").click()
                            try:
                                time.sleep(5)
                                driver.find_element(By.XPATH, "//div[4]/span/span").click()
                            except ElementNotInteractableException:
                                self.message.emit(user)
                                self.progress.emit(count)
                                row_cells = table.add_row().cells
                                row_cells[0].text = user
                                row_cells[1].text = 'Wrong Password entered!'
                                empty_cells = table.add_row().cells
                                empty_cells[0].text = ''
                                empty_cells[1].text = ''
                                driver.quit()
                                continue
                            self.label4.emit('OK')
                            driver.find_element(By.XPATH,
                                                "//a[contains(@href, '/u/indaqub/#settings-profile')]").click()
                            driver.find_element(By.XPATH, "//fieldset[2]/span/span/span/span").click()
                            driver.find_element(By.XPATH,
                                                "//form[@id='change-password-form']/fieldset/span/span/div/input").click()
                            driver.find_element(By.NAME, "current_password").send_keys(self.currentPassword)
                            driver.find_element(By.ID, "id_password1").send_keys(self.newPassword)
                            driver.find_element(By.ID, "id_password2").send_keys(self.newPassword)
                            driver.find_element(By.XPATH,
                                                "//form[@id='change-password-form']/div/div/button/span[2]").click()
                            time.sleep(5)
                            driver.find_element(By.XPATH, "//div[4]/span/span").click()
                            driver.find_element(By.XPATH, "//a[contains(@href, '#signout')]").click()
                            self.label5.emit('OK')
                            driver.quit()

                            row_cells = table.add_row().cells
                            row_cells[0].text = user
                            row_cells[1].text = self.newPassword
                            empty_cells = table.add_row().cells
                            empty_cells[0].text = ''
                            empty_cells[1].text = ''

                        self.progress.emit(count)
                        print(str(count) + '%')
        self.finished.emit(self.newPassword)
        for acc in testAccounts:
            if acc == self.accounts:
                document.save(acc + '.docx')
        self.docFinish.emit('Word file with all changed accounts created and saved in application folder! :)')


window = MainWindow()
window.show()

sys.exit(app.exec_())