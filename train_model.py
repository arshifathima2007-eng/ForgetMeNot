import os
import pandas as pd
import joblib

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# ============================================
# PATHS
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")


# ============================================
# LOAD DATASET
# ============================================

print("\n========================================")
print("       FORGETMENOT AI TRAINING")
print("========================================")

data = pd.read_csv(DATASET_PATH)

print("\nDataset loaded successfully!")
print("Total rows:", len(data))


# ============================================
# CLEAN DATA
# ============================================

for column in ["destination", "activity", "category"]:

    data[column] = (
        data[column]
        .astype(str)
        .str.strip()
        .str.lower()
    )


# ============================================
# INPUT / OUTPUT
# ============================================

X = data[["destination", "activity"]]

y = data["category"]


# ============================================
# ENCODING
# ============================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            ["destination", "activity"]
        )

    ]
)


# ============================================
# DECISION TREE
# ============================================

model = DecisionTreeClassifier(

    random_state=42,

    max_depth=None,

    min_samples_split=2,

    min_samples_leaf=1

)


# ============================================
# PIPELINE
# ============================================

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",
            model
        )

    ]

)


# ============================================
# TRAIN
# ============================================

print("\n========================================")
print("TRAINING MODEL")
print("========================================")

pipeline.fit(X, y)

print("Training completed!")


# ============================================
# TRAINING ACCURACY
# ============================================

predictions = pipeline.predict(X)

accuracy = accuracy_score(y, predictions)

print("\nTraining Accuracy:")
print(round(accuracy * 100, 2), "%")


# ============================================
# TEST INPUTS
# ============================================

print("\n========================================")
print("TESTING IMPORTANT INPUTS")
print("========================================")


test_inputs = pd.DataFrame({

    "destination": [

        "college",
        "college",
        "college",
        "college",

        "school",

        "gym",

        "beach",

        "airport",

        "office",

        "hospital",

        "library",

        "shopping"

    ],

    "activity": [

        "presentation",
        "exam",
        "study",
        "project",

        "sports",

        "workout",

        "swimming",

        "flight",

        "meeting",

        "checkup",

        "reading",

        "grocery"

    ]

})


test_predictions = pipeline.predict(test_inputs)


for i in range(len(test_inputs)):

    destination = test_inputs.iloc[i]["destination"]

    activity = test_inputs.iloc[i]["activity"]

    prediction = test_predictions[i]

    print(
        destination,
        "+",
        activity,
        "→",
        prediction
    )


# ============================================
# SAVE MODEL
# ============================================

print("\n========================================")
print("SAVING MODEL")
print("========================================")

joblib.dump(
    pipeline,
    MODEL_PATH
)

print("\nModel saved successfully!")

print(
    "Location:",
    MODEL_PATH
)


print("\n========================================")
print("TRAINING COMPLETED")
print("========================================\n")