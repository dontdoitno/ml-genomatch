from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib
from typing import Dict, Any, List
import os

app = FastAPI(
    title="GenoMatch API",
    description="API для предсказания успешности трансплантации на основе генетической совместимости и клинических данных",
    version="1.0.0"
)

# Загрузка модели и объектов предобработки
model = XGBClassifier()
model.load_model('models/xgboost_model.json')
preprocessing_objects = joblib.load('models/preprocessing_objects.joblib')

class TransplantData(BaseModel):
    # Генетические и иммунные параметры
    hla_match_score: float  # Совместимость по HLA
    donor_age: int    # Возраст донора
    patient_age: int  # Возраст пациента
    donor_sex: str    # Пол донора
    patient_sex: str  # Пол пациента

    # Клинические параметры
    diagnosis: str  # Диагноз
    conditioning_regimen: str  # Режим кондиционирования
    source_of_cells: str  # Источник клеток
    days_from_diagnosis_to_hct: int  # Дни с диагноза до достижения HCT
    cd34_dose: float  # Доза CD34

class PredictionResponse(BaseModel):
    success_probability: str  # Вероятность успеха в процентах
    risk_level: str  # Уровень риска
    recommendation: str  # Рекомендация
    confidence: str  # Уверенность в предсказании

def get_risk_level(probability: float) -> str:
    if probability >= 0.85:
        return "Низкий риск"
    elif probability >= 0.70:
        return "Умеренный риск"
    else:
        return "Высокий риск"

def get_recommendation(probability: float) -> str:
    if probability >= 0.85:
        return "Высокая вероятность успешной трансплантации. Можно планировать процедуру."
    elif probability >= 0.70:
        return "Умеренная вероятность успеха. Рекомендуется дополнительное обследование."
    else:
        return "Высокий риск отторжения. Рекомендуется поиск альтернативного донора."

@app.post("/predict", response_model=PredictionResponse)
async def predict_transplant_success(data: TransplantData):
    try:
        # Создаем словарь с данными по умолчанию
        default_data = {
            "disease_status": "active",
            "donor_relation": "sibling",
            "gvhd_prophylaxis": "standard",
            "patient_ethnicity": "white",
            "acute_gvhd_grade": 0,
            "chronic_gvhd": 0,
            "overall_survival_1y": 1,
            "relapse": 0,
            "trm": 0
        }

        # Объединяем входные данные с данными по умолчанию
        input_dict = data.dict()
        input_dict.update(default_data)

        # Преобразуем в DataFrame
        input_data = pd.DataFrame([input_dict])

        # Применяем предобработку
        if preprocessing_objects['cat_cols']:
            # Импутация категориальных признаков
            cat_data = input_data[preprocessing_objects['cat_cols']]
            cat_data = pd.DataFrame(
                preprocessing_objects['cat_imputer'].transform(cat_data),
                columns=preprocessing_objects['cat_cols'],
                index=input_data.index
            )
            # One-hot encoding
            cat_data = pd.get_dummies(cat_data, columns=preprocessing_objects['cat_cols'], drop_first=True)

        if preprocessing_objects['num_cols']:
            # Импутация числовых признаков
            num_data = input_data[preprocessing_objects['num_cols']]
            num_data = pd.DataFrame(
                preprocessing_objects['num_imputer'].transform(num_data),
                columns=preprocessing_objects['num_cols'],
                index=input_data.index
            )
            # Стандартизация
            num_data = pd.DataFrame(
                preprocessing_objects['scaler'].transform(num_data),
                columns=preprocessing_objects['num_cols'],
                index=input_data.index
            )

        # Объединяем обработанные данные
        if preprocessing_objects['cat_cols'] and preprocessing_objects['num_cols']:
            X = pd.concat([cat_data, num_data], axis=1)
        elif preprocessing_objects['cat_cols']:
            X = cat_data
        else:
            X = num_data

        # Убеждаемся, что все необходимые признаки присутствуют
        for feature in preprocessing_objects['feature_names']:
            if feature not in X.columns:
                X[feature] = 0

        # Упорядочиваем колонки как при обучении
        X = X[preprocessing_objects['feature_names']]

        # Получаем предсказание
        probability = model.predict_proba(X)[0][1]
        risk_level = get_risk_level(probability)
        recommendation = get_recommendation(probability)

        return PredictionResponse(
            success_probability=f'{probability * 100:.2f}%',
            risk_level=risk_level,
            recommendation=recommendation,
            confidence=f'{(abs(probability - 0.5) * 2) * 100:.2f}%'
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {
        "name": "GenoMatch API",
        "description": "API для предсказания успешности трансплантации",
        "endpoints": {
            "/predict": "Предсказание успешности трансплантации на основе генетической совместимости и клинических данных"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
