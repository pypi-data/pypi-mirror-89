from datetime import datetime
from typing import Any, Dict, List, Tuple

import typer
from nwt_dataset_cli.dtos import ErrorMessage, InfoMessage, SourceEnum
from nwt_dataset_cli.helpers.helpers import catch_error, date_diff, get_sources_data
from typer.models import OptionInfo


def option_duplicates(duplicates: bool) -> None:
    if not type(duplicates) == bool:
        catch_error(f"duplicates - {ErrorMessage.boolean} - {duplicates}")
    typer.echo(f"duplicates: {duplicates}")


def option_end_date(
    end_date: datetime, filters: Dict[str, List[Dict[str, Any]]], start_date: datetime = None
) -> Dict[str, List[Dict[str, Any]]]:
    if start_date and isinstance(start_date, datetime):
        date_diff(start_date, end_date)
    typer.echo(f"end date: {end_date}")
    end_date_iso: datetime = datetime.fromisoformat(end_date.isoformat())
    filters["$and"].append({"document.date": {"$lte": end_date_iso}})
    return filters


def option_languages(languages: List[str], filters: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    if not isinstance(languages, list):
        catch_error(f"languages - {ErrorMessage.languages} - {languages}")
    typer.echo(f"languages: {languages}")
    for language in languages:
        filters["$and"].append({"lang": language})
    return filters


def option_none(option: Any) -> bool:
    return isinstance(option, OptionInfo)


def option_start_date(
    start_date: datetime, filters: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, List[Dict[str, Any]]]:
    typer.echo(f"start date: {start_date}")
    start_date_iso: datetime = datetime.fromisoformat(start_date.isoformat())
    filters["$and"].append({"document.date": {"$gte": start_date_iso}})
    return filters


def option_source(
    source: List[SourceEnum], arr_source: List[str], sources_split: Dict[str, str]
) -> Tuple[List[str], Dict[str, str]]:
    if option_none(source):
        catch_error(f"source - {ErrorMessage.source} - {source}")
    typer.echo(InfoMessage.sourcesplit)
    arr_source, sources_split = get_sources_data(source, arr_source, sources_split)
    typer.echo("\n\r")
    typer.echo(typer.style(InfoMessage.create, fg=typer.colors.BRIGHT_BLUE, bold=True))
    typer.echo(f"sources: {sources_split}")
    return arr_source, sources_split


def option_random_state(random_state: int) -> int:
    if not type(random_state) == int:
        catch_error(f"random_state - {ErrorMessage.isinteger} - {random_state}")
    random_state = int(random_state)
    typer.echo(f"random state: {random_state}")
    return random_state


def option_reviews(reviews: bool, project: Dict[str, Any]) -> Dict[str, Any]:
    if not type(reviews) == bool:
        catch_error(f"reviews - {ErrorMessage.boolean} - {reviews}")
    project["reviews"] = 1
    typer.echo(f"reviews: {reviews}")
    return project


def option_target(
    target: str, filters: Dict[str, List[Dict[str, Any]]], project: Dict[str, Any]
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Any]]:
    typer.echo(f"target: {target}")
    filters["$and"].append({target: {"$exists": True}})
    project[target] = 1
    return filters, project


def option_translations(
    translate: bool, languages: List[str], filters: Dict[str, List[Dict[str, Any]]], project: Dict[str, Any]
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Any]]:
    if not type(translate) == bool:
        catch_error(f"translate - {ErrorMessage.boolean} - {translate}")
    if not isinstance(languages, list):
        catch_error(f"languages - {ErrorMessage.languages} - {languages}")
    typer.echo(f"languages: {languages}")
    typer.echo(f"translate: {True}")
    for language in languages:
        filters["$and"].append({f"translation.{language}": {"$exists": True}})
        project[f"text_{language}"] = f"$translation.{language}"
    return filters, project
