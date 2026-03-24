import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import uuid
import os

def save_plot(title="Graph"):
    os.makedirs("graph", exist_ok=True)

    filename = f"graph/{uuid.uuid4().hex}.png"

    plt.title(title)
    plt.savefig(filename)
    plt.close()

    return filename