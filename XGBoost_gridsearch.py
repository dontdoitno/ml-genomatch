import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.utils import resample

# --- Загрузка и подготовка данных ---
df = pd.read_csv("processed/transplant_data.csv")

# Удаляем потенциальный leakage-признак
df = df.drop(columns=["engraftment_days"])

# Удаляем строки с пропущенной целевой переменной
df = df.dropna(subset=["engraftment_success"])

# Целевая переменная и признаки
X = df.drop(columns=["engraftment_success"])
y = df["engraftment_success"]

# Апсемплинг для балансировки классов
df_full = pd.concat([X, y], axis=1)
df_majority = df_full[df_full["engraftment_success"] == 1.0]
df_minority = df_full[df_full["engraftment_success"] == 0.0]
df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)
df_balanced = pd.concat([df_majority, df_minority_upsampled])
X = df_balanced.drop(columns=["engraftment_success"])
y = df_balanced["engraftment_success"]

# Обработка категориальных признаков
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
if cat_cols:
    empty_cat_cols = [col for col in cat_cols if X[col].isna().all()]
    X = X.drop(columns=empty_cat_cols)
    cat_cols = [col for col in cat_cols if col not in empty_cat_cols]
    cat_imputer = SimpleImputer(strategy='most_frequent')
    X[cat_cols] = pd.DataFrame(
        cat_imputer.fit_transform(X[cat_cols]),
        columns=cat_cols,
        index=X.index
    )
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

# Обработка числовых признаков
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
if num_cols:
    num_imputer = SimpleImputer(strategy='mean')
    X[num_cols] = pd.DataFrame(
        num_imputer.fit_transform(X[num_cols]),
        columns=num_cols,
        index=X.index
    )
    scaler = StandardScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])

# --- Grid Search для XGBoost ---
param_grid = {
    'max_depth': [3, 4, 5],
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [50, 100]
}

xgb = XGBClassifier(
    objective="binary:logistic",
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42
)

grid_search = GridSearchCV(
    estimator=xgb,
    param_grid=param_grid,
    scoring='roc_auc',
    cv=3,
    verbose=1,
    n_jobs=-1
)

grid_search.fit(X, y)

# --- Результаты ---
print("Лучшие параметры:", grid_search.best_params_)
print("Лучший AUC (по 3-фолд кросс-валидации):", grid_search.best_score_)
