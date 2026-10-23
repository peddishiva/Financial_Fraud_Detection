"""
Regression tests for the strict exact-record integrity policy.
Run from the directory containing manage.py:
python manage.py test Remote_User.test_prediction_integrity
"""
from decimal import Decimal
from django.test import SimpleTestCase
from Remote_User.views import _read_reference_dataset, _verify_reference_record


class ReferenceRecordVerificationTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dataset = _read_reference_dataset()
        cls.row0 = cls.dataset.loc[cls.dataset["Label"] == 0].iloc[0]
        cls.row1 = cls.dataset.loc[cls.dataset["Label"] == 1].iloc[0]

    @staticmethod
    def submitted_from(row):
        return {
            "Fid": str(row["Fid"]),
            "trans_datetime": str(row["trans_datetime"]),
            "Acc_num": str(row["Acc_num"]),
            "bankingtype": str(row["bankingtype"]),
            "category": str(row["category"]),
            "amt": str(row["amt"]),
            "Name": str(row["Name"]),
            "gender": str(row["gender"]),
            "street": str(row["street"]),
            "city": str(row["city"]),
            "zip": str(row["zip"]),
            "lat": str(row["lat"]),
            "lon": str(row["long"]),
            "job": str(row["job"]),
            "dob": str(row["dob"]),
            "trans_num": str(row["trans_num"]),
            "merch_lat": str(row["merch_lat"]),
            "merch_long": str(row["merch_long"]),
        }

    def test_exact_label_zero_record_is_legitimate(self):
        label, matched = _verify_reference_record(self.submitted_from(self.row0), self.dataset)
        self.assertTrue(matched)
        self.assertEqual(label, 0)

    def test_exact_label_one_record_is_fraudulent(self):
        label, matched = _verify_reference_record(self.submitted_from(self.row1), self.dataset)
        self.assertTrue(matched)
        self.assertEqual(label, 1)

    def test_scientific_notation_account_number_matches_expanded_form(self):
        row = self.row0
        submitted = self.submitted_from(row)
        submitted["Acc_num"] = str(int(Decimal(str(row["Acc_num"]))))
        label, matched = _verify_reference_record(submitted, self.dataset)
        self.assertTrue(matched)
        self.assertEqual(label, int(row["Label"]))

    def test_changing_amount_makes_record_not_match(self):
        submitted = self.submitted_from(self.row0)
        submitted["amt"] = str(float(submitted["amt"]) + 1.0)
        label, matched = _verify_reference_record(submitted, self.dataset)
        self.assertFalse(matched)
        self.assertEqual(label, 1)

    def test_changing_each_dashboard_feature_makes_record_not_match(self):
        base = self.submitted_from(self.row0)
        mutations = {
            "Fid": base["Fid"] + "-changed",
            "trans_datetime": "31-12-99 23:59",
            "Acc_num": "999999999999999",
            "bankingtype": "Changed Banking Type",
            "category": "changed_category",
            "amt": str(float(base["amt"]) + 0.25),
            "Name": base["Name"] + " changed",
            "gender": "X" if base["gender"] != "X" else "Y",
            "street": base["street"] + " changed",
            "city": base["city"] + " changed",
            "zip": "00000",
            "lat": str(float(base["lat"]) + 0.001),
            "lon": str(float(base["lon"]) + 0.001),
            "job": base["job"] + " changed",
            "dob": "01-01-01",
            "trans_num": base["trans_num"][:-1] + ("0" if base["trans_num"][-1] != "0" else "1"),
            "merch_lat": str(float(base["merch_lat"]) + 0.001),
            "merch_long": str(float(base["merch_long"]) + 0.001),
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                submitted = dict(base)
                submitted[field] = value
                label, matched = _verify_reference_record(submitted, self.dataset)
                self.assertFalse(matched, field)
                self.assertEqual(label, 1, field)

    def test_dataset_has_expected_schema_and_row_count(self):
        self.assertIn("Label", self.dataset.columns)
        self.assertEqual(len(self.dataset), 1149)
