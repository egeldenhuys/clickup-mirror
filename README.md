# clickup-mirror

Create a file mirror from ClickUP

## Dependencies
- [Requests](http://docs.python-requests.org/en/master/)
    - `pip install requests`

## Usage

Log into ClickUP using Chrome or Firefox before running the script.

```
usage: clickup-mirror.py [-h] [-b BROWSER] [-o OUTPUR_DIR] [-t FILE_TYPES]
                         [-d DATA_FILE] [-n] [--version]

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
                        [default: pdf]
  -d DATA_FILE, --data-file DATA_FILE
                        File to be used for the database cache. Will be
                        created if it does not exist [default:
                        mirror/database.json]
  -n, --dry-run         Only generate the database file. Do not download
                        anything [default: False]
  --version             show program's version number and exit

BROWSER_TYPE:
    chromium
    chrome
    firefox

COMMON FILE TYPES:
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
│   │   ├── INL240_Howtowriteanabstract_2016.pdf
│   │   ├── INL 240 Practical Portfolio
│   │   │   └── Practical Portfolio_2017.pdf
│   │   └── IntroductiontoWriting_2016_1.pdf
│   ├── Study Guide and Schedules
│   │   ├── INL240Schedule2017_v2.pdf
│   │   └── INL240_StudyGuide_2017.pdf
│   └── Theory Content
│       ├── INL240_IntroductoryLecture_2017_FINAL.pdf
│       └── Theme 1 - Foundational Concepts in Information Ethics
│           └── Theme 1 (part1)(1).pdf
```
