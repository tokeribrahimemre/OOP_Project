import sys

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
import  pandas as pd
import numpy as np

#cocuk ekrani 
class Stable(QDialog):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.init_ui()
     
    def init_ui(self):
        sorular=pd.read_excel("skortablosu.xlsx").values.tolist()
       
        self.table=QtWidgets.QTableWidget(len(sorular),3) 
        self.table.setHorizontalHeaderLabels(["Kayıt Sırası","Ögrenci","skor"])
        for count, i in enumerate(sorular):
            self.table.setItem(count, 0,  QTableWidgetItem(str(i[1])))
            self.table.setItem(count, 1,  QTableWidgetItem(str(i[2])))
            self.table.setItem(count, 2,  QTableWidgetItem(str(i[3])))
       
        v_box=QtWidgets.QVBoxLayout()
        
        v_box.addWidget(self.table)
       
        v_box.addStretch()
    
        self.setLayout(v_box)
        
        self.setGeometry(500,410,400,500)

class cocukScreen(QDialog):
    switch_window = QtCore.pyqtSignal()
    def __init__(self,username):
        super().__init__()
        self.username=username
        self.init_ui()
     
    def init_ui(self):
        sorular=pd.read_excel("sorular.xlsx").values.tolist()
        self.butonbitir = QtWidgets.QPushButton("Bitir")
        self.butonbitir.clicked.connect(self.bitir)
        self.table=QtWidgets.QTableWidget(len(sorular),3) 
        self.table.setHorizontalHeaderLabels(["a","b","cevaplar"])
        for count, i in enumerate(sorular):
            self.table.setItem(count, 0,  QTableWidgetItem(str(i[1])))
            self.table.setItem(count, 1,  QTableWidgetItem(str(i[2])))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(1000)
        self.time_left_int=count*10
        self.sure=count*10
        self.time_passed_qll = QtWidgets.QLabel()
        self.n=count+1
        v_box=QtWidgets.QVBoxLayout()
        
        v_box.addWidget(self.table)
        v_box.addWidget( self.time_passed_qll )
        v_box.addStretch()
        v_box.addWidget(self.butonbitir)
        self.setLayout(v_box)
        
        self.setGeometry(500,410,400,500)
    def timeout(self):
       self.time_left_int -= 1

       if self.time_left_int == 0:
           pass

       self.update_gui()
    def update_gui(self):
       self.time_passed_qll.setText(str(self.time_left_int))
    def bitir(self):
        data=[]
        data2=[]
        dogrusayisi=0
        for i in range(self.n):
                dogru='yanlış'
                item1=self.table.item(i,0).text()
                item2=self.table.item(i,1).text()
                item3=self.table.item(i,2).text()
                if int(item1)*int(item2)==int(item3):
                    dogru='Doğru'
                    dogrusayisi+=1
                dictt={'Ogrencı':self.username,'a':item1,'b':item2,'Durum':dogru,'sure':self.sure-self.time_left_int}
                data.append(dictt)
        data=pd.DataFrame(data)
        skor=(self.sure-self.time_left_int)*dogrusayisi
      
        skorT=pd.read_excel('skortablosu.xlsx',index_col=0).values.tolist()
        if len(skorT)==0:
            print('eroor')
            dictt={'Ogrencı':self.username,'skor':skor}
            data2.append(dictt)
            data2=pd.DataFrame(data2)
            data2.to_excel('skortablosu.xlsx')
              
           
 
    
        skorT.append([len( skorT)+1,self.username,skor])
        skorT=pd.DataFrame(skorT,columns=['kayıt sırası','Öğrenci','Skor'])
        skorT=skorT.sort_values("Skor",ascending=False)
        skorT.to_excel('skortablosu.xlsx')
        

        name=self.username+'.txt'
        with open(name, 'a') as f:
            dfAsString = data.to_string( index=False)
            f.write(dfAsString)
        self.close()
class tabloo(QDialog):
    switch_window = QtCore.pyqtSignal()
    def __init__(self,n):
        super().__init__()
        self.n=n
        self.init_ui()
     
    def init_ui(self):
        self.table=QtWidgets.QTableWidget() 
        self.table.setRowCount(self.n)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["a","b"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
    QHeaderView.Stretch)
        self.butonkayit = QtWidgets.QPushButton("Kaydet")
        
        self.butonkayit.clicked.connect(self.kaydet)
        h_box2 = QtWidgets.QHBoxLayout()
    
        
        h_box2.addWidget(self.butonkayit)
        h_box2.addWidget(self.butonskor)
        v_box=QtWidgets.QVBoxLayout()
        
        v_box.addWidget(self.table)
        v_box.addStretch()
        v_box.addLayout(h_box2)
        self.setLayout(v_box)
        
        self.setGeometry(500,410,400,500)
    def kaydet(self):
        data=[]
        for i in range(self.n):
       
                
                item1=self.table.item(i,0).text()
                item2=self.table.item(i,1).text()
           
                
                    
                dictt={"a":item1,"b":item2}
                data.append(dictt)
        data=pd.DataFrame(data)
        data.to_excel("sorular.xlsx")
class ebeveynScreen(QDialog):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.lineEdit_soruS=QtWidgets.QLineEdit()
        self.lineEdit_soruS.setPlaceholderText('Soru Sayısını Giriniz')
       
        
        self.butonskor= QtWidgets.QPushButton("skor tablosuna görme")
        self.butonskor.clicked.connect(self.skorf)
        self.butontablo= QtWidgets.QPushButton("Soruları oluştur")
        self.butontablo.clicked.connect(self.tablof)
        h_box = QtWidgets.QHBoxLayout()
        
    
        
        h_box.addWidget(self.lineEdit_soruS)
       
        h_box2 = QtWidgets.QHBoxLayout()
    
        
        
        h_box2.addWidget(self.butontablo)
        h_box2.addWidget(self.butonskor)
        v_box=QtWidgets.QVBoxLayout()
        
        v_box.addLayout(h_box)
        v_box.addStretch()
        v_box.addLayout(h_box2)
        self.setLayout(v_box)
        
        self.setGeometry(300,310,200,100)
    def tablof(self):
        self.F=tabloo(int(self.lineEdit_soruS.text()))
        self.F.show()
        self.close()
    def skorf(self):
        self.F=Stable()
        self.F.show()
       
#main pencere
class Pencere (QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)
    
    def __init__(self):

        super().__init__()
        self.setWindowTitle('Giriş Ekranı')
       
        
   
       



       
        self.table=QtWidgets.QTableWidget() 
        self.lineEdit_username =QtWidgets.QLineEdit()
        self.lineEdit_username.setPlaceholderText('Kullanıcı adını Giriniz')
       
        self.lineEdit_sifre=QtWidgets.QLineEdit()
        self.lineEdit_sifre.setPlaceholderText('Şifrenizi Giriniz')
        self.butoncalistir = QtWidgets.QPushButton("Giriş")
        self.butoncalistir.setIcon(QtGui.QIcon("calistir.png"))
        self.butoncalistir.clicked.connect(self.check_password)
       
    
      
 
        h_box2 = QtWidgets.QHBoxLayout()
    
        
        h_box2.addWidget(self.butoncalistir)
     
       

   
        

        v_box=QtWidgets.QVBoxLayout()
        v_box.addWidget(self.lineEdit_username)
        v_box.addWidget(self.lineEdit_sifre)
       
        
        v_box.addStretch()
        v_box.addLayout(h_box2)
        w = QtWidgets.QWidget()
        w.setLayout(v_box)
        self.setCentralWidget(w)
        self.setGeometry(300,310,300,100)
    def check_password (self):
        users=pd.read_excel('accounts.xlsx').values.tolist()
        status=0
        self.lineEdit_username.text()
        for i in users:
            if i[0]==  self.lineEdit_username.text() and i[1]==  self.lineEdit_sifre.text():
                status=1 
                if i[2]==1:
                        status=1
                        self.F=ebeveynScreen()
                        self.F.show()
                        self.close()
                else:
                    self.F=cocukScreen(self.lineEdit_username.text())
                    self.F.show()
                    self.close()
        if    status==0:
                 
            QtWidgets.QMessageBox.about(self, "Giriş Hatası", "Lütfen kullanıcı adını ve şifresini kontrol edin")
      
app = QtWidgets.QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec_())