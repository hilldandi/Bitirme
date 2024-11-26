import tkinter as tk
from tkinter import messagebox
import uuid

tehis_agaci = {
    "question": "Ateş var mı?",
    "yes": {
        "question": "Öksürük var mı?",
        "yes": {
            "question": "Öksürüğünüz kuru mu?",
            "yes": {
                "question": "Boğaz ağrısı var mı?",
                "yes": "Grip",
                "no": "Sinüzit"
            },
            "no": {
                "question": "Nefes almakta zorlanıyor musunuz?",
                "yes": "Astım/Bronşit",
                "no": {
                    "question": "Ciltte döküntü var mı?",
                    "yes": "Alerjik Reaksiyon",
                    "no": "Mide Problemleri"
                }
            }
        },
        "no": {
            "question": "Burun akıntısı var mı?",
            "yes": {
                "question": "Gözde sulanma var mı?",
                "yes": "Alerjik Rinit",
                "no": "Sinüzit"
            },
            "no": {
                "question": "İshal ve karın ağrısı var mı?",
                "yes": "Mide Problemleri",
                "no": "Diğer"
            }
        }
    },
    "no": {
        "question": "Yorgunluk hissediyor musunuz?",
        "yes": "Alerjik Reaksiyon",
        "no": "Diğer"
    }
}

# Id creator but we will change it with randit function
def generate_patient_id():
    return str(uuid.uuid4())[:8]  # Kısa bir UUID üretir

# app
class DiagnosisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teşhis Uygulaması")

        self.patient_id = generate_patient_id()
        self.current_node = tehis_agaci  # Ağacın başlangıcı

        # id label
        self.id_label = tk.Label(root, text=f"Hasta ID: {self.patient_id}", font=("Arial", 12))
        self.id_label.pack(pady=10)

        # question area
        self.question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        # y/n?
        self.yes_button = tk.Button(root, text="Evet", width=10, command=lambda: self.answer_question("yes"))
        self.yes_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.no_button = tk.Button(root, text="Hayır", width=10, command=lambda: self.answer_question("no"))
        self.no_button.pack(side=tk.RIGHT, padx=20, pady=10)

        # showing the root of the tree
        self.show_next_question()

    def show_next_question(self):
        if isinstance(self.current_node, str):  # Teşhis varsa
            messagebox.showinfo("Teşhis", f"Teşhisiniz: {self.current_node}")
            self.root.destroy()
        else:
            self.question_label.config(text=self.current_node["question"])

    def answer_question(self, answer):
        if answer in self.current_node:
            self.current_node = self.current_node[answer]
            self.show_next_question()
        else:
            messagebox.showerror("Hata", "Geçersiz yanıt. Lütfen tekrar deneyin.")

# starting state
if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosisApp(root)
    root.mainloop()
