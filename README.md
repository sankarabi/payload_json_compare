# Payload Comparison Tool

This tool is designed to compare JSON payloads between different environments (e.g., dev, staging, prod) and identify any differences. It is useful for verifying that data structures are consistent across various environments.

## Files

The tool uses the following files for comparison:

- **dev_payload.json**: JSON payload for the `dev` environment.
- **staging_payload.json**: JSON payload for the `staging` environment.
- **prod_payload.json**: JSON payload for the `prod` environment.

You can replace these files with the appropriate payloads for your comparison needs.

## Usage

To run the payload comparison, you need to specify which environment files you want to compare by setting the `FILE1` and `FILE2` variables in the script.

## Run the Program
[Linux]
```
python3 comparator.py
```
[Windows]
```
python comparator.py
```
### Setting the Environment Files

In the script `comparator.py`, set the `FILE1` and `FILE2` variables to the desired environments:

```python
FILE1 = "dev_payload.json"
FILE2 = "staging_payload.json"```
```
