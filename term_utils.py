import altair as alt
import pandas as pd
import tempfile
import polars as pl
import visidata as vd
import subprocess
from pathlib import Path


def render_alt(chart: alt.Chart):
    with tempfile.NamedTemporaryFile(
        suffix=".png", delete=False
    ) as tmp:
        chart.save(tmp.name, format="png")
        # subprocess.run(["kitty", "icat", tmp.name])
        subprocess.run(["img2sixel", tmp.name])


def display(df: pl.DataFrame):
    vd.vd.view_pandas(df.to_pandas(use_pyarrow_extension_array=False))


def wdf(df: pl.DataFrame, name: str):
    directory_path = Path("/tmp/tmp-visidata/")
    directory_path.mkdir(parents=True, exist_ok=True)
    df.write_parquet(directory_path / f"{name}.parquet")


def display2(df: pl.DataFrame):
    # write dataframe to a temporary CSV
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
    df.write_parquet(tmp.name)
    tmp.close()

    # spawn a new Zellij pane running visidata on the CSV
    # Need to include PATH to vd in loginshell
    _ = subprocess.Popen(
        [
            "zellij",
            "action",
            "new-pane",
            "--direction",
            "down",
            "--",
            "vd",
        ]
    )


if __name__ == "__main__":
    # Example chart
    data = pd.DataFrame({"x": [1, 2, 3], "y": [4, 2, 5]})
    display(pl.from_pandas(data))
    chart = (
        alt.Chart(data)
        .mark_line(color="red", strokeWidth=2)
        .encode(x="x", y="y")
    )
    render_alt(chart)
