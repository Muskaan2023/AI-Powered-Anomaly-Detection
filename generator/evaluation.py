import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

data = pd.read_csv(
    DATA_DIR / "predictions.csv"
)
data["actual"] = data["label"].map({
    "Normal":0,
    "Attack":1
})
data["predicted"] = data["prediction"].map({
    1:0,
    -1:1
})
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
accuracy = accuracy_score(
    data["actual"],
    data["predicted"]
)

print("Accuracy:", accuracy)
precision = precision_score(
    data["actual"],
    data["predicted"]
)

print("Precision:", precision)
recall = recall_score(
    data["actual"],
    data["predicted"]
)

print("Recall:", recall)
f1 = f1_score(
    data["actual"],
    data["predicted"]
)

print("F1 Score:", f1)
cm = confusion_matrix(
    data["actual"],
    data["predicted"]
)

print(cm)
