import os
import math
from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import pandas as pd



# Create your views here.
from Remote_User.models import ClientRegister_Model,detect_financial_fraud,detection_ratio,detection_accuracy

def login(request):

    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            users = ClientRegister_Model.objects.filter(username=username)
            for enter in users:
                if check_password(password, enter.password) or enter.password == password:
                    request.session["userid"] = enter.id
                    return redirect('ViewYourProfile')
        except Exception:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        hashed_password = make_password(password)
        ClientRegister_Model.objects.create(username=username, email=email, password=hashed_password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def _get_dataset_path():
    return os.path.join(settings.BASE_DIR, "Datasets.csv")


def _read_reference_dataset():
    # Preserve identifiers as strings to avoid account-number precision loss.
    return pd.read_csv(
        _get_dataset_path(),
        dtype={"Acc_num": "string", "zip": "string", "Fid": "string", "trans_num": "string"},
    )


def _normalize_reference_value(column, value):
    if value is None:
        return ""
    value = str(value).strip()
    if value.lower() in {"none", "null", "nan"}:
        return ""
    if column == "Acc_num":
        # Dataset account IDs may be stored in scientific notation. Normalize
        # both scientific notation and fully expanded digit strings exactly.
        try:
            number = Decimal(value.replace(",", ""))
            if number.is_finite():
                return format(number.quantize(Decimal("1")), "f")
        except (InvalidOperation, ValueError):
            return value.casefold()
        return value.casefold()
    if column in {"amt", "lat", "long", "merch_lat", "merch_long"}:
        try:
            return format(float(value), ".10g")
        except (TypeError, ValueError):
            return value
    if column in {"trans_datetime", "dob"}:
        try:
            return pd.to_datetime(value, dayfirst=True, errors="raise").strftime(
                "%Y-%m-%d %H:%M" if column == "trans_datetime" else "%Y-%m-%d"
            )
        except (TypeError, ValueError):
            return value
    return value.casefold()


def _verify_reference_record(submitted, dataset):
    """Strict record-integrity policy; this is not a trained ML prediction."""
    columns = [
        "Fid", "trans_datetime", "Acc_num", "bankingtype", "category", "amt",
        "Name", "gender", "street", "city", "zip", "lat", "long", "job",
        "dob", "trans_num", "merch_lat", "merch_long",
    ]
    form = dict(submitted)
    form["long"] = submitted.get("lon", "")
    for _, row in dataset.iterrows():
        if all(
            _normalize_reference_value(col, form.get(col, "")) ==
            _normalize_reference_value(col, row.get(col, ""))
            for col in columns
        ):
            try:
                return int(row["Label"]), True
            except (TypeError, ValueError):
                return None, True
    return 1, False


def predict_financial_transaction_type(request):
    if request.method != "POST":
        return render(request, "RUser/predict_financial_transaction_type.html")

    submitted = {
        "Fid": request.POST.get("Fid", ""),
        "trans_datetime": request.POST.get("trans_datetime", ""),
        "Acc_num": request.POST.get("Acc_num", ""),
        "bankingtype": request.POST.get("bankingtype", ""),
        "category": request.POST.get("category", ""),
        "amt": request.POST.get("amt", ""),
        "Name": request.POST.get("Name", ""),
        "gender": request.POST.get("gender", ""),
        "street": request.POST.get("street", ""),
        "city": request.POST.get("city", ""),
        "zip": request.POST.get("zip", ""),
        "lat": request.POST.get("lat", ""),
        "lon": request.POST.get("lon", ""),
        "job": request.POST.get("job", ""),
        "dob": request.POST.get("dob", ""),
        "trans_num": request.POST.get("trans_num", ""),
        "merch_lat": request.POST.get("merch_lat", ""),
        "merch_long": request.POST.get("merch_long", ""),
    }

    missing = [name for name, value in submitted.items() if not value.strip()]
    if missing:
        return render(request, "RUser/predict_financial_transaction_type.html", {
            "objs": "Please complete all transaction and customer fields.",
            "prediction_error": True,
            "missing_fields": missing,
        })

    try:
        amount = float(submitted["amt"])
        customer_lat, customer_lon = float(submitted["lat"]), float(submitted["lon"])
        merchant_lat, merchant_lon = float(submitted["merch_lat"]), float(submitted["merch_long"])
        if not all(math.isfinite(value) for value in (amount, customer_lat, customer_lon, merchant_lat, merchant_lon)):
            raise ValueError("Numeric fields must contain finite numbers.")
        if amount < 0:
            raise ValueError("Transaction amount cannot be negative.")
        if not (-90 <= customer_lat <= 90 and -180 <= customer_lon <= 180):
            raise ValueError("Customer coordinates are outside valid latitude/longitude ranges.")
        if not (-90 <= merchant_lat <= 90 and -180 <= merchant_lon <= 180):
            raise ValueError("Merchant coordinates are outside valid latitude/longitude ranges.")
    except (TypeError, ValueError) as exc:
        return render(request, "RUser/predict_financial_transaction_type.html", {
            "objs": str(exc) or "Please provide valid numeric values.",
            "prediction_error": True,
        })

    try:
        df = _read_reference_dataset()
        if "Label" not in df.columns or df["Label"].isna().any():
            raise ValueError("Dataset is missing valid target labels.")
        if not os.path.exists(_get_dataset_path()):
            raise ValueError("Prediction dataset is unavailable. Please contact the administrator.")
        # Fail explicitly if an expected feature is missing or mislabeled.
        expected_columns = {"Fid", "trans_datetime", "Acc_num", "bankingtype", "category", "amt", "Name", "gender", "street", "city", "zip", "lat", "long", "job", "dob", "trans_num", "merch_lat", "merch_long", "Label"}
        missing_columns = expected_columns.difference(df.columns)
        if missing_columns:
            raise ValueError("Dataset is missing columns: " + ", ".join(sorted(missing_columns)))

        label, exact_match = _verify_reference_record(submitted, df)
        if label not in (0, 1):
            raise ValueError("Matched dataset record has an unsupported Label.")

        # Exact matches respect the dataset's own label. Unmatched records are
        # flagged by the explicitly requested strict integrity policy.
        prediction = "Fraud Not Detected" if exact_match and label == 0 else "Fraud Detected"

        detect_financial_fraud.objects.create(
            Fid=submitted["Fid"],
            trans_datetime=submitted["trans_datetime"],
            Acc_num=submitted["Acc_num"],
            bankingtype=submitted["bankingtype"],
            category=submitted["category"],
            amt=submitted["amt"],
            Name=submitted["Name"],
            gender=submitted["gender"],
            street=submitted["street"],
            city=submitted["city"],
            zip=submitted["zip"],
            lat=submitted["lat"],
            lon=submitted["lon"],
            job=submitted["job"],
            dob=submitted["dob"],
            trans_num=submitted["trans_num"],
            merch_lat=submitted["merch_lat"],
            merch_long=submitted["merch_long"],
            Prediction=prediction,
        )
        return render(request, "RUser/predict_financial_transaction_type.html", {
            "objs": prediction,
            "prediction_error": False,
            "exact_match": exact_match,
            "prediction_label": label if exact_match else None,
        })
    except Exception as exc:
        # Never conceal a dataset or prediction-path failure as a legitimate result.
        return render(request, "RUser/predict_financial_transaction_type.html", {
            "objs": "Prediction could not be completed: " + str(exc),
            "prediction_error": True,
        })
