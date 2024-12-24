# eve2clab

A rudimentary script to convert an EVE-NG .unl file to a containerlab topology. 

It can also be used to 'extract' startup confgs from an EVE-NG `.unl` file.

## Usage

1. Place the EVE-NG `.unl` file in the same directory as `parse.py`.
1. In `parse.py` edit:
    - `REGISTRY` to your container registry (usually this should be `vrnetlab`).
    - `file_path` to the name of your `.unl` file (including file extension).

1. Run `parse.py`. A new export directory with the lab name should be created. In that directory you will find:

- Converted containerlab topology
- Any startup configurations under the 'config' directory.

## Caveats

**Mapping**

You may have to edit the `MAPPING` dictionary. `MAPPING` is used to convert the EVE-NG template name to the correct containerlab kind. 

It is simple to add a mapping and the format is as follows:

```py
MAPPING = {
    'EVE-NG Name': 'Containerlab Kind'
}
 ```

**Links**

1. Only point-to-point links are supported, currently multipoint or networks connected via 'dumb' switches aren't supported.

1. The topology `yaml` file will not contain the links in the abbreviated format you are used to. Indentation will also be incorrect. These two issues are mainly visual and the topology will work with containerlab as normal.