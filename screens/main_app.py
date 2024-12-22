from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from screens.patient_id_screen import PatientIDScreen
from screens.patient_registration_screen import PatientRegistrationScreen
from screens.symptoms_screen import SymptomsScreen


class MainApp(QMainWindow):
    """Ana uygulama penceresi."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hasta Teşhis Sistemi")
        self.setGeometry(100, 100, 800, 600)

        # Ekranları yönetmek için QStackedWidget kullanımı
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Ekranların eklenmesi
        self.patient_id_screen = PatientIDScreen(self.stacked_widget)
        self.patient_registration_screen = PatientRegistrationScreen(self.stacked_widget)
        self.symptoms_screen = SymptomsScreen()

        self.stacked_widget.addWidget(self.patient_id_screen)          # 0. ekran: Hasta ID girişi
        self.stacked_widget.addWidget(self.patient_registration_screen)  # 1. ekran: Hasta kayıt
        self.stacked_widget.addWidget(self.symptoms_screen)           # 2. ekran: Semptom sorgulama
