import os
from cancer_model import CancerPredictor
from data_storage import save_patient_data
from visualization import visualize_probabilities

def get_user_input():
    try:
        print("\n📝 Enter Patient Medical Data:")
        gender = input("Gender (Male/Female): ").strip().lower()
        if gender not in ["male", "female"]:
            print("❌ Invalid gender. Please enter Male or Female.")
            return None

        age = int(input("Age: "))
        smoking = int(input("Smoking Habit (0 - Never, 1 - Occasionally, 2 - Regularly): "))
        bmi = float(input("Body Mass Index (BMI): "))
        wbc = int(input("White Blood Cell Count (WBC per µL, normal: 4000-11000): "))
        psa = float(input("PSA Level (Prostate-Specific Antigen, normal: <4 ng/mL, males only): "))
        ca125 = float(input("CA-125 Level (normal: <35 U/mL, females only): "))
        crp = float(input("C-Reactive Protein (CRP, normal: <10 mg/L): "))
        plt = int(input("Platelet Count (PLT per µL, normal: 150000-450000): "))
        rbc = float(input("Red Blood Cell Count (RBC, normal: 4.2-5.9 M/uL): "))
        hb = float(input("Hemoglobin Level (Hb, normal: 12-17 g/dL): "))
        tumor_detected = int(input("Tumor Detected in Scan? (0 - No, 1 - Yes): "))

        return {
            "gender": gender,
            "age": age,
            "smoking": smoking,
            "bmi": bmi,
            "wbc": wbc,
            "psa": psa,
            "ca125": ca125,
            "crp": crp,
            "plt": plt,
            "rbc": rbc,
            "hb": hb,
            "tumor_detected": tumor_detected
        }

    except ValueError:
        print("❌ Invalid input! Please enter numeric values only.")
        return None

def read_file_input():    
    folder_path = "Predefine_data"
    if not os.path.exists(folder_path):
        print("❌ Folder 'Predefine_data' not found. Please create it and add patient data files.")
        return

    # Get all .txt files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    
    if not files:
        print("❌ No patient data files found in 'Predefine_data'.")
        return

    # Display available files as a menu
    print("\n📂 Choose a patient data file to upload:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    # Get user selection
    try:
        choice = int(input("\nEnter the number of the file: ")) - 1
        if choice < 0 or choice >= len(files):
            print("❌ Invalid choice. Returning to menu...")
            return

        selected_file = files[choice]
        file_path = os.path.join(folder_path, selected_file)

        # Read and process the selected file
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Parse patient data from file
        patient_data = {}
        for line in lines:
            key, value = line.strip().split(": ")
            patient_data[key.lower().replace(" ", "_")] = value

        patient_data["age"] = int(patient_data["age"])
        patient_data["smoking"] = int(patient_data["smoking"])
        patient_data["bmi"] = float(patient_data["bmi"])
        patient_data["wbc"] = int(patient_data["wbc"])
        patient_data["psa"] = float(patient_data["psa"])
        patient_data["ca125"] = float(patient_data["ca125"])
        patient_data["crp"] = float(patient_data["crp"])
        patient_data["plt"] = int(patient_data["plt"])
        patient_data["rbc"] = float(patient_data["rbc"])
        patient_data["hb"] = float(patient_data["hb"])
        patient_data["tumor_detected"] = int(patient_data["tumor_detected"])

        predictor = CancerPredictor(**patient_data)
        probabilities = predictor.predict_cancer()

        print("\n📊 Cancer Probability Results:")
        for cancer, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
            print(f"{cancer}: {prob:.2f}% probability")

        most_probable = max(probabilities, key=probabilities.get)
        print(f"\n🔴 Most Likely Cancer: {most_probable} ({probabilities[most_probable]:.2f}%)")
        visualize_probabilities(probabilities)
        save_patient_data(patient_data, probabilities)

    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"❌ Error processing file: {e}")
def list_patient_folders():
    """Lists all available patient folders inside 'patients_details/'."""
    base_dir = "patients_details"
    
    if not os.path.exists(base_dir):
        print("❌ No patient records found.")
        return None

    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    
    if not folders:
        print("❌ No patient records found.")
        return None

    print("\n📂 Choose whose data you want to read:")
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")

    return folders

def view_patient_data():
    folders = list_patient_folders()
    if not folders:
        return
    
    try:
        choice = int(input("\nEnter the number of the patient: ")) - 1
        if choice < 0 or choice >= len(folders):
            print("❌ Invalid choice. Returning to menu...")
            return

        selected_patient = folders[choice]
        patient_dir = os.path.join("patients_details", selected_patient)
        report_file = os.path.join(patient_dir, f"{selected_patient}_report.txt")
        graph_file = os.path.join(patient_dir, f"{selected_patient}_graph.png")

        # Print the report
        if os.path.exists(report_file):
            print("\n📄 Patient Report:")
            with open(report_file, "r", encoding="utf-8") as file:
                print(file.read())
        else:
            print("❌ Report file not found.")

        # Show the graph
        if os.path.exists(graph_file):
            print("\n🖼 Displaying Graph...")
            import matplotlib.pyplot as plt
            img = plt.imread(graph_file)
            plt.imshow(img)
            plt.axis("off")
            plt.show()
        else:
            print("❌ Graph file not found.")

    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")
