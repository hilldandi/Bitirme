✨ Add patient diagnosis system with dynamic decision tree and file storage

This commit introduces a comprehensive Python-based system for diagnosing
patients using a dynamic decision tree. The program interacts with users to 
collect patient information, traverse a diagnosis tree, and store the data 
persistently in JSON files. 

## Key Features:
1. **Patient Registration**:
   - Collects the patient's full name.
   - Generates a unique 11-digit patient ID starting from "00000000001".
   - Creates a JSON file for each patient in the `DiagnosesSystem` directory.
   - Each JSON file includes patient ID, name, and visit history.

2. **Symptom Collection**:
   - Users can input a list of symptoms during each visit.
   - Input is terminated when the user types "done".

3. **Dynamic Diagnosis Tree**:
   - Implements a customizable decision tree (`tehis_agaci`).
   - Asks relevant questions based on the user's responses (`yes`/`no`).
   - Determines the diagnosis based on the traversed path.

4. **Visit Recording**:
   - Logs the symptoms and diagnosis of each visit in the patient's JSON file.
   - Appends visit data to maintain a complete visit history.

5. **File Structure**:
   - Creates and saves patient JSON files in the `DiagnosesSystem` directory.
   - File names follow the format: `<PatientName>_<PatientID>.json`.

6. **Example JSON Structure**:
   ```json
   {
       "id": "00000000001",
       "name": "Ali Veli",
       "visits": [
           {
               "symptoms": ["Ateş", "Öksürük"],
               "diagnosis": "Grip"
           }
       ]
   }
