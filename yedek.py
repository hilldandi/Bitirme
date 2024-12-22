import os
import json
from datetime import datetime

# Klasör oluşturma (yoksa)
if not os.path.exists("DiagnosesSystem"):
    os.makedirs("DiagnosesSystem")

# Hasta bilgileri JSON dosyası
ID_INFO_FILE = os.path.join("DiagnosesSystem", "id_information.json")

# Hasta bilgileri yükleniyor
if os.path.exists(ID_INFO_FILE):
    with open(ID_INFO_FILE, 'r') as f:
        id_information = json.load(f)
else:
    id_information = {}  # {id: {"name": "Ad", "surname": "Soyad"}}

# Günlük kayıtlar
daily_records = {}  # Günlük hasta takibi {tarih: {"patient_count": sayı, "records": [{"id": ..., "diagnosis": ...}]}}

def load_daily_records():
    """Günlük kayıtları yükler."""
    global daily_records
    file_path = os.path.join("DiagnosesSystem", "date_patientNo.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            daily_records = json.load(f)

def save_daily_records():
    """Günlük kayıtları kaydeder."""
    file_path = os.path.join("DiagnosesSystem", "date_patientNo.json")
    with open(file_path, 'w') as f:
        json.dump(daily_records, f, indent=4)

def save_id_information():
    """Hasta bilgilerini id_information.json dosyasına kaydeder."""
    with open(ID_INFO_FILE, 'w') as f:
        json.dump(id_information, f, indent=4)

def create_patient_file(patient_id):
    """Hastaya özel JSON dosyasını oluşturur."""
    file_path = os.path.join("DiagnosesSystem", f"{patient_id}.json")
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({"id": patient_id, "visits": []}, f)

def record_visit(patient_id, diagnosis, symptoms):
    """Hastanın ziyaretini kaydeder."""
    file_path = os.path.join("DiagnosesSystem", f"{patient_id}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            patient_data = json.load(f)

        # Tarih ve teşhis bilgisi ekle
        visit_date = datetime.now().strftime("%Y-%m-%d")
        patient_data["visits"].append({
            "date": visit_date,
            "diagnosis": diagnosis,
            "symptoms": symptoms
        })

        # Hasta bilgilerini güncelle
        with open(file_path, 'w') as f:
            json.dump(patient_data, f, indent=4)

        # Günlük kayıtları güncelle
        if visit_date not in daily_records:
            daily_records[visit_date] = {"patient_count": 0, "records": []}
        daily_records[visit_date]["patient_count"] += 1
        daily_records[visit_date]["records"].append({
            "id": patient_id,
            "diagnosis": diagnosis
        })
        save_daily_records()
    else:
        print("Hasta dosyası bulunamadı!")

def traverse_diagnosis_tree(tree):
    """Teşhis ağacını dolaşır ve semptomları toplar."""
    symptoms = []
    while "question" in tree:
        answer = input(f"{tree['question']} (yes/no): ").strip().lower()
        symptoms.append({"question": tree["question"], "answer": answer})
        if answer == "yes":
            tree = tree["yes"]
        elif answer == "no":
            tree = tree["no"]
        else:
            print("Lütfen sadece 'yes' veya 'no' cevabını verin.")
    return tree, symptoms

def get_valid_id():
    """Geçerli bir TC kimlik numarası alır."""
    while True:
        patient_id = input("TC Kimlik Numarası (11 haneli): ").strip()
        if len(patient_id) == 11 and patient_id.isdigit():
            return patient_id
        print("Lütfen geçerli bir TC kimlik numarası giriniz (11 haneli olmaları).")

def main():
    """Programın ana fonksiyonu."""
    load_daily_records()

    # Teşhis ağaçları
    diagnosis_tree_1 = {
        "question": "Ateş var mı?",
        "yes": {
            "question": "Öksürük var mı?",
            "yes": {
                "question": "Öksürünüz kuru mu?",
                "yes": {
                    "question": "Boğaz ağrısı var mı?",
                    "yes": "Grip",
                    "no": "Sinüzit"
                },
                "no": {
                    "question": "Nefes almakta zorlanıyor musunuz?",
                    "yes": "Astım/Bronşit",
                    "no": "Mide Problemleri"
                }
            },
            "no": "Diğer"
        },
        "no": "Diğer"
    }

    diagnosis_tree_2 = {
        "question": "Baş ağrısı var mı?",
        "yes": {
            "question": "Baş ağrısı tekrarlayıcı mı?",
            "yes": "Migren",
            "no": "Tansiyon tipi baş ağrısı"
        },
        "no": "Diğer"
    }

    print("Sistem Başlatılıyor...")
    while True:
        print("Hangi teşhis ağacını kullanmak istersiniz?")
        print("1. Ateş ve Öksürük Ağacı")
        print("2. Baş Ağrısı Ağacı")
        tree_choice = input("Seçiminiz (1/2): ").strip()
        if tree_choice == "1":
            selected_tree = diagnosis_tree_1
            break
        elif tree_choice == "2":
            selected_tree = diagnosis_tree_2
            break
        else:
            print("Lütfen geçerli bir seçim yapınız (1 veya 2).")

    patient_id = get_valid_id()

    if patient_id in id_information:
        patient_name = id_information[patient_id]["name"]
        patient_surname = id_information[patient_id]["surname"]
        print(f"Hoş geldin {patient_surname}, {patient_name}.")
    else:
        patient_name = input("Adınız: ").strip()
        patient_surname = input("Soyadınız: ").strip()
        id_information[patient_id] = {"name": patient_name, "surname": patient_surname}
        save_id_information()
        create_patient_file(patient_id)

    diagnosis, symptoms = traverse_diagnosis_tree(selected_tree)
    record_visit(patient_id, diagnosis, symptoms)
    print(f"Teşhis kaydedildi: {diagnosis}")

if __name__ == "__main__":
    main()
