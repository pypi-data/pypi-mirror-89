from typing import Optional
from wxltz.models import Proportion
import wxltz.utils as utils
from wxltz import __version__
import pywal
import typer

app = typer.Typer()


def file_exists_callback(path: str) -> Optional[str]:
    return pywal.image.get(path)


def version_callback(val: bool) -> None:
    if val:
        typer.secho(
            f"wxltz verison: {__version__}", fg=typer.colors.BRIGHT_WHITE, bold=True
        )
        raise typer.Exit()


@app.command()
def main(
    img: str = typer.Argument(
        ..., help="Path to Image", metavar="IMAGE", callback=file_exists_callback
    ),
    set_wallpaper: bool = typer.Option(
        False, "-w", "--wallpaper", help="Set Wallpaper"
    ),
    backend: str = typer.Option(
        "wal", "-b", "--backend", help="Backend for fetching colors", metavar="BACKEND"
    ),
    version: Optional[bool] = typer.Option(
        False, "--version", callback=version_callback, show_default=False
    ),
    shade_factor: float = typer.Option(
        0.2,
        "-s",
        "--shade",
        help="Shade factor to apply to colors 1 through 7",
    ),
    to_reload: bool = typer.Option(
        False, "-r", "--reload", help="Reload Sway, Waybar, etc."
    ),
):
    """
    Wrapper library for pywal to generate more diverse colors
    """
    all_colors = pywal.colors.get(img=img, backend=backend)
    colors, special = all_colors["colors"], all_colors["special"]
    # make color1 - color7 darker
    shade_factor = Proportion(shade_factor)
    for i in range(1, 8):
        color = f"color{i}"
        color_hsv = utils.hex_to_hsv(colors[color])
        shaded = utils.shade(color_hsv, shade_factor)
        colors[color] = utils.hsv_to_hex(shaded)
    # generate lighter shades of color0
    dark_hsv = utils.hex_to_hsv(colors["color0"])
    for i in range(3):
        # TODO: Find a shade_factor that ensures a valid hex is returned
        special[f"gray{i}"] = utils.hsv_to_hex(
            utils.shade(dark_hsv, Proportion(0.2 * i), "tint")
        )
    pywal.export.every(all_colors)
    pywal.sequences.send(all_colors)
    typer.secho(
        "🌈 wxltz Successfully set and exported colors 🌈",
        fg=typer.colors.BRIGHT_GREEN,
        bold=True,
    )
    pywal.colors.palette()
    if set_wallpaper:
        pywal.wallpaper.change(img)
        typer.secho(
            f"📸 wxltz Successfully changed wallpaper to {img} 📸",
            fg=typer.colors.BRIGHT_GREEN,
            bold=True,
        )
    if to_reload:
        pywal.reload.env()
