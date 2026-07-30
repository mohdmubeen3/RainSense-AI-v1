import joblib

feature_columns = joblib.load("models/feature_columns.pkl")

print("Total Features:", len(feature_columns))
print()

for i, col in enumerate(feature_columns, start=1):
    print(f"{i}. {col}")