import pandas as pd
import numpy as np
from xgboost import XGBClassifier, plot_importance
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import os
import joblib

# Загрузка данных
df = pd.read_csv("processed/transplant_data.csv")

# Удаляем потенциальный leakage-признак
df = df.drop(columns=["engraftment_days"])

# Удаляем строки с пропущенными значениями в целевой переменной
df = df.dropna(subset=["engraftment_success"])

# Целевая переменная и признаки
X = df.drop(columns=["engraftment_success"])
y = df["engraftment_success"]

# ===== Уравниваем классы через апсемплинг =====
from sklearn.utils import resample

df_full = pd.concat([X, y], axis=1)
df_majority = df_full[df_full["engraftment_success"] == 1.0]
df_minority = df_full[df_full["engraftment_success"] == 0.0]

df_minority_upsampled = resample(df_minority,
                                 replace=True,
                                 n_samples=len(df_majority),
                                 random_state=42)

df_balanced = pd.concat([df_majority, df_minority_upsampled])

# Обновляем X и y
X = df_balanced.drop(columns=["engraftment_success"])
y = df_balanced["engraftment_success"]

# Разделение на категориальные и числовые признаки
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()

# Обработка категориальных признаков
if cat_cols:
    # Удаляем пустые категориальные колонки
    empty_cat_cols = [col for col in cat_cols if X[col].isna().all()]
    if empty_cat_cols:
        print(f"Removing empty categorical columns: {empty_cat_cols}")
        cat_cols = [col for col in cat_cols if col not in empty_cat_cols]
        X = X.drop(columns=empty_cat_cols)

    # Импутация пропущенных значений
    cat_imputer = SimpleImputer(strategy='most_frequent')
    X[cat_cols] = pd.DataFrame(
        cat_imputer.fit_transform(X[cat_cols]),
        columns=cat_cols,
        index=X.index
    )

    # One-hot encoding
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

# Обработка числовых признаков
if num_cols:
    # Импутация пропущенных значений
    num_imputer = SimpleImputer(strategy='mean')
    X[num_cols] = pd.DataFrame(
        num_imputer.fit_transform(X[num_cols]),
        columns=num_cols,
        index=X.index
    )

    # Стандартизация
    scaler = StandardScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])

# Балансировка классов
n_negative = sum(y == 0)
n_positive = sum(y == 1)
scale_pos_weight = n_negative / n_positive

# Разделение на train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Модель
model = XGBClassifier(
    objective="binary:logistic",
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    use_label_encoder=False,
    random_state=42,
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1
)

# Обучение
model.fit(X_train, y_train)

# Оценка
y_pred = model.predict(X_test)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.show()

# Важность признаков
plt.figure(figsize=(10, 6))
plot_importance(model, max_num_features=10)
plt.title("Feature Importance (XGBoost)")
plt.tight_layout()
plt.show()

# Кросс-валидация (AUC как метрика)
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc")
print(f"Mean AUC (5-fold CV): {np.mean(scores):.3f} ± {np.std(scores):.3f}")

# Создаем папку models, если её нет
os.makedirs('models', exist_ok=True)

# Сохраняем модель
model.save_model('models/xgboost_model.json')

# Сохраняем объекты предобработки
preprocessing_objects = {
    'cat_imputer': cat_imputer if cat_cols else None,
    'num_imputer': num_imputer if num_cols else None,
    'scaler': scaler if num_cols else None,
    'cat_cols': cat_cols,
    'num_cols': num_cols,
    'feature_names': X.columns.tolist()
}

joblib.dump(preprocessing_objects, 'models/preprocessing_objects.joblib')
print("\nМодель и объекты предобработки сохранены в папке 'models'")
