import copy
import json
import os
import time
from typing import Any, Dict, List, Tuple

import pandas as pd
import pymongo
import typer
from nwt_dataset_cli.dtos import ErrorMessage, InfoMessage, SourceEnum
from nwt_dataset_cli.helpers.helpers import catch_error, progress, split_sizes
from pandas.core.frame import DataFrame
from pymongo.command_cursor import CommandCursor
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from sklearn.model_selection import train_test_split


def dataset_train_test_split(
    df: DataFrame, random_state: int, train_size: float, target: str
) -> Tuple[DataFrame, DataFrame]:
    train, test = train_test_split(
        df, random_state=random_state, train_size=train_size, shuffle=True, stratify=df[target]
    )
    return train, test


def reviews_split(df: DataFrame, target: str) -> Tuple[DataFrame, DataFrame, int, DataFrame]:
    positive: DataFrame = df[df[target] > 0]
    negative: DataFrame = df[df[target] < 1]
    reviews: DataFrame = pd.DataFrame()
    remain_positive: DataFrame = copy.deepcopy(positive)

    for index, row in positive.iterrows():
        if "reviews" in row and isinstance(row["reviews"], list):
            reviews = reviews.append(pd.DataFrame([row]))
            remain_positive = remain_positive.drop([index])

    negative = negative.drop(columns=["reviews"], axis=1)
    reviews = reviews.drop(columns=["reviews"], axis=1)
    remain_positive = remain_positive.drop(columns=["reviews"], axis=1)
    return reviews, remain_positive, len(positive), negative


def dataset_reviews_train_test_split(df: DataFrame, dataset_split: Dict[str, Any]) -> Tuple[DataFrame, DataFrame]:
    # total records
    total: int = len(df)
    # apply random_state
    df = df.sample(n=total, random_state=dataset_split["random_state"])
    # split reviews
    reviews, remain_positive, len_positive, negative = reviews_split(df, dataset_split["target"])
    # percentage total positive
    percentage: float = len_positive / total
    # percentage test_size from splits
    test_size: float = 1 - dataset_split["train_size"]
    # total positives will go to test
    positive_test_len: int = round(total * test_size * percentage)
    positive_test = reviews

    if len(reviews) > positive_test_len:
        # reviews - total positives will go to test
        positive_test = reviews.iloc[:positive_test_len, :]
        # add remain reviews to remain positive
        reviews_remain = reviews.iloc[(positive_test_len + 1) :, :]
        remain_positive = pd.concat([remain_positive, (reviews_remain)])

    if len(reviews) < positive_test_len:
        # positive test - reviews + diff between remain_postive and reviews
        diff_len_positive = positive_test_len - len(reviews)
        positive_test = remain_positive.iloc[:diff_len_positive, :]
        positive_test = pd.concat([reviews, (positive_test)])
        # remain test - substract diff between remain_postive and reviews
        remain_positive = remain_positive.iloc[(diff_len_positive + 1) :, :]

    # total test size
    test_total = round(total * test_size)
    # calculate the remaining to be added to test
    total_remain_to_test = test_total - len(positive_test)
    # remain - all negative + remain postive
    remain = pd.concat([negative, (remain_positive)])
    # remain will go to test
    remain_to_test = remain.iloc[:total_remain_to_test, :]
    # will go to train
    train = remain.iloc[(total_remain_to_test + 1) :, :]
    # test concat reviews and positive and remain to test
    test = pd.concat([positive_test, (remain_to_test)])

    return train, test


def export_dataset(export_folder: str, export: Dict[str, Any]) -> None:
    timestamp: int = int(time.time())
    folder: str = f"{export_folder}/{timestamp}"
    if len(export["arr_train"]) > 1:
        if not os.path.exists(folder):
            os.makedirs(folder)

        export["arr_train"].to_csv(f"{folder}/dataset_train_{timestamp}.csv")
        if len(export["arr_test"]) > 1:
            export["arr_test"].to_csv(f"{folder}/dataset_test_{timestamp}.csv")
        if len(export["arr_dev"]) > 1:
            export["arr_dev"].to_csv(f"{folder}/dataset_dev_{timestamp}.csv")

        with open(f"{folder}/export_config_{timestamp}.json", "w+") as outfile:
            json.dump(export["config"], outfile, ensure_ascii=True, indent=4)

        output: str = typer.style(folder, fg=typer.colors.GREEN, bold=True)
        typer.echo(f"{InfoMessage.path} {output}")


def get_records(mongo: str, source: str, data_split: Dict[str, Any]) -> List[Dict]:
    client: MongoClient = pymongo.MongoClient(mongo)
    db: Database = client["claimdetection"]

    filters: Dict[str, List[Dict[str, Any]]] = copy.deepcopy(data_split["filters"])
    filters["$and"].append({"document.source": source})

    if source == SourceEnum.editor:
        filters["$and"].append({"document.status": "FINISHED"})

    result: CommandCursor = db.sentence.aggregate(
        [
            {"$match": filters},
            {"$project": data_split["project"]},
        ]
    )
    records: List[Dict[str, Any]] = [doc for doc in result]
    return records


def split_dataset(
    total: int, dataset_split: Dict[str, Any], duplicates: bool, reviews: bool
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    df: DataFrame = pd.DataFrame.from_records(dataset_split["records"])

    # Drop duplicates
    if duplicates:
        prev_len = len(df)
        df = df.drop_duplicates(subset=["text"], keep="last")
        current_len = len(df)
        if prev_len == current_len:
            progress(total, label=f"{InfoMessage.duplicates}", update=3)
        else:
            progress(total, label=f"{InfoMessage.dropped}", update=3)

    # Split 100 0 0
    if dataset_split["train_size"] == 1:
        return df, None, None

    # Split X X 0
    progress(total, label=f"{InfoMessage.labelsplit}", update=4)
    if reviews and "reviews" in df.columns:
        train, pretest = dataset_reviews_train_test_split(df, dataset_split)
    else:
        train, pretest = dataset_train_test_split(
            df, dataset_split["random_state"], dataset_split["train_size"], dataset_split["target"]
        )
    if not (dataset_split["test_size"] > 0 and dataset_split["dev_size"] > 0):
        return train, pretest, None

    # Split X X X
    test_dev_size: int = dataset_split["test_size"] + dataset_split["dev_size"]
    test_size: float = round(((100 * dataset_split["test_size"]) / test_dev_size) / 100, 2)
    test, dev = dataset_train_test_split(pretest, dataset_split["random_state"], test_size, dataset_split["target"])
    return train, test, dev


def generate_dataset(mongo: str, folder: str, data_split: Dict[str, Any]) -> None:
    arr_train: DataFrame = pd.DataFrame()
    arr_dev: DataFrame = pd.DataFrame()
    arr_test: DataFrame = pd.DataFrame()
    total: int = 5
    typer.echo("\n\r")
    if not data_split["arr_source"]:
        catch_error(f'source - {ErrorMessage.source} - {data_split["arr_source"]}')

    for source in data_split["arr_source"]:
        duplicates = False
        reviews = False
        typer.echo(f"{InfoMessage.processing} {source}")

        # Get records
        progress(total, label=f"{InfoMessage.labelrecords}", update=1)
        records: List[Dict[str, Any]] = get_records(mongo, source, data_split)

        count: int = len(records)
        if not count > 0:
            typer.echo(typer.style(f"{InfoMessage.notfound}\n\r", fg=typer.colors.BLUE, bold=True))
            continue

        # Read splits
        progress(total, label=f"{InfoMessage.labelread}", update=2)
        train_size, test_size, dev_size = split_sizes(data_split["source"][source])

        # Split dataset train/test/dev
        dataset_split: Dict[str, Any] = {
            "random_state": data_split["random_state"],
            "records": records,
            "target": data_split["target"],
            "train_size": train_size,
            "test_size": test_size,
            "dev_size": dev_size,
        }

        if "duplicates" in data_split["export_config"]:
            duplicates = True

        if "reviews" in data_split["export_config"]:
            reviews = True

        train, *test = split_dataset(total, dataset_split, duplicates, reviews)

        # Save dataset, concat to previous source split
        progress(total, label=f"{InfoMessage.labelsave}", update=5)
        arr_train = pd.concat([arr_train, train])
        arr_test = pd.concat([arr_test, (test[0])])
        if len(test) > 1:
            arr_dev = pd.concat([arr_dev, (test[1])])

        typer.echo("\n\r")

    export: Dict[str, Any] = {
        "config": data_split["export_config"],
        "arr_train": arr_train,
        "arr_dev": arr_dev,
        "arr_test": arr_test,
    }
    export_dataset(folder, export)
