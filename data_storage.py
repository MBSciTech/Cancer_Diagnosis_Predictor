import os
import matplotlib.pyplot as plt

def save_patient_data(patient_data, probabilities):
    patient_name = input("📂 Enter patient's name otherwise just press enter: ").strip()
    if not patient_name:
        print("Data not saved.")
        return

    main_directory = "patients_details"
    os.makedirs(main_directory, exist_ok=True)
    
    patient_directory = os.path.join(main_directory, patient_name)
    os.makedirs(patient_directory, exist_ok=True)

    report_filename = os.path.join(patient_directory, f"{patient_name}_report.txt")
    graph_filename = os.path.join(patient_directory, f"{patient_name}_graph.png")

    try:
        with open(report_filename, "w", encoding="utf-8") as file:
            file.write("============================================\n")
            file.write("       🏥 CANCER DIAGNOSIS REPORT 🏥        \n")
            file.write("============================================\n\n")
            file.write(f"🩺 Name: {patient_name}\n")
            file.write(f"📅 Age: {patient_data['age']}\n")
            file.write(f"🚬 Smoking Habit: {'Never' if patient_data['smoking'] == 0 else 'Occasionally' if patient_data['smoking'] == 1 else 'Regularly'}\n")
            file.write(f"⚖️ BMI: {patient_data['bmi']}\n")
            file.write(f"🩸 WBC Count: {patient_data['wbc']} per µL\n")
            file.write(f"🔬 PSA Level: {patient_data['psa']} ng/mL\n")
            file.write(f"🔬 CA-125 Level: {patient_data['ca125']} U/mL\n")
            file.write(f"🩺 CRP Level: {patient_data['crp']} mg/L\n")
            file.write(f"📸 Tumor Detected: {'Yes' if patient_data['tumor_detected'] else 'No'}\n\n")
            file.write("=====================================================\n")
            file.write("           🏥 DIAGNOSIS SUMMARY 🏥         \n")
            file.write("=====================================================\n\n")
            
            file.write("📊 Cancer Probability Results:\n")
            for cancer, prob in probabilities.items():
                file.write(f"   - {cancer}: {prob:.2f}% probability\n")
            
            # Most likely cancer
            most_probable = max(probabilities, key=probabilities.get)
            file.write(f"\n🔴 Most Likely Cancer: {most_probable} ({probabilities[most_probable]:.2f}%)\n")
            
            file.write("\n============================================\n")
            file.write("    🩺 Please consult a doctor for further analysis. 🩺\n")
            file.write("============================================\n")

        print(f"✅ Patient data saved in: {report_filename}")

        axes = plt.subplots(1, 2, figsize=(12, 5))

        #Bar Chart
        axes[0].barh(list(probabilities.keys()), list(probabilities.values()), color="skyblue", edgecolor="black")
        axes[0].set_xlabel("Probability (%)")
        axes[0].set_ylabel("Cancer Type")
        axes[0].set_title(f"Cancer Prediction for {patient_name}")
        axes[0].set_xlim(0, 100)
        axes[0].grid(axis="x", linestyle="--", alpha=0.7)

        for index, value in enumerate(probabilities.values()):
            axes[0].text(value + 2, index, f"{value:.2f}%", va='center', fontsize=10)

        #Pie Chart
        axes[1].pie(probabilities.values(), labels=probabilities.keys(), autopct="%1.1f%%", startangle=140, colors=["skyblue", "orange", "green", "red", "purple", "pink"])
        axes[1].set_title("Cancer Probability Distribution")

        plt.tight_layout()
        plt.savefig(graph_filename)
        plt.close()

        print(f"✅ Probability graphs saved in: {graph_filename}")

    except Exception as e:
        print(f"❌ Error saving data: {e}")
