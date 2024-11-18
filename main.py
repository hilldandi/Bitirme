import tkinter as tk
from tkinter import messagebox
import uuid

# Sorular ve teşhis sonuçlarını içeren yapı
tehis_agaci = {
    "Boğaz ağrısı var mı?": {
        "Evet": {
            "Öksürüğünüz kuru mu?": {
                "Evet": "Grip",
                "Hayır": "Sinüzit",
            }
        },
        "Hayır": {
            "Nefes almakta zorlanıyor musunuz?": {
                "Evet": {
                    "Gözlerde sulama var mı?": {
                        "Evet": "Alerjik Rinit",
                        "Hayır": "Astım/Bronşit",
                    }
                },
                "Hayır": "Ciltte döküntü var mı?",
            }
        },
    },
    # Diğer soruları ekleyebilirsiniz
}

# Hasta ID oluşturucu
def generate_patient_id():
    return str(uuid.uuid4())[:8]  # Kısa bir UUID üretir

# Uygulama ana sınıfı
class DiagnosisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teşhis Uygulaması")

        self.patient_id = generate_patient_id()
        self.current_question = None
        self.tree_pointer = tehis_agaci  # Ağacın başlangıcı

        # Hasta ID etiketi
        self.id_label = tk.Label(root, text=f"Hasta ID: {self.patient_id}", font=("Arial", 12))
        self.id_label.pack(pady=10)

        # Soru alanı
        self.question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        # Evet ve Hayır butonları
        self.yes_button = tk.Button(root, text="Evet", width=10, command=lambda: self.answer_question("Evet"))
        self.yes_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.no_button = tk.Button(root, text="Hayır", width=10, command=lambda: self.answer_question("Hayır"))
        self.no_button.pack(side=tk.RIGHT, padx=20, pady=10)

        # İlk soruyu göster
        self.show_next_question()

    def show_next_question(self):
        if isinstance(self.tree_pointer, str):  # Teşhis varsa
            messagebox.showinfo("Teşhis", f"Teşhisiniz: {self.tree_pointer}")
            self.root.destroy()
        else:
            self.current_question = list(self.tree_pointer.keys())[0]
            self.question_label.config(text=self.current_question)

    def answer_question(self, answer):
        if answer in self.tree_pointer[self.current_question]:
            self.tree_pointer = self.tree_pointer[self.current_question][answer]
            self.show_next_question()
        else:
            messagebox.showerror("Hata", "Geçersiz yanıt. Lütfen tekrar deneyin.")

# Uygulama başlatma
if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosisApp(root)
    root.mainloop()
