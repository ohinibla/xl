import asyncio
import random
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from rich import print
from rich.progress import track


def generate_random_num() -> str:
    """
    This function generates a random phone number.

    Returns:
        str: A string representing a random phone number with known prefixes.
    """
    prefix = random.choice(["12", "35", "36", "02", "18"])
    num = [str(i) for i in range(7)]
    random.shuffle(num)
    num = "".join(num)
    num = f"09{prefix}{num}"
    return num


def generate_days(days: int, numbers: int) -> None:
    (Path(".") / "months").mkdir(exist_ok=True)
    for i in track(range(1, days + 1)):
        wb = Workbook()
        ws = wb.active
        for row in ws.iter_rows(min_row=1, max_col=1, max_row=numbers):
            for cell in row:
                cell.value = generate_random_num()
        wb.save(Path(".") / "months" / f"{i}.xlsx")


def get_files_values(files: set) -> dict:
    values = {}
    for xp in files:
        wb = load_workbook(filename=xp, data_only=True)
        ws = wb.active
        colA = ws["A"]
        for v in colA:
            _v = v.value
            num = values.get(_v, (0, []))[0] + 1
            fn = values.get(_v, (0, []))[1] + [str(xp)]
            values[_v] = (num, fn)
    return values


async def edit_files_values(
    valuesDict: dict,
    files: set,
    make_copy: bool,
    show_dup_origin: bool,
    test: bool,
) -> None:
    path_delimiter = "\\" if test else "/"
    fp = Path(".") / "data"
    for xp in files:
        wb = load_workbook(filename=xp, data_only=True)
        ws = wb.active
        colA = ws["A"]
        for cell in colA:
            if valuesDict[cell.value][0] > 1:
                cell.font = Font(color="FF0000")
                if show_dup_origin:
                    for i, x in enumerate(set(valuesDict[cell.value][1])):
                        ws.cell(
                            row=cell.row,
                            column=cell.column + i + 1,
                            value=x.split(path_delimiter)[-1],
                        )
        if make_copy:
            fp.mkdir(exist_ok=True)
            fp = fp.resolve()
            xp_file_name = xp.split(path_delimiter)[-1]
            wb.save(filename=fp / xp_file_name)
        else:
            wb.save(xp)
        await asyncio.sleep(0)


# ----------------- test ----------------------
async def test() -> None:
    print(
        "[bold magenta]test case months added[/bold magenta]",
        "------------------ :white_check_mark:",
    )

    fp = Path(".") / "months"
    xl_files = fp.glob("*.xlsx")
    test_files = set([x.resolve().__str__() for x in xl_files])

    _v = get_files_values(test_files)
    await edit_files_values(
        valuesDict=_v, files=test_files, make_copy=True, show_dup_origin=True, test=True
    )
    print(
        "[bold magenta]edited files[/bold magenta]",
        "---------------------------- :white_check_mark:",
    )


if __name__ == "__main__":
    generate_days(days=31, numbers=400)
    asyncio.run(test())
