# Prediction audit and change summary

## Confirmed behavior on the original main branch

The original `Remote_User/views.py::predict_financial_transaction_type` collected the dashboard values but built `X = df['Fid']`, fit `CountVectorizer` on that single identifier field during each form submission, and predicted only from the submitted `Fid`. The transaction amount, category, date, customer details and coordinates did not enter the model's feature vector, explaining why editing them could leave the output unchanged.

The service-provider training page also reported metrics for classifiers trained on `Fid` alone. The repository's form includes all record fields, but the model did not use them. Those scores therefore do not demonstrate full-record fraud detection.

The CSV has both `Label=0` and `Label=1`, so matched rows must use their own label. The form calls customer longitude `lon`, whereas the CSV column is `long`.

## Implementation in this branch

This branch implements the requested **strict exact-record integrity policy** for the demo:
- It compares all submitted record fields with the dataset fields after limited normalization for numbers, dates, and case/whitespace.
- An exact record match returns the record's actual label: 0 -> Fraud Not Detected; 1 -> Fraud Detected.
- A record that does not exactly match a reference row is flagged as Fraud Detected.
- Required fields, amount, and coordinate ranges are validated.
- Exceptions are surfaced as errors instead of silently defaulting to a legitimate result.

This is **not an ML prediction for an unseen transaction**. It is exact-record verification implemented to match the requested demo rule. For real-world classification of new transactions, train and evaluate a separate model using appropriate transaction/customer/merchant features and consistent preprocessing; do not treat every altered record as automatically proven fraud outside this demo rule.

## Regression test coverage

The added tests cover a label-0 exact row, a label-1 exact row, a changed amount, and mutations to each field. Run from the folder containing `manage.py`:

```powershell
python manage.py test Remote_User.test_prediction_integrity
```

## Execution status

The GitHub connector was used to inspect and commit source code, but this environment did not execute the Django app or test suite against the local MySQL/server setup. Run the command above locally before merging, and report any failing tests for follow-up.
