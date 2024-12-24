from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox, QButtonGroup, QComboBox
)
from models.data_management import record_visit


class SymptomsScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Ağaçlar ve semptomlar
        self.diagnosis_trees = {
            "Baş Ağrısı Ağacı 2": {
                "Baş ağrısı var mı?": {
                    "yes": {
                        "Baş ağrısı tekrarlayıcı mı?": {
                            "yes": {
                                "Baş ağrısı genellikle tek taraflı mı?": {
                                    "yes": {
                                        "Bulantı veya kusma var mı?": {
                                            "yes": "Migren",
                                            "no": {
                                                "Aura belirtileri (görsel rahatsızlıklar, karıncalanma vb.) var mı?": {
                                                    "yes": "Migren",
                                                    "no": "Tansiyon tipi baş ağrısı"
                                                }
                                            }
                                        }
                                    },
                                    "no": {
                                        "Ağrı ışık veya ses hassasiyeti yaratıyor mu?": {
                                            "yes": "Migren",
                                            "no": "Tansiyon tipi baş ağrısı"
                                        }
                                    }
                                }
                            },
                            "no": {
                                "Ağrı fiziksel aktiviteyle kötüleşiyor mu?": {
                                    "yes": "Migren",
                                    "no": "Diğer"
                                }
                            }
                        }
                    },
                    "no": {
                        "Başka belirtiler mevcut mu?": {
                            "yes": "Diğer",
                            "no": "Migren düşünülmez"
                        }
                    }
                }
            },
            "COVID-19 Ağacı": {
                "Ateşiniz var mı?": {
                    "yes": {
                        "Öksürüğünüz var mı?": {
                            "yes": {
                                "Nefes almakta zorluk çekiyor musunuz?": {
                                    "yes": "COVID-19 Olabilir",
                                    "no": {
                                        "Koku veya tat kaybı yaşadınız mı?": {
                                            "yes": "COVID-19 Olabilir",
                                            "no": "Soğuk Algınlığı veya Grip"
                                        }
                                    }
                                }
                            },
                            "no": {
                                "Son 14 gün içinde bir COVID-19 hastasıyla temasınız oldu mu?": {
                                    "yes": "COVID-19 Şüphesi (Test Önerilir)",
                                    "no": "Diğer Nedenler Araştırılmalı"
                                }
                            }
                        }
                    },
                    "no": {
                        "Aşı türünüzü biliyor musunuz?": {
                            "yes": {
                                "Hangi aşı türünü oldunuz? (mRNA/Vektör)": {
                                    "mRNA": {
                                        "Kaç doz oldunuz?": {
                                            "1-2": "COVID-19 Şüphesi Az",
                                            "3+": "COVID-19 Olasılığı Çok Düşük"
                                        }
                                    },
                                    "Vektör": {
                                        "Kaç doz oldunuz?": {
                                            "1-2": "COVID-19 Şüphesi Az",
                                            "3+": "COVID-19 Olasılığı Çok Düşük"
                                        }
                                    }
                                }
                            },
                            "no": {
                                "Son 14 gün içinde bir COVID-19 hastasıyla temasınız oldu mu?": {
                                    "yes": "COVID-19 Şüphesi (Test Önerilir)",
                                    "no": "COVID-19 Olasılığı Çok Düşük"
                                }
                            }
                        }
                    }
                }
            },
            "Ateş ve Öksürük Ağacı": {
                "Ateş var mı?": {
                    "yes": {
                        "Öksürük var mı?": {
                            "yes": {
                                "Öksürünüz kuru mu?": {
                                    "yes": {
                                        "Boğaz ağrısı var mı?": {
                                            "yes": "Grip",
                                            "no": "Sinüzit"
                                        }
                                    },
                                    "no": {
                                        "Nefes almakta zorlanıyor musunuz?": {
                                            "yes": "Astım/Bronşit",
                                            "no": "Mide Problemleri"
                                        }
                                    }
                                }
                            },
                            "no": "Diğer"
                        }
                    },
                    "no": "Diğer"
                }
            }
        }

        self.current_tree = None
        self.current_branch = None
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
        self.yes_button = QRadioButton("yes")
        self.no_button = QRadioButton("no")
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.yes_button)
        self.button_group.addButton(self.no_button)

        self.next_button = QPushButton("next")
        self.next_button.clicked.connect(self.next_question)

        self.back_button = QPushButton("back")
        self.back_button.clicked.connect(self.previous_question)

        self.save_exit_button = QPushButton("save and exit")
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
        if self.current_branch is None or isinstance(self.current_branch, str):
            # Teşhis ekranı
            self.question_label.setText(f"TEŞHİSİNİZ: {self.current_branch}")
            self.yes_button.hide()
            self.no_button.hide()
            self.next_button.hide()
            self.back_button.hide()
            self.save_exit_button.show()
        else:
            # Yeni soruyu göster
            self.question_label.setText(list(self.current_branch.keys())[0])
            self.yes_button.show()
            self.no_button.show()
            self.next_button.show()
            self.back_button.setVisible(len(self.selected_answers) > 0)
            self.save_exit_button.hide()

    def select_tree(self):
        """Seçilen teşhis ağacını başlatır."""
        tree_name = self.tree_selector.currentText()
        self.current_tree = self.diagnosis_trees[tree_name]
        self.current_branch = self.current_tree
        self.current_index = 0
        self.selected_answers = []
        self.update_ui()

    def next_question(self):
        """Bir sonraki soruya geçiş."""
        if not (self.yes_button.isChecked() or self.no_button.isChecked()):
            QMessageBox.warning(self, "Hata", "Lütfen bir seçim yapın!")
            return

        # Kullanıcının cevabını kaydet
        answer = "yes" if self.yes_button.isChecked() else "no"
        self.selected_answers.append((list(self.current_branch.keys())[0], answer))

        # Ağaçta bir sonraki dala geç
        self.current_branch = self.current_branch[list(self.current_branch.keys())[0]].get(answer, "Belirlenemedi")
        self.update_ui()

    def previous_question(self):
        """Bir önceki soruya dönüş."""
        if self.selected_answers:
            # Bir önceki cevabı kaldır
            last_question, last_answer = self.selected_answers.pop()

            # Ağaçta geri gitmek için dalları yeniden yükle
            self.current_branch = self.current_tree
            for question, answer in self.selected_answers:
                self.current_branch = self.current_branch[question][answer]
            self.update_ui()

    def save_and_exit(self):
        """Teşhisi kaydedip çıkışı sağlar."""
        if isinstance(self.current_branch, str):
            diagnosis = self.current_branch
        else:
            diagnosis = "Belirlenemedi"
        self.save_diagnosis(diagnosis)
        QMessageBox.information(self, "Çıkış", "Teşhisiniz kaydedildi. Uygulamadan çıkılıyor.")
        exit(0)

    def save_diagnosis(self, diagnosis):
        """Teşhisi JSON dosyasına kaydeder."""
        self.patient_id = "12345678901"  # Gerçek uygulamada bu değer dinamik olmalı
        formatted_answers = [
            {"question": question, "answer": answer}
            for question, answer in self.selected_answers
        ]
        record_visit(self.patient_id, diagnosis, formatted_answers)
