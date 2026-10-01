"""
gcs_to_pubsub_lab1_simple.py  --  Lab 1's "Job 1"

Reads the 4 dummy .jsonl files from Cloud Storage and publishes each
line as one message to its matching Pub/Sub topic.

Local test (reads from ./dummy_data/, just prints instead of publishing):
    python gcs_to_pubsub_lab1_simple.py --runner=DirectRunner

Real run:
    python gcs_to_pubsub_lab1_simple.py \
      --runner=DataflowRunner --project=YOUR_PROJECT_ID --region=us-central1 \
      --temp_location=gs://YOUR_BUCKET/temp \
      --gcs_prefix=gs://YOUR_BUCKET/dummy \
      --project_for_topics=YOUR_PROJECT_ID
"""

import argparse
import os

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# .jsonl filename stem -> the Pub/Sub topic it feeds
TOPIC_MAP = {
    "TOPIC_account_loanslinesleases_lcm": "afs-topic-lcm",
    "TOPIC_account_loanslinesleases_chargeheaders": "afs-topic-chargeheaders",
    "TOPIC_account_loanslinesleases_balanceheaders": "afs-topic-balanceheaders",
    "TOPIC_account_loanslinesleases_chargeheaders_amounts": "afs-topic-chargeheaders-amounts",
}


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gcs_prefix", default=None, help="e.g. gs://bucket/dummy -- omit for local test")
    parser.add_argument("--local_dir", default="dummy_data")
    parser.add_argument("--project_for_topics", default=None, help="Required for a real (non-local) run")
    known_args, pipeline_args = parser.parse_known_args()
    options = PipelineOptions(pipeline_args)
    local_mode = known_args.gcs_prefix is None

    with beam.Pipeline(options=options) as p:
        for stem, topic_name in TOPIC_MAP.items():
            path = (os.path.join(known_args.local_dir, f"{stem}.jsonl") if local_mode
                    else f"{known_args.gcs_prefix}/{stem}.jsonl")
            lines = p | f"Read {stem}" >> beam.io.ReadFromText(path)
            encoded = lines | f"Encode {stem}" >> beam.Map(lambda line: line.encode("utf-8"))

            if local_mode:
                encoded | f"Print {stem}" >> beam.Map(
                    lambda b, t=topic_name: print(f"[would publish to {t}] {b.decode('utf-8')}")
                )
            else:
                topic_path = f"projects/{known_args.project_for_topics}/topics/{topic_name}"
                encoded | f"Publish {stem}" >> beam.io.WriteToPubSub(topic=topic_path)


if __name__ == "__main__":
    run()
