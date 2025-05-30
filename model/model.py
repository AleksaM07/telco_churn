import os
import pickle
import inflection
import pandas as pd
import json
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, roc_auc_score)
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE


def get_env_var(key):
    val = os.getenv(key)
    if val:
        return val.strip()
    else:
        raise EnvironmentError(f"{key} not set")

def load_clean_data(csv_path):
    df = pd.read_csv(csv_path)
    df.drop(columns=['customerID'], inplace=True)

    df.columns = [inflection.underscore(col).replace(' ', '_') for col in df.columns]
    df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce').fillna(0.0)
    df.replace({'No phone service': 'No', 'No internet service': 'No'}, inplace=True)
    df['senior_citizen'] = df['senior_citizen'].map({0: 'No', 1: 'Yes'})
    df.dropna(inplace=True)
    df['churn'] = df['churn'].map({'Yes': 1, 'No': 0})
    return df


def build_preprocessor(df, target_col='churn'):
    num_cols = (df.select_dtypes(include=['int64', 'float64']).drop(columns=[target_col]).columns.tolist())
    cat_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()

    preprocessor = ColumnTransformer([
        ('num', MinMaxScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
    ])

    return preprocessor, num_cols, cat_cols


def get_scores(y_true, y_pred):
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
        'roc_auc': roc_auc_score(y_true, y_pred)
    }


def train_model(df,target_col='churn',test_size=0.2,random_state=1,smote_random_state=1,n_selected_features=13):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=test_size,random_state=random_state,stratify=y)
    # 2) Preprocess (fit on train, transform both)
    preprocessor, _, _ = build_preprocessor(df, target_col)
    X_train_scaled = preprocessor.fit_transform(X_train)
    X_test_scaled  = preprocessor.transform(X_test)
    # 3) SMOTE
    smote = SMOTE(random_state=smote_random_state)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)
    # 4) SelectKBest
    selector = SelectKBest(score_func=f_classif, k=n_selected_features)
    selector.fit(X_train_smote, y_train_smote)
    X_train_sel = selector.transform(X_train_smote)
    X_test_sel  = selector.transform(X_test_scaled)
    # 5) Train model
    model = LGBMClassifier(
        random_state=random_state,
        num_leaves=10,
        n_estimators=175,
        learning_rate=0.01
    )
    model.fit(X_train_sel, y_train_smote)
    # 6) Evaluate on TEST set
    y_pred = model.predict(X_test_sel)
    scores = get_scores(y_test, y_pred)
    for metric, val in scores.items():
        print(f"  {metric:8s}: {val:.4f}")
    # 7) capture selected feature names
    feature_names = (preprocessor.get_feature_names_out())
    selected_features = feature_names[selector.get_support()]

    return model, preprocessor, selector, selected_features, scores


def save_artifacts(model,
                   preprocessor,
                   selector,
                   metrics,
                   artifacts_dir='/opt/airflow/model/artifacts'):
    os.makedirs(artifacts_dir, exist_ok=True)

    with open(os.path.join(artifacts_dir, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)

    with open(os.path.join(artifacts_dir, 'preprocessor.pkl'), 'wb') as f:
        pickle.dump(preprocessor, f)

    with open(os.path.join(artifacts_dir, 'selector.pkl'), 'wb') as f:
        pickle.dump(selector, f)

    metrics_path = os.path.join(artifacts_dir, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)

    print(f"Artifacts saved to: {artifacts_dir}/")


def main():
    csv_path = get_env_var('CSV_PATH')
    #csv_path = "C:\\Users\\aleks\\OneDrive\\Desktop\\Aleksie kerefeke\\Python_Exercise\\a1-churn\\telco_churn_etl\\data\\raw\\Telco-Customer-Churn.csv"

    df = load_clean_data(csv_path)

    model, preprocessor, selector, sel_feats, scores = train_model(df,test_size=0.2,random_state=1,smote_random_state=1,n_selected_features=13)

    print("\nSelected features:")
    for feat in sel_feats:
        print("  -", feat)

    save_artifacts(model, preprocessor, selector, scores)


if __name__ == '__main__':
    main()