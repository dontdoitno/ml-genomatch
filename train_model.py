import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBClassifier

# Загрузка данных
df = pd.read_csv('processed/transplant_data.csv')

# Целевые переменные
targets = ['engraftment_success', 'overall_survival_1y']

# Общая предобработка
def preprocess(df, target_column):
    df = df.copy()
    df = df[df[target_column].notna()]
    df = df[df[target_column].isin([0, 1])]
    y = df[target_column]
    X = df.drop(columns=targets)

    cat_cols = X.select_dtypes(include='object').columns.tolist()
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()

    # Remove empty categorical columns
    empty_cat_cols = [col for col in cat_cols if X[col].isna().all()]
    if empty_cat_cols:
        print(f"Removing empty categorical columns: {empty_cat_cols}")
        cat_cols = [col for col in cat_cols if col not in empty_cat_cols]
        X = X.drop(columns=empty_cat_cols)

    # Handle categorical columns
    if cat_cols:
        cat_imputer = SimpleImputer(strategy='most_frequent')
        X[cat_cols] = pd.DataFrame(
            cat_imputer.fit_transform(X[cat_cols]),
            columns=cat_cols,
            index=X.index
        )

    # Handle numeric columns
    if num_cols:
        num_imputer = SimpleImputer(strategy='mean')
        X[num_cols] = pd.DataFrame(
            num_imputer.fit_transform(X[num_cols]),
            columns=num_cols,
            index=X.index
        )

    # One-hot encode categorical columns
    if cat_cols:
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    # Scale numeric columns
    if num_cols:
        scaler = StandardScaler()
        X[num_cols] = scaler.fit_transform(X[num_cols])

    return X, y

# Универсальная функция обучения
def train_model(X_train, y_train, model_type):
    if model_type == 'random_forest':
        clf = RandomForestClassifier(random_state=42)
        param_grid = {
            'n_estimators': [100, 300, 500],
            'max_depth': [3, 5, 7],
            'min_samples_leaf': [1, 5, 10]
        }
    elif model_type == 'xgboost':
        clf = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
        param_grid = {
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5, 7],
            'n_estimators': [100, 300],
            'subsample': [0.8, 1.0]
        }
    else:
        raise ValueError("Unknown model type")

    grid = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid.fit(X_train, y_train)
    return grid.best_estimator_, grid.best_params_

# Основной пайплайн
def train_and_evaluate(X, y, target_name):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    for model_type in ['random_forest', 'xgboost']:
        model, best_params = train_model(X_train, y_train, model_type)
        print(f"\n===== {model_type.upper()} for {target_name} =====")
        print(f"Best params: {best_params}")

        y_pred = model.predict(X_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

        # Важность признаков
        if model_type == 'random_forest':
            importances = model.feature_importances_
        elif model_type == 'xgboost':
            importances = model.feature_importances_

        feature_importance = pd.Series(importances, index=X.columns)
        top_features = feature_importance.sort_values(ascending=False).head(20)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_features.values, y=top_features.index)
        plt.title(f"{model_type.upper()} - Feature Importances: {target_name}")
        plt.tight_layout()
        plt.show()

# Запуск
for target in targets:
    X, y = preprocess(df, target)
    train_and_evaluate(X, y, target)
