import os
import json
from datetime import datetime
# Ana klasör ve alt klasör oluşturma

# Ana klasör ve alt klasör oluşturma
BASE_DIR = "DiagnosesSystem"
PATIENTS_DIR = os.path.join(BASE_DIR, "Patients")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

if not os.path.exists(PATIENTS_DIR):
    os.makedirs(PATIENTS_DIR)

# Hasta bilgileri JSON dosyası
ID_INFO_FILE = os.path.join(BASE_DIR, "id_information.json")

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
    file_path = os.path.join(BASE_DIR, "date_patientNo.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            daily_records = json.load(f)

def save_daily_records():
    """Günlük kayıtları kaydeder."""
    file_path = os.path.join(BASE_DIR, "date_patientNo.json")
    with open(file_path, 'w') as f:
        json.dump(daily_records, f, indent=4)

def save_id_information():
    """Hasta bilgilerini id_information.json dosyasına kaydeder."""
    with open(ID_INFO_FILE, 'w') as f:
        json.dump(id_information, f, indent=4)

def create_patient_file(patient_id):
    """Hastaya özel JSON dosyasını oluşturur."""
    file_path = os.path.join(PATIENTS_DIR, f"{patient_id}.json")
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({"id": patient_id, "visits": []}, f)

def record_visit(patient_id, diagnosis, symptoms):
    """Hastanın ziyaretini kaydeder."""
    file_path = os.path.join(PATIENTS_DIR, f"{patient_id}.json")
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

def get_valid_id():
    """Geçerli bir TC kimlik numarası alır."""
    while True:
        patient_id = input("TC Kimlik Numarası (11 haneli): ").strip()
        if len(patient_id) == 11 and patient_id.isdigit():
            return patient_id
        print("Lütfen geçerli bir TC kimlik numarası giriniz (11 haneli olmaları).")

def get_protocol_number():
    """Protokol numarası oluşturur."""
    today = datetime.now().strftime("%Y%m%d")
    if today not in daily_records:
        daily_records[today] = {"patient_count": 0, "records": []}
    daily_records[today]["patient_count"] += 1
    patient_count = daily_records[today]["patient_count"]
    save_daily_records()
    return f"{today}{patient_count:02d}"