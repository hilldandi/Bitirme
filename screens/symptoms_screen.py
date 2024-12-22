from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox, QButtonGroup, QComboBox
)
from models.data_management import record_visit


class SymptomsScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Ağaçlar ve semptomlar
        self.diagnosis_trees = {
            "Soğuk Algınlığı Ağacı": {
                "Baş ağrısı var mı?": {"yes": "Soğuk Algınlığı", "no": "Grip"},
                "Ateş var mı?": {"yes": "Grip", "no": "Soğuk Algınlığı"},
            },
            "Covid Ağacı": {
                "Öksürük var mı?": {"yes": "Covid", "no": "Soğuk Algınlığı"},
                "Ateş var mı?": {"yes": "Covid", "no": "Sağlıklı"},
            },
        }
        self.current_tree = None
        self.symptoms = []
        self.selected_answers = []
        self.current_index = 0
        self.patient_id = None  # Hasta ID'sini arayüzden alacağız

        # Arayüz elemanları
        self.layout = QVBoxLayout()
        self.tree_selector_label = QLabel("Teşhis Ağacını Seçin:")
        self.tree_selector = QComboBox()
        self.tree_selector.addItems(self.diagnosis_trees.keys())

        self.select_tree_button = QPushButton("Ağacı Seç ve Başla")
        self.select_tree_button.clicked.connect(self.select_tree)

        self.question_label = QLabel()
        self.yes_button = QRadioButton("Evet")
        self.no_button = QRadioButton("Hayır")
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.yes_button)
        self.button_group.addButton(self.no_button)

        self.next_button = QPushButton("İleri")
        self.next_button.clicked.connect(self.next_question)

        self.back_button = QPushButton("Geri")
        self.back_button.clicked.connect(self.previous_question)

        self.save_exit_button = QPushButton("Kaydet ve Çık")
        self.save_exit_button.clicked.connect(self.save_and_exit)

        # Layout elemanlarını ekle
        self.layout.addWidget(self.tree_selector_label)
        self.layout.addWidget(self.tree_selector)
        self.layout.addWidget(self.select_tree_button)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.yes_button)
        self.layout.addWidget(self.no_button)
        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.back_button)
        self.layout.addWidget(self.save_exit_button)

        self.setLayout(self.layout)
        self.update_ui()

    def update_ui(self):
        """Arayüzün durumunu günceller."""
        if self.current_tree is None:
            # Ağaç seçimi aşaması
            self.question_label.hide()
            self.yes_button.hide()
            self.no_button.hide()
            self.next_button.hide()
            self.back_button.hide()
            self.save_exit_button.hide()
        else:
            # Semptom sorgulama aşaması
            self.tree_selector_label.hide()
            self.tree_selector.hide()
            self.select_tree_button.hide()
            self.question_label.show()
            self.yes_button.show()
            self.no_button.show()
            self.next_button.show()
            self.back_button.show()
            self.save_exit_button.show()
            if self.current_index < len(self.symptoms):
                self.question_label.setText(self.symptoms[self.current_index])
            else:
                self.question_label.setText("Teşhis Tamamlandı.")

    def select_tree(self):
        """Seçilen teşhis ağacını başlatır."""
        tree_name = self.tree_selector.currentText()
        self.current_tree = self.diagnosis_trees[tree_name]
        self.symptoms = list(self.current_tree.keys())
        self.selected_answers = []
        self.current_index = 0
        self.update_ui()

    def next_question(self):
        """Bir sonraki soruya geçiş."""
        if self.yes_button.isChecked():
            self.selected_answers.append(("yes"))
        elif self.no_button.isChecked():
            self.selected_answers.append(("no"))
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir seçim yapın!")
            return

        self.current_index += 1
        if self.current_index >= len(self.symptoms):
            diagnosis = self.determine_diagnosis()
            QMessageBox.information(self, "Teşhis", f"TEŞHİSİNİZ: {diagnosis}")
            self.save_diagnosis(diagnosis)
        else:
            self.update_ui()

    def previous_question(self):
        """Bir önceki soruya dönüş."""
        if self.current_index > 0:
            self.current_index -= 1
            self.selected_answers.pop()
            self.update_ui()

    def determine_diagnosis(self):
        """Seçilen semptomlara göre teşhis belirler."""
        tree = self.current_tree
        for index, answer in enumerate(self.selected_answers):
            question = self.symptoms[index]
            if question in tree and answer in tree[question]:
                tree = tree[question][answer]
            else:
                break
        return tree if isinstance(tree, str) else "Belirlenemedi"

    def save_diagnosis(self, diagnosis):
        """Teşhisi JSON dosyasına kaydeder."""
        self.patient_id = "12345678901"  # Gerçek uygulamada bu değer dinamik olmalı
        formatted_answers = [
            {"question": self.symptoms[i], "answer": answer}
            for i, answer in enumerate(self.selected_answers)
        ]
        record_visit(self.patient_id, diagnosis, formatted_answers)

    def save_and_exit(self):
        """Teşhisi kaydedip çıkışı sağlar."""
        QMessageBox.information(self, "Çıkış", "Teşhisiniz kaydedildi. Uygulamadan çıkılıyor.")
        exit(0)
