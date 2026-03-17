"""Report generation for Jyotish."""
from __future__ import annotations
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .models import BirthChart, Yoga, Dasha


class JyotishReport:
    def __init__(self) -> None:
        self.console = Console()

    def display_chart(self, chart: BirthChart) -> None:
        self.console.print(Panel(f"[bold]{chart.name}[/bold]\nBorn: {chart.birth_datetime}\nPlace: {chart.birth_place}\nLagna: {chart.lagna.value}",
                                  title="Birth Chart (Kundli)"))
        table = Table(title="Planetary Positions")
        table.add_column("Graha", style="bold cyan")
        table.add_column("Rashi")
        table.add_column("Nakshatra")
        table.add_column("House", style="green")
        table.add_column("Dignity", style="yellow")
        table.add_column("Retro")
        for p in chart.planets:
            table.add_row(p.name.value, p.rashi.value, f"{p.nakshatra.value} P{p.nakshatra_pada}",
                         str(p.house), p.dignity, "R" if p.is_retrograde else "")
        self.console.print(table)

    def display_houses(self, chart: BirthChart) -> None:
        table = Table(title="House (Bhava) Chart")
        table.add_column("House", style="bold")
        table.add_column("Rashi", style="cyan")
        table.add_column("Lord", style="yellow")
        table.add_column("Planets", style="green")
        table.add_column("Significations")
        for h in chart.houses:
            planets = ", ".join(g.value for g in h.planets) if h.planets else "-"
            sigs = ", ".join(h.significations[:3])
            table.add_row(str(h.number), h.rashi.value, h.lord.value, planets, sigs)
        self.console.print(table)

    def display_yogas(self, yogas: list[Yoga]) -> None:
        table = Table(title="Yogas Detected")
        table.add_column("Yoga", style="bold magenta")
        table.add_column("Type", style="green")
        table.add_column("Strength")
        table.add_column("Description")
        for y in yogas:
            ytype = "Benefic" if y.is_benefic else "Malefic"
            table.add_row(y.name, ytype, y.strength, y.description)
        self.console.print(table)

    def display_dashas(self, dashas: list[Dasha]) -> None:
        table = Table(title="Vimshottari Maha Dasha Periods")
        table.add_column("Planet", style="bold cyan")
        table.add_column("Start", style="green")
        table.add_column("End", style="red")
        table.add_column("Years")
        for d in dashas:
            table.add_row(d.planet.value, d.start_date, d.end_date, f"{d.duration_years:.1f}")
        self.console.print(table)
