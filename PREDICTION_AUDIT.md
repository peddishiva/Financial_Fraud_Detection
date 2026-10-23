# Prediction audit and fix report

## Findings from the original `main` branch

- `Remote_User/views.py::predict_financial_transaction_type` read the dashboard fields but built `X = df['Fid']`, trained `CountVectorizer` on that one identifier field during every POST, and inferred from only the submitted `Fid`. Changing amount, category, customer details, or merchant coordinates therefore could not affect model inputs.
- `Service_Provider/views.py::Train_Test_DataSets` also trained/evaluated classifiers on `Fid` only. It did not save those trained models; its displayed metrics were for separate fits and a random split without a fixed seed.
- The old training code used a non-stratified random split and reported accuracy but did not use the complete transaction record. Its scores do not establish that all dashboard fields are validated.
- The dashboard's customer longitude field is named `lon`, while the CSV column is `long`.
- The CSV target column is `Label`; the implementation must respect each exact matched record's own label, not treat every matched record as legitimate.

## Changes on this branch

The prediction view now has an explicit exact-record integrity checker using the submitted form fields against the dataset fields, with basic normalization for dates, numbers, and case/whitespace. Exact matches return the actual `Label`: 0 -> Fraud Not Detected; 1 -> Fraud Detected. A record that does not match any row is flagged as Fraud Detected under this strict policy. Required fields, amount, coordinate ranges, and dataset availability are validated; errors are shown instead of silently falling back to class 0. The result cell exposes a live status region for accessibility.

This is deliberately an **exact-record integrity policy**, not an ML fraud-classifier prediction. It follows the requested demonstration rule; it does not prove that every changed real-world transaction is fraudulent. A separate properly trained model using appropriate transaction features is still needed for generalization to unseen transactions.

## Regression tests added

`Remote_User/test_prediction_integrity.py` tests an exact label-0 record, exact label-1 record, amount mutation, single-field mutations across the form fields, and the dataset path/column count.

Run in the Django project directory:

```powershell
python manage.py test Remote_User.test_prediction_integrity
```

## Limitation

The GitHub connector can inspect and commit code, but this environment did not run the Django server/database or execute these tests against the user's local machine. Run the command above locally before merging. The test assumes the local CSV has the same schema and 1,149 records as the checked-in dataset.
