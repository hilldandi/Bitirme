def record_visit(patient_name, patient_id, diagnosis_tree):
    file_path = os.path.join("DiagnosesSystem", f"{patient_name}_{patient_id}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            patient_data = json.load(f)

        """symptoms = []
        while True:
            symptom = input("Lütfen bir semptom girin (veya bitirmek için 'done' yazın): ").strip()
            if symptom.lower() == "done":
                break
            symptoms.append(symptom)"""
        
        #yukarıda yorum satırında olan yapı kullanıma açılabilirse tree takibi otomatik semptom girişi ile de sağlanabilecek. örn hasta oraya ateş,öksürük yazarsa direkt semptom bilgisi grip olarak verilecek
        

        diagnosis = traverse_diagnosis_tree(diagnosis_tree)

        patient_data["visits"].append({
            "symptoms": symptoms,
            "diagnosis": diagnosis
        })

        with open(file_path, 'w') as f:
            json.dump(patient_data, f, indent=4)
        print(f"\nTeşhis kaydedildi: {diagnosis}")
    else:
        print("Hasta dosyası bulunamadı!")
