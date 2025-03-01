import numpy as np

class CancerPredictor:

    CANCER_PRIORS = {
        "Lung Cancer": 0.13,
        "Breast Cancer": 0.11,
        "Prostate Cancer": 0.12,
        "Leukemia": 0.10,
        "Ovarian Cancer": 0.08,
        "Colon Cancer": 0.09
    }

    BLOOD_MARKER_STATS = {
        "WBC": {"mean": 7000, "std": 2000},
        "PSA": {"mean": 3, "std": 1.5},
        "CA125": {"mean": 15, "std": 10},
        "CRP": {"mean": 5, "std": 3},
        "PLT": {"mean": 250000, "std": 50000},
        "RBC": {"mean": 5.0, "std": 0.5},       
        "Hb": {"mean": 14, "std": 2}            
    }

    def __init__(self, gender, age, smoking, bmi, wbc, psa, ca125, crp, plt, rbc, hb, tumor_detected):
        self.gender = gender.lower()
        self.age = age
        self.smoking = smoking
        self.bmi = bmi
        self.wbc = wbc
        self.psa = psa
        self.ca125 = ca125
        self.crp = crp
        self.plt = plt  
        self.rbc = rbc  
        self.hb = hb    
        self.tumor_detected = tumor_detected

    def normal_distribution_probability(self, value, marker):
        mean = self.BLOOD_MARKER_STATS[marker]["mean"]
        std = self.BLOOD_MARKER_STATS[marker]["std"]
        z_score = (value - mean) / std
        probability = np.exp(-0.5 * z_score**2) / (std * np.sqrt(2 * np.pi))
        return probability if value > mean else 1 - probability

    def predict_cancer(self):
        probabilities = {}

        for cancer in self.CANCER_PRIORS:
            if self.gender == "male" and cancer in ["Breast Cancer", "Ovarian Cancer"]:
                continue

            prior = self.CANCER_PRIORS[cancer]

            age_factor = 1.6 if self.age > 50 else 1.2
            smoking_factor = 2.5 if (self.smoking == 2 and cancer == "Lung Cancer") else 1.0
            bmi_factor = 1.4 if self.bmi > 30 and cancer in ["Breast Cancer", "Prostate Cancer", "Colon Cancer"] else 1.0
            tumor_factor = 3.5 if self.tumor_detected else 1.0

            wbc_factor = self.normal_distribution_probability(self.wbc, "WBC")
            psa_factor = self.normal_distribution_probability(self.psa, "PSA") if cancer == "Prostate Cancer" else 1
            ca125_factor = self.normal_distribution_probability(self.ca125, "CA125") if cancer == "Ovarian Cancer" else 1
            crp_factor = self.normal_distribution_probability(self.crp, "CRP")
            plt_factor = self.normal_distribution_probability(self.plt, "PLT") if cancer == "Leukemia" else 1
            rbc_factor = self.normal_distribution_probability(self.rbc, "RBC") if cancer in ["Leukemia", "Colon Cancer"] else 1
            hb_factor = self.normal_distribution_probability(self.hb, "Hb") if cancer in ["Leukemia", "Colon Cancer"] else 1

            final_probability = prior * age_factor * smoking_factor * bmi_factor * tumor_factor
            final_probability *= wbc_factor * psa_factor * ca125_factor * crp_factor * plt_factor * rbc_factor * hb_factor

            probabilities[cancer] = final_probability

        
        total = sum(probabilities.values())
        for cancer in probabilities:
            probabilities[cancer] = (probabilities[cancer] / total) * 100

        return probabilities
