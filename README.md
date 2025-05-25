# ml-genomatch
Harmonization and analysis of HCT patient datasets using Python and ML

---
# Transplant Outcome Prediction Pipeline

This project is focused on predicting transplant outcomes using clinical data from multiple sources. The full pipeline includes dataset loading and harmonization, model training, hyperparameter tuning, and model evaluation using XGBoost.

---

## Files Overview

### `pipeline.py`

* Loads and preprocesses datasets from 4 clinical sources: UAE, Bone Marrow, P5191, and P5303.
* Standardizes column names and structures.
* Merges all datasets into one unified DataFrame.
* Validates and saves the cleaned dataset to `processed/transplant_data.csv`.
* Handles missing columns by filling with `NaN` and prints column completeness.

### `train_model.py`

* Loads the unified dataset.
* Preprocesses it (handling missing values, converting categorical variables, etc.).
* Applies random oversampling to balance target classes.
* Splits the data into training and test sets.
* Trains a baseline XGBoost model with default hyperparameters.
* Evaluates model performance on test set:

  * Accuracy: **0.97**
  * AUC: **0.993**
  * Confusion Matrix shows **very low false negatives**.
  * Classification report confirms balanced precision/recall (all \~0.97).

### `XGBoost.py`

* Repeats training pipeline, but allows more manual tuning and extended analysis.
* Outputs classification metrics (precision, recall, F1, AUC).
* Identifies the top 10 most important features by weight:

| Feature                                  | Importance |
| ---------------------------------------- | ---------- |
| `patient_age`                            | 180        |
| `days_from_diagnosis_to_hct`             | 97         |
| `chronic_gvhd`                           | 60         |
| `cd34_dose`                              | 54         |
| `hla_match_score`                        | 43         |
| `overall_survival_1y`                    | 30         |
| `acute_gvhd_grade`                       | 30         |
| `source_of_cells_BM`                     | 27         |
| `conditioning_regimen_reduced_intensity` | 27         |
| `patient_sex_M`                          | 26         |

These features can guide domain experts in interpreting clinical relevance.

### `XGBoost_gridsearch.py`

* Performs hyperparameter tuning using Grid Search with 3-fold cross-validation.
* Search space includes `learning_rate`, `max_depth`, and `n_estimators`.
* Best parameters found:

  ```json
  {
    "learning_rate": 0.2,
    "max_depth": 5,
    "n_estimators": 100
  }
  ```
* Best average AUC from cross-validation: **0.9697**

---

## Model Evaluation Summary

| Metric        | Value |
| ------------- | ----- |
| Accuracy      | 0.97  |
| AUC           | 0.993 |
| Precision (0) | 0.95  |
| Recall (0)    | 1.00  |
| Precision (1) | 1.00  |
| Recall (1)    | 0.94  |

* Excellent discrimination between classes
* No false positives for class 1, and very few false negatives

> **Note:** These results were obtained on a balanced dataset via oversampling. To fully validate, further testing on raw and independent data is recommended.

---

## How to Run

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Preprocess Data**

   ```bash
   python pipeline.py
   ```

3. **Train Baseline Model**

   ```bash
   python train_model.py
   ```

4. **Evaluate Feature Importance**

   ```bash
   python XGBoost.py
   ```

5. **Run Grid Search**

   ```bash
   python XGBoost_gridsearch.py
   ```

---

## Requirements

Dependencies are listed in `requirements.txt`:

```
pandas
numpy
scikit-learn
xgboost
imbalanced-learn
```

---

## Conclusion

This pipeline enables effective prediction of transplant outcomes using a robust clinical dataset and a fine-tuned XGBoost model. The high AUC and well-calibrated metrics demonstrate strong performance, but real-world validation is essential for deployment.

For clinical collaboration or integration, top features and model predictions can guide risk stratification and personalized treatment planning.

---

## REST API: GenoMatch

The trained XGBoost model is deployed as a RESTful API, allowing real-time predictions of transplant success based on clinical inputs.

### Available Endpoints

#### `POST /predict`

Predicts the likelihood of a successful transplant based on patient and donor data.

**Example Request:**

```json
{
  "hla_match_score": 9.0,
  "donor_age": 28,
  "patient_age": 35,
  "donor_sex": "M",
  "patient_sex": "F",
  "diagnosis": "AML",
  "conditioning_regimen": "myeloablative",
  "source_of_cells": "PBSC",
  "days_from_diagnosis_to_hct": 45,
  "cd34_dose": 6.7
}
```

**Example Response:**

```json
{
  "success_probability": "87.30%",
  "risk_level": "Low Risk",
  "recommendation": "High likelihood of successful transplant. Procedure can be planned.",
  "confidence": "74.60%"
}
```

#### `GET /`

Returns basic information about the GenoMatch API service.

---

### Swagger Documentation

Swagger documentation is available [here](https://app.swaggerhub.com/apis/itmo-0e9/GenoMatch/1.0.0)

---

### Running the API

```bash
uvicorn api:app --reload
```

The `api.py` file implements a FastAPI server that wraps the trained model and handles prediction requests.
