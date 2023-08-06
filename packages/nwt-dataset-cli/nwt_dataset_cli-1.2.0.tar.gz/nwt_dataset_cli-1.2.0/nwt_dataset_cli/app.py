import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer

from nwt_dataset_cli.dtos import ErrorMessage, HelpMessage, InfoMessage, SourceEnum, TargetEnum
from nwt_dataset_cli.helpers.helpers import date_callback, date_from_string
from nwt_dataset_cli.helpers.options import (
    option_duplicates,
    option_end_date,
    option_languages,
    option_none,
    option_random_state,
    option_reviews,
    option_source,
    option_start_date,
    option_target,
    option_translations,
)
from nwt_dataset_cli.services.dataset_service import generate_dataset

app = typer.Typer()

app = typer.Typer(add_completion=False)


@app.callback()
def callback():
    """
    Dataset Generate CLI app.
    Use the create command and a dataset will be created.
    """
    typer.echo("\n\r")


@app.command()
def create(
    duplicates: Optional[bool] = typer.Option(
        False,
        "--duplicates",
        "-du",
        help=HelpMessage.duplicates,
    ),
    end_date: Optional[datetime] = typer.Option(
        None,
        "--end",
        "-en",
        formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"],
        help=HelpMessage.end,
    ),
    folder: Optional[str] = typer.Option(
        "./datasets",
        "--folder",
        "-fo",
        case_sensitive=False,
        help=HelpMessage.folder,
    ),
    languages: Optional[List[str]] = typer.Option(
        None,
        "--lang",
        "-la",
        case_sensitive=False,
        help=HelpMessage.lang,
    ),
    mongo: Optional[str] = typer.Option(
        "mongodb://localhost:27017",
        "--mongo",
        "-mo",
        case_sensitive=False,
        help=HelpMessage.mongo,
    ),
    random_state: int = typer.Option(..., "--random", "-ra", help=HelpMessage.ramdom),
    reviews: Optional[bool] = typer.Option(
        False,
        "--reviews",
        "-re",
        help=HelpMessage.reviews,
    ),
    source: List[SourceEnum] = typer.Option(
        ...,
        "--source",
        "-so",
        case_sensitive=False,
        help=HelpMessage.source,
    ),
    start_date: Optional[datetime] = typer.Option(
        None,
        "--start",
        "-st",
        formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"],
        help=HelpMessage.start,
    ),
    target: TargetEnum = typer.Option(
        ...,
        "--target",
        "-ta",
        case_sensitive=False,
        help=HelpMessage.target,
    ),
    translate: Optional[bool] = typer.Option(
        False,
        "--translate",
        "-tr",
        help=HelpMessage.translations,
    ),
) -> None:
    """
    Create a dataset with custom parameters.
    """
    filters: Dict[str, List[Dict[str, Any]]] = {"$and": []}
    project: Dict[str, Any] = {"_id": 1, "text": 1, "date": "$document.date"}
    sources_split: Dict[str, str] = {}
    arr_source: List[str] = []
    export_config: Dict[str, Any] = {}

    try:
        if source:
            arr_source, sources_split = option_source(source, arr_source, sources_split)
            export_config["source"] = sources_split

        if target:
            filters, project = option_target(target.value, filters, project)
            export_config["target"] = target.value

        if duplicates and not option_none(duplicates):
            option_duplicates(duplicates)
            export_config["duplicates"] = duplicates

        if reviews and not option_none(reviews):
            project = option_reviews(reviews, project)
            export_config["reviews"] = reviews

        if random_state:
            random_state = option_random_state(random_state)
            export_config["random_state"] = random_state

        if start_date and date_callback(start_date) and not option_none(start_date):
            filters = option_start_date(start_date, filters)
            export_config["start_date"] = start_date.isoformat()

        if end_date and date_callback(end_date) and not option_none(end_date):
            filters = option_end_date(end_date, filters, start_date)
            export_config["end_date"] = end_date.isoformat()

        if languages and not option_none(languages):
            languages = list(languages)
            if translate and not option_none(translate):
                filters, project = option_translations(translate, languages, filters, project)
                export_config["translate"] = True
            else:
                filters = option_languages(languages, filters)
            export_config["languages"] = languages

        data_split: Dict[str, Any] = {
            "arr_source": arr_source,
            "export_config": export_config,
            "filters": filters,
            "project": project,
            "source": sources_split,
            "random_state": random_state,
            "target": target.value,
        }
        generate_dataset(mongo, folder, data_split)
        typer.echo(typer.style(InfoMessage.created, fg=typer.colors.GREEN, bold=True))

    except Exception as err:
        error: str = typer.style(str(err), fg=typer.colors.WHITE, bg=typer.colors.RED)
        typer.echo(f"{ErrorMessage.exception} {error}")
        raise typer.Exit(code=1)


@app.command()
def fromjson(
    mongo: Optional[str] = typer.Option(
        "mongodb://localhost:27017",
        "--mongo",
        "-mo",
        case_sensitive=False,
        help=HelpMessage.mongo,
    ),
    file: Path = typer.Option(
        ...,
        "--file",
        "-fi",
        case_sensitive=False,
        help=HelpMessage.file,
    ),
    folder: Optional[str] = typer.Option(
        "./datasets",
        "--folder",
        "-fo",
        case_sensitive=False,
        help=HelpMessage.folder,
    ),
) -> None:
    """
    Create a dataset from json file.
    """
    try:
        with open(file) as json_file:
            jsondata = json.load(json_file)
            jsondata["mongo"] = mongo
            jsondata["folder"] = folder
            jsondata["target"] = TargetEnum[jsondata["target"]]

            if "start_date" in jsondata:
                jsondata["start_date"] = date_from_string(jsondata["start_date"])
            if "end_date" in jsondata:
                jsondata["end_date"] = date_from_string(jsondata["end_date"])

            create(**jsondata)

    except Exception as err:
        error: str = typer.style(str(err), fg=typer.colors.WHITE, bg=typer.colors.RED)
        typer.echo(f"{ErrorMessage.exception} {error}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
