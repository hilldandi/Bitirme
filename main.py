import os
import json

# klasör oluşturma (yoksa)
if not os.path.exists("DiagnosesSystem"):
    os.makedirs("DiagnosesSystem")

#hasta id global variable
current_id = 1
#00000000001   tc kimlik gibi 11 hane olsun istediğimiz için formatlayacağız sonrasında
def generate_patient_id():
    global current_id
    patient_id = f"{current_id:011d}"
    current_id += 1
    return patient_id

def create_patient_file(patient_name, patient_id):
    # creating json files
    file_path = os.path.join("DiagnosesSystem", f"{patient_name}_{patient_id}.json")
    if not os.path.exists(file_path):  #w mi a mı dene sonra tekrar yaz bruayı
        with open(file_path, 'w') as f:
            json.dump({"id": patient_id, "name": patient_name, "visits": []}, f)
def traverse_diagnosis_tree(tree):
    #ree yapısını dolaşmayı sağlar
    # (emin değilim geliştirilmesi iyi olur)
    if "question" in tree:  #soru varsa işlemi başlat  
        #QT bakamadım daha qt öğrendikten sonra terminalden çıkartıp qt üzerinden seçim yaptırılacak
        answer = input(f"{tree['question']} (yes/no): ").strip().lower()
        if answer == "yes":
            return traverse_diagnosis_tree(tree["yes"])
        elif answer == "no":
            return traverse_diagnosis_tree(tree["no"])
        else:
            print("Lütfen sadece 'yes' veya 'no' cevabını verin.")
            return traverse_diagnosis_tree(tree)
    else: 
        return tree

#sistemin json üzerine her ziyareti kaydetmesi gerekiyor bunu hazırlayan kod parçası(?) altta
#olacak ama daha yazımı tam bitmedi yarım hali git içerisinde record.py içinde bulunuyor

def main():
    """Programın ana fonksiyonu."""
    #tree (just one)
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
    print("Welcome")
    patient_name = input("Name, Surname?? ").strip()
    patient_id = generate_patient_id()

    create_patient_file(patient_name, patient_id)
    print(f"\nPatient added to the DB {patient_name}, ID: {patient_id}")

    while True:
        record_visit(patient_name, patient_id, tehis_agaci)
        another = input("\nDo u want to save another patinet?(yes/no??): ").strip().lower()
        if another != "yes":
            break

    print("\nApp Ended")


if __name__ == "__main__":
    main()