# FIX matplotlib backend (no GUI)
import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid

# FORCE SAVE GRAPH IN graph/
def custom_show(*args, **kwargs):
    os.makedirs("graph", exist_ok=True)
    filename = f"graph/{uuid.uuid4().hex}.png"
    plt.savefig(filename)
    plt.close()

# override show()
plt.show = custom_show


# AI Agent
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import Ollama


def create_agent(csv_path):
    df = pd.read_csv(csv_path)

    llm = Ollama(model="llama3")

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=False,
        allow_dangerous_code=True
    )

    return agent