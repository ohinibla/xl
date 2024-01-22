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


def load() -> dict:
    values = {}
    p = Path(".")
    for xp in list(p.glob("*.xlsx")):
        wb = load_workbook(filename=xp, data_only=True)
        ws = wb.active
        colA = ws["A"]
        for v in colA:
            _v = v.value
            num = values.get(_v, (0, []))[0] + 1
            fn = values.get(_v, (0, []))[1] + [str(xp)]
            values[_v] = (num, fn)
    return values


def edit(valuesDict) -> None:
    p = Path(".")
    for xp in list(p.glob("*.xlsx")):
        wb = load_workbook(filename=xp, data_only=True)
        ws = wb.active
        colA = ws["A"]
        for cell in colA:
            for cell in colA:
                if valuesDict[cell.value][0] > 1:
                    cell.font = Font(color="FF0000")
                    for i, x in enumerate(set(valuesDict[cell.value][1])):
                        ws.cell(row=cell.row, column=cell.column +
                                i + 1, value=x)
        wb.save(filename=xp)


def get_files_values(files: set) -> dict:
    values = {}
    for xp in files:
        wb = load_workbook(filename=xp, data_only=True)
        ws = wb.active
        colA = ws["A"]
        # for v in ws.values:
        for v in colA:
            _v = v.value
            num = values.get(_v, (0, []))[0] + 1
            fn = values.get(_v, (0, []))[1] + [str(xp)]
            values[_v] = (num, fn)
    return values


async def edit_files_values(
    valuesDict: dict, files: set, make_copy: bool, show_dup_origin: bool
) -> None:
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
                            value=x.split("/")[-1],
                        )
        if make_copy:
            fp.mkdir(exist_ok=True)
            fp = fp.resolve()
            xp_file_name = xp.split("/")[-1]
            wb.save(filename=fp / xp_file_name)
        else:
            wb.save(xp)
        await asyncio.sleep(0)


def create_main(path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    for row_index, row in enumerate(
        ws.iter_rows(min_row=3, max_col=31, max_row=403), 1
    ):
        for col_index, cell in enumerate(row, 1):
            cell.value = f"='{path}\\[{col_index}.xlsx]Sheet'!A{row_index}"
    wb.save("report.xlsx")


# ----------------- test ----------------------
def main() -> None:
    try:
        current_directory = Path(".").resolve()
        generate_days(days=31, numbers=400)
        print(
            "[bold magenta]test case months added[/bold magenta]", ":white_check_mark:"
        )
        # create_main(current_directory)
        print(
            "[bold magenta]report created successfully![/bold magenta]",
            ":white_check_mark:",
        )
        print(f"Done with no error")
    except Exception as e:
        print(f"Error: {e}")


def test(_days: int, numbers: int) -> None:
    try:
        generate_days(days=_days, numbers=numbers)
        print(
            "[bold magenta]test case months added[/bold magenta]", ":white_check_mark:"
        )
        # _v = load()
        # edit(_v)
        # print("[bold magenta]Done[/bold magenta]", ":white_check_mark:")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test(31, 500)
