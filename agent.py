import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid

def save_plot():
    os.makedirs("graph", exist_ok=True)
    filename = f"graph/{uuid.uuid4().hex}.png"
    plt.savefig(filename)
    plt.close()
    return filename


def create_agent(csv_path):
    df = pd.read_csv(csv_path)

    def ask_question(q):
        q_lower = q.lower()

        try:
            # 📊 BASIC
            if "average" in q_lower:
                return round(df["sales"].mean(), 2)

            elif "total" in q_lower or "sum" in q_lower:
                return df["sales"].sum()

            elif "max" in q_lower or "highest" in q_lower:
                return df["sales"].max()

            elif "min" in q_lower or "lowest" in q_lower:
                return df["sales"].min()

            elif "count" in q_lower:
                return len(df)

            # 🧠 ADVANCED
            elif "region" in q_lower and "highest" in q_lower:
                return df.groupby("region")["sales"].sum().idxmax()

            elif "product" in q_lower and "highest" in q_lower:
                return df.groupby("product")["sales"].sum().idxmax()

            elif "month" in q_lower and "highest" in q_lower:
                return df.groupby("month")["sales"].sum().idxmax()

            elif "profit" in q_lower:
                return df["profit"].sum()

            # 📈 PIE
            elif "pie" in q_lower:
                df.groupby("region")["sales"].sum().plot(kind="pie", autopct='%1.1f%%')
                return save_plot()

            # 📊 BAR
            elif "plot" in q_lower or "graph" in q_lower or "chart" in q_lower:
                df.groupby("region")["sales"].sum().plot(kind="bar")
                return save_plot()

            # 🤖 DEFAULT (अब better)
            else:
                return "Try: average, total, highest region, plot sales"

        except Exception as e:
            return str(e)

    return ask_question
