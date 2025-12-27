import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QFileDialog
from ui.rsa_2 import Ui_MainWindow
import requests
class RSA_Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.gen_keys_person_1.clicked.connect(self.call_api_gen_keys)
        self.ui.gen_keys_person_2.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        #self.ui.btn_decrypt.clicked.connect()
        self.ui.btn_open_file.clicked.connect(self.prepare_file)
        #self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify) #Button Verify right most of the UI program screen 
        #self.ui.btn_encrypt_2.clicked.connect()
        self.ui.btn_decrypt_2.clicked.connect(self.call_api_decrypt)
        self.ui.btn_open_file_2.clicked.connect(self.prepare_file_2)
        self.ui.btn_sign_2.clicked.connect(self.call_api_sign) #Button Sign at the left most of the UI program screen
        #self.ui.btn_verify_2.clicked.connect(self.call_api_verify)
        
    def call_api_gen_keys(self):
        url="http://127.0.0.1:5000/api/rsa/generate_keys"
        payload={
            "sender_name":self.ui.input_sender_name_person_1.toPlainText(),
            "sender_name_2":self.ui.input_sender_name_person_2.toPlainText()
        }
        
        try:
            response=requests.post(url,json=payload)
            if response.status_code==200:
                data=response.json()
                
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
                self.ui.input_sender_name_person_1.clear()
                self.ui.input_sender_name_person_2.clear()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error %s" % e)
    def prepare_file(self):
        fname, _=QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;PDF File (*.pdf);; Doc Files (*.doc,*.docx);; PNG Files (*.png);; JPEG Files (*.jpg)")
        
        if fname:
            self.ui.file_name_display_person_1.setText(str(fname))
            #self.ui.file_name_display_person_2.setText(str(fname))
            
    def prepare_file_2(self):
        fname, _=QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;PDF File (*.pdf);; Doc Files (*.doc,*.docx);; PNG Files (*.png);; JPEG Files (*.jpg)")
        
        if fname:
            self.ui.file_name_display_person_2.setText(str(fname))
    
    def call_api_encrypt(self):
        url="http://127.0.0.1:5000/api/rsa/encrypt"
        payload={
            "package": self.ui.file_name_display_person_1.text(),
            "sender": self.ui.input_sender_name_person_1.toPlainText(),
            "receiver": self.ui.input_receiver_name_person_1.toPlainText()
        }
        try:
            response=requests.post(url,json=payload)
            if response.status_code == 200:
                data=response.json()
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
                if data["message"]=="This receiver doesn't exist":
                    self.ui.input_receiver_name_person_1.clear()
                    self.ui.input_sender_name_person_1.clear()
                    self.ui.file_name_display_person_1.clear()
                    self.ui.file_name_display_person_1.setText("File Name Display: ")
                elif data["message"]=="This sender doesn't exist":
                    self.ui.input_receiver_name_person_1.clear()
                    self.ui.input_sender_name_person_1.clear()
                    self.ui.file_name_display_person_1.clear()
                    self.ui.file_name_display_person_1.setText("File Name Display: ")
                else:
                    self.ui.file_name_display_person_2.setText(payload["package"])
                    self.ui.file_name_display_person_1.clear()
                    self.ui.file_name_display_person_1.setText("File Name Display: ")
                    self.ui.input_receiver_name_person_2.setPlainText(self.ui.input_receiver_name_person_1.toPlainText())
                    self.ui.input_receiver_name_person_1.clear()
                    self.ui.input_sender_name_person_1.clear()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error %" % e)
    def call_api_decrypt(self):
        url="http://127.0.0.1:5000/api/rsa/decrypt"
        payload={
            "receiver":self.ui.input_receiver_name_person_2.toPlainText()
        }
        try:
            response=requests.post(url,json=payload)
            if response.status_code == 200:
                data=response.json()
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
                self.ui.file_name_display_person_2.clear()
                self.ui.file_name_display_person_2.setText("File Name Display: ")
                self.ui.input_receiver_name_person_2.clear()
                self.ui.decrypted_message_display.setPlainText(data["decrypted"])
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error %" % e)
    
    def call_api_sign(self):
        url="http://127.0.0.1:5000/api/rsa/sign"
        payload={
            "sender":self.ui.input_sender_name_person_1.toPlainText(),
            "package":self.ui.file_name_display_person_1.text(),
            "receiver":self.ui.input_receiver_name_person_1.toPlainText(),
        }
        try:
            response=requests.post(url,json=payload)
            if response.status_code == 200:
                data=response.json()
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
                if data["message"]=="This sender doesn't exist":  
                    self.ui.input_sender_name_person_1.clear()
                    self.ui.input_receiver_name_person_1.clear()
                    self.ui.file_name_display_person_1.clear()
                    self.ui.file_name_display_person_1.setText("File Name Display: ")
                    self.ui.input_sender_name_person_2.clear()
                    self.ui.input_receiver_name_person_2.clear()
                    self.ui.file_name_display_person_2.clear()
                    self.ui.file_name_display_person_2.setText("File Name Display: ")
                elif data["message"]=="This receiver doesn't exist":
                    self.ui.input_sender_name_person_1.clear()
                    self.ui.input_receiver_name_person_1.clear()
                    self.ui.file_name_display_person_1.clear()
                    self.ui.file_name_display_person_1.setText("File Name Display: ")
                    self.ui.input_sender_name_person_2.clear()
                    self.ui.input_receiver_name_person_2.clear()
                    self.ui.file_name_display_person_2.clear()
                    self.ui.file_name_display_person_2.setText("File Name Display: ")
                else:
                    self.ui.file_name_display_person_2.setText(self.ui.file_name_display_person_1.text())
                    self.ui.file_name_display_person_1.clear()
                    self.ui.file_name_display_person_1.setText("File Name Display: ")
                    self.ui.input_sender_name_person_2.setPlainText(self.ui.input_sender_name_person_1.toPlainText())
                    self.ui.input_sender_name_person_1.clear()
                    self.ui.input_receiver_name_person_2.setPlainText(self.ui.input_receiver_name_person_1.toPlainText())
                    self.ui.input_receiver_name_person_1.clear()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error %" % e)
    def call_api_verify(self):
        url="http://127.0.0.1:5000/api/rsa/verify"
        payload={
            "sender":self.ui.input_sender_name_person_2.toPlainText(),
            "receiver":self.ui.input_receiver_name_person_2.toPlainText(),
            "package":self.ui.file_name_display_person_2.text()
        }
        try:
            response=requests.post(url,json=payload)
            if response.status_code == 200:
                data=response.json()
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
                self.ui.input_sender_name_person_1.clear()
                self.ui.file_name_display_person_1.clear()
                self.ui.file_name_display_person_1.setText("File Name Display: ")
                self.ui.input_sender_name_person_2.clear()
                self.ui.input_receiver_name_person_2.clear()
                self.ui.file_name_display_person_2.clear()
                self.ui.file_name_display_person_2.setText("File Name Display: ")
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error %" % e)
        
        
            



if __name__ == "__main__":
    app=QApplication(sys.argv)
    window=RSA_Interface()
    window.show()
    sys.exit(app.exec_())
                
                