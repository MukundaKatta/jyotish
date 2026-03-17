"""CLI for Jyotish."""
from __future__ import annotations
import click
from datetime import datetime
from rich.console import Console
from .chart.calculator import ChartCalculator
from .chart.planets import PlanetDatabase
from .analysis.yoga import YogaDetector
from .analysis.dasha import DashaCalculator
from .analysis.strength import PlanetStrengthCalculator
from .report import JyotishReport
from .models import Graha

console = Console()


@click.group()
def cli() -> None:
    """Jyotish - Vedic Astrology Engine."""
    pass


@cli.command()
@click.argument("name")
@click.argument("date", type=str)
@click.argument("time", type=str)
@click.argument("place", type=str)
@click.option("--lat", type=float, default=28.6139, help="Latitude")
@click.option("--lon", type=float, default=77.2090, help="Longitude")
def chart(name: str, date: str, time: str, place: str, lat: float, lon: float) -> None:
    """Generate birth chart. DATE: YYYY-MM-DD, TIME: HH:MM"""
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    calc = ChartCalculator()
    birth_chart = calc.calculate(name, dt, place, lat, lon)
    report = JyotishReport()
    report.display_chart(birth_chart)
    report.display_houses(birth_chart)

    # Detect yogas
    detector = YogaDetector()
    yogas = detector.detect_all(birth_chart)
    if yogas:
        report.display_yogas(yogas)

    # Calculate dashas
    moon = next((p for p in birth_chart.planets if p.name == Graha.CHANDRA), None)
    if moon:
        dasha_calc = DashaCalculator()
        dashas = dasha_calc.calculate_mahadashas(moon, dt)
        report.display_dashas(dashas)


@cli.command()
@click.argument("graha", type=click.Choice([g.value for g in Graha], case_sensitive=False))
def planet_info(graha: str) -> None:
    """Show information about a graha."""
    db = PlanetDatabase()
    g = Graha(graha)
    props = db.get_properties(g)
    console.print(f"\n[bold magenta]{g.value}[/bold magenta] ({props['english']})")
    for k, v in props.items():
        if k != "english":
            console.print(f"  [bold]{k}:[/bold] {v}")
    console.print(f"  [bold]Friends:[/bold] {', '.join(f.value for f in db.get_friends(g))}")
    console.print(f"  [bold]Enemies:[/bold] {', '.join(f.value for f in db.get_enemies(g))}")
    ex = db.get_exaltation(g)
    if ex:
        console.print(f"  [bold]Exalted in:[/bold] {ex[0].value} at {ex[1]} degrees")


if __name__ == "__main__":
    cli()
