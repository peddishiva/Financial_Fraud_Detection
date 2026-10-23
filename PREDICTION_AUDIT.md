# Prediction audit and fix report

## Findings from main

- `Remote_User/views.py::predict_financial_transaction_type` read every dashboard field, but built features from `df['Fid']` only and inferred from only the submitted `Fid`. Therefore changing amount, category, customer data or coordinates did not change the model input.
- `Service_Provider/views.py::Train_Test_DataSets` also evaluated classifiers on `Fid` alone and did not persist those models for inference. The displayed metric is not evidence that the full transaction form is being evaluated.
- The dashboard names customer longitude `lon`; the CSV uses `long`.
- The dataset contains both `Label=0` and `Label=1`, so exact matches must follow their actual label.

## Current branch behavior

The endpoint uses a strict exact-record integrity check: it compares the complete submitted feature set to the CSV after basic normalization. Exact matches use their recorded label (0 => Fraud Not Detected, 1 => Fraud Detected); any record with no exact match is flagged as Fraud Detected. Errors are shown rather than silently defaulting to class 0. This is an explicit record-verification policy, **not a trained ML model predicting unseen transactions**.

## Regression tests

Added `Remote_User/test_prediction_integrity.py` for exact label-0/label-1 rows, amount changes, one-field changes, and dataset schema/row count.

Run from the directory containing `manage.py`:
```powershell
python manage.py test Remote_User.test_prediction_integrity
```

## Limitation

The GitHub connector did not run this Django app or its tests against a local database/server. Run the command locally before merging. A separate properly trained and evaluated full-feature model is still needed for classification of unseen transactions.
