import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
import sqlite3

# db setup
def setup_database():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            tc_no TEXT UNIQUE,
            name TEXT,
            surname TEXT,
            gender TEXT,
            age INTEGER,
            hospital TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY,
            date TEXT,
            hospital_name TEXT,
            patient_name TEXT,
            tc_no TEXT,
            questions_and_answers TEXT,
            final_diagnosis TEXT,
            protocol_number TEXT
        )
    ''')
    conn.commit()
    conn.close()
# Protokol numarası oluşturma fonksiyonu
def generate_protocol_number(hospital_name):
    import datetime  # Tarih işlemleri için
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    date_prefix = f"{year}{month:02}{day:02}"

    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM diagnoses WHERE hospital_name = ? AND date LIKE ?",
        (hospital_name, f"{year}-{month:02}%")
    )
    count = cursor.fetchone()[0] + 1  # Ay içerisindeki toplam hasta sayısı + 1
    conn.close()

    protocol_number = f"{date_prefix}{count:02}"  # 2024122303 formatında
    return protocol_number

def load_diagnostic_trees():
    with open('diagnostic_trees.json', 'r', encoding='utf-8') as file:
        diagnostic_trees = json.load(file)
    return diagnostic_trees

# main app
class DiagnosisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Diagnosis System")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_scene = LoginScene(self)
        self.diagnosis_scene = DiagnosisScene(self)
        self.results_scene = ResultsScene(self)

        self.stacked_widget.addWidget(self.login_scene)
        self.stacked_widget.addWidget(self.diagnosis_scene)
        self.stacked_widget.addWidget(self.results_scene)

        self.stacked_widget.setCurrentWidget(self.login_scene)

    def switch_to_login_scene(self):
        self.stacked_widget.setCurrentWidget(self.login_scene)

    def switch_to_diagnosis_scene(self):
        self.stacked_widget.setCurrentWidget(self.diagnosis_scene)
        self.diagnosis_scene.load_patient_diagnoses()

    def switch_to_results_scene(self):
        self.stacked_widget.setCurrentWidget(self.results_scene)

class LoginScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.hospital_combo = QComboBox()
        self.hospital_combo.setStyleSheet("font-size: 18px; padding: 5px;")
        self.hospital_combo.addItems(["Hastane-1", "Hastane-2", "Hastane-3"])

        self.tc_input = QLineEdit()
        self.tc_input.setPlaceholderText("TC Kimlik No")
        self.tc_input.setStyleSheet("font-size: 18px; padding: 5px;")

        search_button = QPushButton("Hasta Ara")
        search_button.setStyleSheet("font-size: 18px; padding: 10px;")
        search_button.clicked.connect(self.search_patient)

        layout.addWidget(QLabel("Hastane Seçin:", alignment=Qt.AlignCenter))
        layout.addWidget(self.hospital_combo, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("TC Kimlik No Girin:", alignment=Qt.AlignCenter))
        layout.addWidget(self.tc_input, alignment=Qt.AlignCenter)
        layout.addWidget(search_button, alignment=Qt.AlignCenter)

        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(50, 20, 50, 20)

        
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Erkek", "Kadın"])
        self.age_input = QLineEdit()

        self.form_layout.addRow(QLabel("Ad:"), self.name_input)
        self.form_layout.addRow(QLabel("Soyad:"), self.surname_input)
        self.form_layout.addRow(QLabel("Cinsiyet:"), self.gender_combo)
        self.form_layout.addRow(QLabel("Yaş:"), self.age_input)

        self.form_group = QWidget()
        self.form_group.setLayout(self.form_layout)
        self.form_group.setVisible(False)

        self.save_button = QPushButton("Kaydet")
        self.save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.save_button.clicked.connect(self.save_patient)
        self.save_button.setVisible(False)

        layout.addWidget(self.form_group)
        layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def search_patient(self):
        tc_no = self.tc_input.text()
        host=self.hospital_combo.currentText()
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        query = "SELECT * FROM patients WHERE tc_no = ? AND hospital = ?"
        cursor.execute(query, (tc_no, host))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            QMessageBox.information(self, "Hasta Bulundu", "Hasta mevcut. Teşhis sahnesine yönlendiriliyorsunuz.")
            
            self.main_window.switch_to_diagnosis_scene()
        else:
            QMessageBox.warning(self, "Hasta Bulunamadı", "Hasta bulunamadı, lütfen kayıt oluşturun.")
            self.form_group.setVisible(True)
            self.save_button.setVisible(True)

    def save_patient(self):
        tc_no = self.tc_input.text()
        name = self.name_input.text()
        surname = self.surname_input.text()
        gender = self.gender_combo.currentText()
        age = self.age_input.text()
        hospital = self.hospital_combo.currentText()

        if not (tc_no and name and surname and age):
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun.")
            return

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        try:
            # Hasta kaydını patients tablosuna ekle
            cursor.execute(
                "INSERT INTO patients (tc_no, name, surname, gender, age, hospital) VALUES (?, ?, ?, ?, ?, ?)",
                (tc_no, name, surname, gender, int(age), hospital)
            )
            conn.commit()

            QMessageBox.information(self, "Başarılı", "Hasta kaydedildi.")
            self.form_group.setVisible(False)
            self.save_button.setVisible(False)

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu TC Kimlik No zaten kayıtlı.")
        finally:
            conn.close()

        # Formu sıfırla
        self.name_input.setText('')
        self.surname_input.setText('')
        self.age_input.setText('')

class DiagnosisScene(QWidget):
    def __init__(self, main_window):
        
        
        super().__init__()
        self.main_window = main_window
        self.diagnostic_trees = load_diagnostic_trees()
        self.current_tree = None
        self.current_node = None
        self.questions_and_answers = []  # Store questions and answers
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # nav butons (forward, backward etc)
        nav_layout = QHBoxLayout()
        back_button = QPushButton("Geri")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        back_button.clicked.connect(self.main_window.switch_to_login_scene)
        nav_layout.addWidget(back_button)

        layout.addLayout(nav_layout)

        # hastalık hist table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Tarih", "Teşhis"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(QLabel("Hasta Teşhis Geçmişi:", alignment=Qt.AlignLeft))
        layout.addWidget(self.history_table)

        layout.addWidget(QLabel("Teşhis ağacını seçin ve soruları cevaplayın:", alignment=Qt.AlignCenter))

        self.tree_combo = QComboBox()
        self.tree_combo.setStyleSheet("font-size: 18px; padding: 5px;")
        self.tree_combo.addItems(self.diagnostic_trees.keys())
        layout.addWidget(self.tree_combo, alignment=Qt.AlignCenter)

        self.select_tree_button = QPushButton("Ağacı Seç")
        self.select_tree_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.select_tree_button.clicked.connect(self.load_tree)
        layout.addWidget(self.select_tree_button, alignment=Qt.AlignCenter)

        self.question_label = QLabel("")
        self.question_label.setStyleSheet("font-size: 18px; padding: 10px;")
        self.question_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.question_label, alignment=Qt.AlignCenter)

        self.yes_button = QPushButton("Evet")
        self.yes_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.yes_button.clicked.connect(lambda: self.answer_question("yes"))
        self.yes_button.setVisible(False)
        layout.addWidget(self.yes_button, alignment=Qt.AlignCenter)

        self.no_button = QPushButton("Hayır")
        self.no_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.no_button.clicked.connect(lambda: self.answer_question("no"))
        self.no_button.setVisible(False)
        layout.addWidget(self.no_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def load_patient_diagnoses(self):
        """Load the diagnosis history for the patient."""
        tc_no = self.main_window.login_scene.tc_input.text()  # tc no alış
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT date, protocol_number, final_diagnosis FROM diagnoses WHERE tc_no = ?",
            (tc_no,)
        )
        diagnoses = cursor.fetchall()
        conn.close()

        self.history_table.setRowCount(len(diagnoses))
        for row_idx, (date, protocol_number, diagnosis) in enumerate(diagnoses):
            self.history_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.history_table.setItem(row_idx, 1, QTableWidgetItem(protocol_number))
            self.history_table.setItem(row_idx, 2, QTableWidgetItem(diagnosis))


    def load_tree(self):
        tree_name = self.tree_combo.currentText()
        self.current_tree = self.diagnostic_trees.get(tree_name)
        self.current_node = self.current_tree  # root starting (1st)
        self.questions_and_answers = []  # reset questipons and answers
        self.next_question()

    def next_question(self):
        """Display the next question or diagnosis result."""
        if isinstance(self.current_node, dict):  # not sure ??
            question = list(self.current_node.keys())[0]
            self.question_label.setText(question)
            self.yes_button.setVisible(True)
            self.no_button.setVisible(True)
        else:  # If the node is a result
            self.question_label.setText(f"Teşhis: {self.current_node}")
            self.yes_button.setVisible(False)
            self.no_button.setVisible(False)
            self.save_diagnosis(self.current_node)
            self.question_label.setText('')

    def answer_question(self, answer):
        """Process the user's answer and navigate the tree."""
        if isinstance(self.current_node, dict):
            question = list(self.current_node.keys())[0]
            self.questions_and_answers.append((question, answer))  # storing the data
            self.current_node = self.current_node[question].get(answer)
            self.next_question()

    def save_diagnosis(self, final_diagnosis):
        """Save the diagnosis result to the database."""
        hospital_name = self.main_window.login_scene.hospital_combo.currentText()
        tc_no = self.main_window.login_scene.tc_input.text()  # TC kimlik no
        questions_and_answers_str = json.dumps(self.questions_and_answers, ensure_ascii=False)

        # hastanın ad ve soyadını veritabanından al
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, surname FROM patients WHERE tc_no = ?", (tc_no,))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            patient_name = f"{patient[0]} {patient[1]}"
        else:
            QMessageBox.warning(self, "Hata", "Hasta bulunamadı.")
            return

        # creation of protocol no
        protocol_number = generate_protocol_number(hospital_name)

        # diagnoses tablosunda aynı TC numarası varsa güncelle, yoksa yeni kayıt oluştur
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM diagnoses WHERE tc_no = ? AND hospital_name = ?",
            (tc_no, hospital_name)
        )
        existing_record = cursor.fetchone()

        if existing_record:
            # var olan teşhisi güncelle
            cursor.execute(
                "UPDATE diagnoses SET date = datetime('now'), patient_name = ?, questions_and_answers = ?, final_diagnosis = ?, protocol_number = ? WHERE tc_no = ? AND hospital_name = ?",
                (patient_name, questions_and_answers_str, final_diagnosis, protocol_number, tc_no, hospital_name)
            )
        else:
            # yeni teşhis kaydı ekle
            cursor.execute(
                "INSERT INTO diagnoses (date, hospital_name, patient_name, tc_no, questions_and_answers, final_diagnosis, protocol_number) VALUES (datetime('now'), ?, ?, ?, ?, ?, ?)",
                (hospital_name, patient_name, tc_no, questions_and_answers_str, final_diagnosis, protocol_number)
            )
        conn.commit()
        conn.close()

        QMessageBox.information(self, f"Teşhis: {final_diagnosis}", f"Teşhis başarıyla kaydedildi. Protokol Numarası: {protocol_number}.")
        self.main_window.login_scene.tc_input.setText('')
        self.main_window.switch_to_login_scene()


class ResultsScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # nav bıttons
        nav_layout = QHBoxLayout()
        back_button = QPushButton("Geri")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        back_button.clicked.connect(self.main_window.switch_to_login_scene)
        nav_layout.addWidget(back_button)

        layout.addLayout(nav_layout)

        layout.addWidget(QLabel("Sonuçlar ve geçmiş kayıtlar:"))

        self.setLayout(layout)

if __name__ == '__main__':
    setup_database()
    app = QApplication(sys.argv)
    main_window = DiagnosisApp()
    main_window.show()
    sys.exit(app.exec_())
