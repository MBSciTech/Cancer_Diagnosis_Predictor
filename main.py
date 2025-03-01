from cancer_model import CancerPredictor
from utils import get_user_input, read_file_input, view_patient_data
from data_storage import save_patient_data
from visualization import visualize_probabilities

def main():
    while True:
        print("\n🔬 Welcome to the Cancer Diagnosis Predictor 🔬")
        print("1. Enter Patient Data Manually")
        print("2. Upload Data File")
        print("3. View Previous Results")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_data = get_user_input()
            if not user_data:
                print("Invalid input. Returning to menu...")
                continue
            
            predictor = CancerPredictor(**user_data)
            probabilities = predictor.predict_cancer()

            print("\n📊 Cancer Probability Results:")
            for cancer, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
                print(f"{cancer}: {prob:.2f}% probability")

            most_probable = max(probabilities, key=probabilities.get)
            print(f"\n🔴 Most Likely Cancer: {most_probable} ({probabilities[most_probable]:.2f}%)")
            visualize_probabilities(probabilities)
            
            # Save patient data & graph
            save_patient_data(user_data, probabilities)

        elif choice == "2":
            read_file_input()

        elif choice == "3":
            view_patient_data()

        elif choice == "4":
            print("Exiting the program. Stay healthy! 🩺")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


main()
