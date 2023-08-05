from enum import Enum


class SourceEnum(str, Enum):
    claimhunter = "claimhunter"
    congreso = "congreso"
    editor = "editor"
    slack = "slack"


class TargetEnum(str, Enum):
    fact = "fact"
    worthy = "check-worthy"


class ErrorMessage(str, Enum):
    boolean = "Must be a boolean"
    date = "Must be a date with format %Y-%m-%d or %Y-%m-%dT%H:%M:%S"
    diffdate = "End date must be less than or equal to start date"
    exception = "\n\rError Exception: "
    isinteger = "Must be a integer: "
    languages = "Must be a list of strings"
    source = f"Must be a valid source {[src.value for src in SourceEnum]}:"
    splits = "Please enter 3 splits, train, test and dev: "
    target = f"Must be a valid target {[target.value for target in TargetEnum]}:"
    total = "Total must be equal to 100: "


class HelpMessage(str, Enum):
    duplicates = "Remove duplicate records from the dataset.\n\rExample: --duplicates"
    end = "Select end date to create dataset.\n\rExample: --end-date 2020-01-30 or including time --end-date 2020-01-30T12:25:00 [optional]"
    file = """Path to json file. \n\rExample: datasets/1606214056/export_config_1606214056.json \n\rSchema json file:\n\r{ "source": { "slack": "80 10 10", "claimhunter": "80 10 10" }, "target": "fact", "random_state": 123, "start_date": "2018-09-24T12:13:54", "end_date": "2020-10-24T00:00:00", "translate": true, "languages": ["fr"] }\n\r"""
    folder = "Folder to export dataset.\n\rExample: --folder /home/user/datasets"
    lang = "Select language or multiple languages to create dataset.\n\rExample: --lang en --lang fr [optional]"
    mongo = "Mongo URI.\n\rExample: --mongo mongodb://localhost:27017 [optional]"
    ramdom = "Select random state to create dataset.\n\rExample: --random 1234"
    reviews = "Split with reviews, respect reviews pertentage in test/dev.\n\rExample: --reviews"
    source = "Select source or multiple sources to create dataset.\n\rExample: --source congreso --source editor"
    start = "Select start date to create dataset.\n\rExample: --start-date 2020-01-22 or including time --start-date 2020-01-22T10:37:05 [optional]"
    target = "Select target to create dataset.\n\rExample: --target check-worthy"
    translations = "Search sentence translations.\n\rExample: --translate"


class InfoMessage(str, Enum):
    create = "The dataset will be created with these parameters: \n\r"
    created = "\n\rDataset created OK !!!\n\r"
    duplicates = "no duplicates    "
    dropped = "remove duplicates"
    labelread = "read splits      "
    labelrecords = "get records      "
    labelsave = "save dataset     "
    labelsplit = "split dataset    "
    notfound = "Not found records in db"
    path = "\n\rPath dataset: "
    processing = "Processing source: "
    sourcesplit = "Select split train test dev, example: 80 10 10"
