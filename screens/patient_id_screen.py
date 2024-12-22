from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.data_management import id_information

class PatientIDScreen(QWidget):
    """Hasta ID giriş ekranı."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        self.id_label = QLabel("TC Kimlik Numarası:")
        self.id_input = QLineEdit()
        self.next_button = QPushButton("Devam Et")
        self.next_button.clicked.connect(self.check_patient)

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.next_button)
        self.setLayout(layout)

    def check_patient(self):
        patient_id = self.id_input.text().strip()
        if len(patient_id) != 11 or not patient_id.isdigit():
            QMessageBox.warning(self, "Hata", "Geçerli bir TC kimlik numarası girin!")
            return

        if patient_id in id_information:
            patient_name = id_information[patient_id]["name"]
            patient_surname = id_information[patient_id]["surname"]
            QMessageBox.information(self, "Hoş Geldiniz", f"Hoş geldiniz {patient_surname}, {patient_name}.")
            self.stacked_widget.setCurrentIndex(2)  # Semptom ekranına geç
        else:
            QMessageBox.information(self, "Kayıt Bulunamadı", "Hasta kaydı bulunamadı, lütfen kayıt oluşturun.")
            self.stacked_widget.setCurrentIndex(1)  # Hasta kayıt ekranına geç
