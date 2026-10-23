# Prediction audit and change summary

## Confirmed behavior on the original main branch

The original `Remote_User/views.py::predict_financial_transaction_type` collected the dashboard values but built `X = df['Fid']`, fit `CountVectorizer` on that single identifier field during each form submission, and predicted only from the submitted `Fid`. The transaction amount, category, date, customer details and coordinates did not enter the model's feature vector, explaining why editing them could leave the output unchanged.

The service-provider training page also reported metrics for classifiers trained on `Fid` alone. Those metrics do not demonstrate that the full dashboard fields are being evaluated.

The CSV has both `Label=0` and `Label=1`, so matched rows must use their actual label. The dashboard calls customer longitude `lon`, while the CSV calls it `long`.

## Implementation in this branch

This branch implements the requested **strict exact-record integrity policy**:
- It compares all submitted record fields against dataset fields after limited normalization for numbers, dates, case/whitespace, and account-number scientific notation.
- An exact record match returns the record's actual label: 0 -> Fraud Not Detected; 1 -> Fraud Detected.
- A record that does not exactly match any reference row is flagged as Fraud Detected.
- Required fields, numeric inputs, coordinate ranges, and the dataset schema are validated.
- Errors are shown rather than silently defaulting to a legitimate result.

This is **not a trained ML prediction for unseen transactions**. It is exact-record verification implemented to follow the requested demo rule. For generalization to new transactions, the next step is a separate properly trained and evaluated model using suitable transaction/customer/merchant features. An altered record is treated as suspicious by this strict demo policy, but that is not proof of fraud in the real world.

## Regression tests

The new test module covers exact label-0 and label-1 records, expanded versus scientific account-number notation, amount changes, and individual field mutations.

Run from the project directory containing `manage.py`:

```powershell
python manage.py test Remote_User.test_prediction_integrity
```

## Verification performed

A local Python reproduction against the attached CSV confirmed that:
- an exact row with `Label=0` matches as class 0;
- an exact row with `Label=1` matches as class 1;
- converting a scientific-notation account number to its expanded integer string still matches;
- all 18 single-field mutation cases in the regression-test matrix fail exact matching.

This reproduction used the CSV and the normalization logic; it did **not** execute the Django test suite or exercise the local MySQL-backed HTTP flow.

## Remaining verification

The GitHub connector environment did not run Django against the user's local server/database. Run the test command above locally and test one end-to-end form submission before merging. A separately trained all-feature ML classifier remains future work; the current fix is an explicit record-integrity rule.
