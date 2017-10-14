# clickup-mirror


## This script no longer works and will not be fixed in the future!

----

[![GitHub release](https://img.shields.io/github/release/egeldenhuys/clickup-mirror.svg)](https://github.com/egeldenhuys/clickup-mirror/releases)

Create a file mirror from ClickUP

## Dependencies
- [Requests](https://github.com/kennethreitz/requests)
    - `pip install requests`
- [browser-cookie3](https://github.com/borisbabic/browser_cookie3)
    - `pip install browser_cookie3`
- python3

## Install
```
git clone https://github.com/egeldenhuys/clickup-mirror
```

## Usage

Log into ClickUP using Chrome or Firefox before running the script.

```
usage: clickup-mirror.py [-h] [-b BROWSER] [-o OUTPUR_DIR] [-t FILE_TYPES]
                         [-d DATA_FILE] [-u] [-s SESSION_FILE] [-n]
                         [--version]

Create a file mirror from ClickUP

optional arguments:
  -h, --help            show this help message and exit
  -b BROWSER, --browser BROWSER
                        The browser to be used for authentication [default:
                        chromium]
  -o OUTPUR_DIR, --outpur-dir OUTPUR_DIR
                        The directory to create the mirror in [default:
                        mirror/]
  -t FILE_TYPES, --file-types FILE_TYPES
                        Comma-separated list of file types to download
                        [default: all]
  -d DATA_FILE, --data-file DATA_FILE
                        File to be used for the database cache. Will be
                        created if it does not exist [default:
                        mirror/database.json]
  -u, --update-database
                        Overwrite the database file
  -s SESSION_FILE, --session-file SESSION_FILE
                        File containing the s_session_id
  -n, --dry-run         Only generate the database file. Do not download
                        anything [default: False]
  --version             show program's version number and exit


BROWSER_TYPE:
    chromium
    chrome
    firefox

COMMON FILE TYPES:
    all
    pdf
    doc
    docx
    xlsx
    pptx
    sql
    iso
    txt
    reg
    exe
```

### Example Usage
To download pdf and sql files into the `ClickUP` directory in home

```
python3 mirror.py --brower chrome --output-directory ~/ClickUp/ --file-types pdf,sql
```

## Example Output
```
├── INL 240 S1 2017
│   ├── Practical Content
│   │   ├── Class activity 2
│   │   │   └── Class activity 2.docx
│   │   ├── Group Project marks
│   │   │   └── INL 240 Group project marks.pdf
│   │   ├── INL240_Howtowriteanabstract_2016.pdf
│   │   ├── INL 240 Practical Portfolio
│   │   │   ├── Practical Portfolio_2017.docx
│   │   │   └── Practical Portfolio_2017.pdf
│   │   ├── IntroductiontoWriting_2016_1.pdf
```
