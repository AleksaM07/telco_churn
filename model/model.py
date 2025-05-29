import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import roc_auc_score, f1_score
from lightgbm import LGBMClassifier
import pickle
import os

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df.dropna(inplace=True)
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    return df

def build_preprocessor(df, target_col='Churn'):
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'bool']).drop(columns=[target_col]).columns.tolist()

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
    ])
    return preprocessor, numerical_cols, categorical_cols

def train_model(df, target_col='Churn'):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    preprocessor, num_cols, cat_cols = build_preprocessor(df, target_col)
    X_transformed = preprocessor.fit_transform(X)

    model = LGBMClassifier(random_state=42)
    model.fit(X_transformed, y)

    preds = model.predict(X_transformed)
    auc = roc_auc_score(y, preds)
    f1 = f1_score(y, preds)

    print(f"AUC: {auc:.4f}")
    print(f"F1 Score: {f1:.4f}")

    return model, preprocessor

def save_artifacts(model, preprocessor, path='model/artifacts'):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    with open(os.path.join(path, 'preprocessor.pkl'), 'wb') as f:
        pickle.dump(preprocessor, f)
    print(f"Artifacts saved to: {path}/")

def main():
    csv_path = 'data/Telco-Customer-Churn.csv'  # adjust as needed
    df = load_data(csv_path)
    model, preprocessor = train_model(df)
    save_artifacts(model, preprocessor)

if __name__ == '__main__':
    main()