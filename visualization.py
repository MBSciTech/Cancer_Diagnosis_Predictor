import matplotlib.pyplot as plt

def visualize_probabilities(probabilities):
    fig,axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].barh(list(probabilities.keys()), list(probabilities.values()), color="skyblue", edgecolor="black")
    axes[0].set_xlabel("Probability (%)")
    axes[0].set_ylabel("Cancer Type")
    axes[0].set_title("Cancer Prediction Results")
    axes[0].set_xlim(0, 100)
    axes[0].grid(axis="x", linestyle="--", alpha=0.7)
    
    for index, value in enumerate(probabilities.values()):
        axes[0].text(value + 2, index, f"{value:.2f}%", va='center', fontsize=10)

    axes[1].pie(probabilities.values(), labels=probabilities.keys(), autopct="%1.1f%%", startangle=140, colors=["skyblue", "orange", "green", "red", "purple", "pink"])
    axes[1].set_title("Cancer Probability Distribution")

    plt.tight_layout()
    plt.show()
