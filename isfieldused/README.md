# isfieldused

A small utility to check whether specific fields are used within a project directory. It reads a list of fields from a text file, searches recursively under a given start path, and reports which files contain each field.

## Features

- Exact token match (field must not be part of a larger word)
- Recursive search from a user-provided start path
- Console report per field with matching files
- JSON output for easy post-processing
- Progress line showing which field is currently being checked

## Requirements

- Python 3.8+

## Usage

```bash
python3 isfieldused.py --fields fields.txt --start /path/to/project --json-out results.json
```

## Inputs

- `fields.txt`: one field name per line. Empty lines are ignored. Lines starting with `#` are treated as comments.
- `--start`: the root path where the recursive search begins (can be absolute or relative).

## Output

### Console
For each field, the script prints either the list of matching files or `(not found)`.

Example:
```
Pruefe Feld: MyField__c
MyField__c
  /path/to/project/force-app/main/default/classes/Foo.cls
  /path/to/project/force-app/main/default/triggers/Bar.trigger
```

### JSON
A JSON file mapping each field name to a list of file paths where it was found.

Example:
```json
{
  "MyField__c": [
    "/path/to/project/force-app/main/default/classes/Foo.cls",
    "/path/to/project/force-app/main/default/triggers/Bar.trigger"
  ],
  "OtherField__c": []
}
```

## Exact Match Behavior

The search uses an exact token match. A field is considered found only when it is **not** directly preceded or followed by letters, digits, or underscores.

If you want substring matching instead, ask to adjust the script.

## Notes

- All files under the start path are scanned, regardless of extension.
- The script reads files as UTF-8 with `errors="ignore"` to tolerate mixed encodings.
