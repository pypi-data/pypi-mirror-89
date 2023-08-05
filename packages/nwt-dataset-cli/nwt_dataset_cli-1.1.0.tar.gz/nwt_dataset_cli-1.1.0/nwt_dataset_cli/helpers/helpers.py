import time
from datetime import datetime
from typing import Any, Dict, List, NoReturn, Tuple

import typer
from nwt_dataset_cli.dtos import ErrorMessage, SourceEnum


def catch_error(err: str) -> NoReturn:
    error: str = typer.style(err, fg=typer.colors.WHITE, bg=typer.colors.RED)
    raise typer.echo(f"{ErrorMessage.exception} {error}")


def date_callback(date: datetime) -> datetime:
    if date is None:
        catch_error(f"{ErrorMessage.date}")
    return date


def date_diff(start_date: datetime, end_date: datetime):
    if start_date and start_date > end_date:
        catch_error(f"{ErrorMessage.diffdate}")


def date_from_string(date: str) -> datetime:
    try:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return datetime.strptime(date, "%Y-%m-%d")


def progress(total: int, label: str, update: int) -> None:
    with typer.progressbar(length=total, label=label) as progress:
        if update > 0:
            time.sleep(0.5)
            progress.update(update)


def get_sources_data(
    source: Any, arr_source: List[str], sources_split: Dict[str, str]
) -> Tuple[List[str], Dict[str, str]]:
    if type(source) == dict:
        arr_source, sources_split = get_sources_json_data(source, arr_source, sources_split)
    else:
        arr_source, sources_split = get_sources_cli_data(source, arr_source, sources_split)
    return arr_source, sources_split


def get_sources_cli_data(
    source: List[SourceEnum], arr_source: List[str], sources_split: Dict[str, str]
) -> Tuple[List[str], Dict[str, str]]:
    for src in source:
        current_src = src.value
        src_split: str = typer.prompt(src, default="80 10 10")
        arr_source.append(current_src)
        sources_split[current_src] = src_split
        validate_source_split(current_src, src_split)
    return arr_source, sources_split


def get_sources_json_data(
    source: Dict[str, Any], arr_source: List[str], sources_split: Dict[str, str]
) -> Tuple[List[str], Dict[str, str]]:
    for src in source:
        validate_source(src)
        arr_source.append(src)
        sources_split[src] = source[src]
        validate_source_split(src, source[src])
    return arr_source, sources_split


def source_split(src_split: str) -> List[str]:
    return src_split.strip().split(" ")


def source_split_isdigit(source: str, splits: List[str]):
    total_splits = 0
    for split in splits:
        if not split.isdigit():
            catch_error(f"{source} - {ErrorMessage.isinteger} - {split}")
        total_splits += int(split)
    return total_splits


def source_split_len(source: str, splits: List[str]) -> None:
    if len(splits) < 3:
        catch_error(f"{source} - {ErrorMessage.splits} {splits}")


def source_split_total(source: str, total: int) -> None:
    if total != 100:
        catch_error(f"{source} - {ErrorMessage.total} {total}")


def split_sizes(src_split: str) -> Tuple[float, int, int]:
    split: List[str] = src_split.strip().split(" ")
    train_size: float = int(split[0]) / 100
    test_size: int = int(split[1])
    dev_size: int = int(split[2])
    return train_size, test_size, dev_size


def validate_source(source: str) -> None:
    if not hasattr(SourceEnum, source):
        catch_error(f"source - {ErrorMessage.source} - {source}")


def validate_source_split(source: str, src_split: str) -> None:
    split = source_split(src_split)
    source_split_len(source, split)
    total_splits = source_split_isdigit(source, split)
    source_split_total(source, total_splits)
