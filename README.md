# Payload Comparison Tool

This tool is designed to compare JSON payloads between different environments (e.g., dev, staging, prod) and identify any differences. It can be used to verify that data structures are consistent across environments.

## Files

The following files we can use for comparison:

- **dev_payload.json**: JSON payload for the `dev` environment.
- **staging_payload.json**: JSON payload for the `staging` environment.
- **prod_payload.json**: JSON payload for the `prod` environment.

You can replace these with the appropriate payloads for your comparison.

## Usage

To run the payload comparison, you need to specify which environments (files) you want to compare by setting the `FILE1` and `FILE2` variables in the script.

### Setting the Environment Files

In the script `payload_comparision.py`, set the variables `FILE1` and `FILE2` to the desired environments:

```python
FILE1 = "dev"
FILE2 = "staging"
