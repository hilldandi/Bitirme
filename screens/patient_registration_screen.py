from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.data_management import id_information, save_id_information, create_patient_file

class PatientRegistrationScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        self.name_label = QLabel("Ad:")
        self.name_input = QLineEdit()
        self.surname_label = QLabel("Soyad:")
        self.surname_input = QLineEdit()
        self.register_button = QPushButton("Kayıt Oluştur")
        self.register_button.clicked.connect(self.register_patient)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def register_patient(self):
        patient_id = self.parent().findChild(QLineEdit, "id_input").text().strip()
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()

        if not name or not surname:
            QMessageBox.warning(self, "Hata", "Ad ve soyad boş bırakılamaz!")
            return

        id_information[patient_id] = {"name": name, "surname": surname}
        save_id_information()
        create_patient_file(patient_id)
        QMessageBox.information(self, "Başarılı", "Hasta kaydı oluşturuldu.")
        self.stacked_widget.setCurrentIndex(2)
