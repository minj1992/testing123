"""
generate_dummy_data_lab1.py

Generates the dummy records for Lab 1's 4 topics (T23, T8, T7, T12) and
either writes them locally or uploads them straight to Cloud Storage,
one .jsonl file per topic, ready for gcs_to_pubsub_lab1_simple.py to
pick up and publish.

----------------------------------------------------------------------
HOW TO ADD NEW DUMMY DATA
----------------------------------------------------------------------
Each topic below is a plain Python list of dicts. To add a new record:

  1. Copy an existing dict for that topic.
  2. Give it a new, unique ID for that topic's primary-key field
     (e.g. "LCM-0003" for T23 -- IDs must not repeat).
  3. If it's a child topic (T8, T7, T12), make sure its foreign-key
     field points at an ID that actually exists in the parent list
     below it -- T8/T7 need a real T23 accountLoanslinesleaseId,
     and T12 needs a real T8 accountLoanslinesleasesChargeheaderId.
  4. Save the file, then re-run this script to regenerate the .jsonl
     files, and re-run gcs_to_pubsub_lab1_simple.py to publish them.
     Old records already in Bigtable/AlloyDB are untouched -- new
     records are simply added alongside them the next time the main
     pipeline runs.
----------------------------------------------------------------------

Local test (writes to ./dummy_data/, no cloud needed):
    python generate_dummy_data_lab1.py

Upload straight to Cloud Storage:
    python generate_dummy_data_lab1.py --gcs_bucket=YOUR_BUCKET
"""

import argparse
import json
import os

T23_LCM = [
    {"accountLoanslinesleasesLcmId": "LCM-0001", "accountLoanslinesleaseId": "ACC-0001",
     "applicationNumber": "APP01", "applicationSystem": "AFSVISION", "bankNumber": "001",
     "financialInstrumentNumber": "4521", "obligationNumber": "88012", "obligorNumber": "4521",
     "externalSourceTicklerReference": None},
    {"accountLoanslinesleasesLcmId": "LCM-0002", "accountLoanslinesleaseId": "ACC-0002",
     "applicationNumber": "APP01", "applicationSystem": "AFSVISION", "bankNumber": "001",
     "financialInstrumentNumber": "9310", "obligationNumber": "204", "obligorNumber": "9310",
     "externalSourceTicklerReference": "TKL-77"},
    # --- add new T23 records here, following the same shape, with a new LCM-000x id ---
]

T8_CHARGEHEADERS = [
    {"accountLoanslinesleasesChargeheaderId": "CHG-0001", "accountLoanslinesleaseId": "ACC-0001",
     "applicationNumber": "APP01", "applicationSystem": "AFSVISION", "bankNumber": "001",
     "chargeCode": "10", "financialInstrumentNumber": "4521", "obligationNumber": "88012", "obligorNumber": "4521"},
    {"accountLoanslinesleasesChargeheaderId": "CHG-0002", "accountLoanslinesleaseId": "ACC-0002",
     "applicationNumber": "APP01", "applicationSystem": "AFSVISION", "bankNumber": "001",
     "chargeCode": "22", "financialInstrumentNumber": "9310", "obligationNumber": "204", "obligorNumber": "9310"},
    # --- new T8 records: accountLoanslinesleaseId MUST match a real T23 record above ---
]

T7_BALANCEHEADERS = [
    {"accountLoanslinesleasesBalanceheaderId": "BAL-0001", "accountLoanslinesleaseId": "ACC-0001",
     "applicationSystem": "AFSVISION", "associatedPrincipalBalanceCode": "P", "balanceCode": "CUR",
     "bankNumber": "001", "financialInstrumentNumber": "4521", "obligationNumber": "88012",
     "obligorNumber": "4521", "sequenceNumber": "1"},
    {"accountLoanslinesleasesBalanceheaderId": "BAL-0002", "accountLoanslinesleaseId": "ACC-0002",
     "applicationSystem": "AFSVISION", "associatedPrincipalBalanceCode": "P", "balanceCode": "CUR",
     "bankNumber": "001", "financialInstrumentNumber": "9310", "obligationNumber": "204",
     "obligorNumber": "9310", "sequenceNumber": "1"},
    # --- new T7 records: accountLoanslinesleaseId MUST match a real T23 record above ---
]

T12_CHARGEHEADERS_AMOUNTS = [
    {"accountLoanslinesleasesChargeheadersAmountId": "CHGAMT-0001", "accountLoanslinesleasesChargeheaderId": "CHG-0001",
     "amountFieldName": "PRINCIPAL", "applicationNumber": "APP01", "applicationSystem": "AFSVISION",
     "bankNumber": "001", "chargeCode": "10", "financialInstrumentNumber": "4521",
     "obligationNumber": "88012", "obligorNumber": "4521"},
    {"accountLoanslinesleasesChargeheadersAmountId": "CHGAMT-0002", "accountLoanslinesleasesChargeheaderId": "CHG-0002",
     "amountFieldName": "INTEREST", "applicationNumber": "APP01", "applicationSystem": "AFSVISION",
     "bankNumber": "001", "chargeCode": "22", "financialInstrumentNumber": "9310",
     "obligationNumber": "204", "obligorNumber": "9310"},
    # --- new T12 records: accountLoanslinesleasesChargeheaderId MUST match a real T8 record above ---
]

TOPIC_FILES = {
    "TOPIC_account_loanslinesleases_lcm": T23_LCM,
    "TOPIC_account_loanslinesleases_chargeheaders": T8_CHARGEHEADERS,
    "TOPIC_account_loanslinesleases_balanceheaders": T7_BALANCEHEADERS,
    "TOPIC_account_loanslinesleases_chargeheaders_amounts": T12_CHARGEHEADERS_AMOUNTS,
}


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", default="dummy_data")
    parser.add_argument("--gcs_bucket", default=None, help="If set, uploads instead of writing locally.")
    args = parser.parse_args()

    if args.gcs_bucket:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(args.gcs_bucket)
        for name, records in TOPIC_FILES.items():
            blob = bucket.blob(f"dummy/{name}.jsonl")
            body = "\n".join(json.dumps(r) for r in records)
            blob.upload_from_string(body)
            print(f"Uploaded gs://{args.gcs_bucket}/dummy/{name}.jsonl ({len(records)} records)")
        return

    os.makedirs(args.out_dir, exist_ok=True)
    for name, records in TOPIC_FILES.items():
        path = os.path.join(args.out_dir, f"{name}.jsonl")
        with open(path, "w") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")
        print(f"Wrote {path} ({len(records)} records)")


if __name__ == "__main__":
    run()
