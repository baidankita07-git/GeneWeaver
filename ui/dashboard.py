from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import Iterable, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    DataTable, Footer, Header, Label, ProgressBar, RichLog, Static
)
from textual.reactive import reactive
from rich.text import Text


BASES = "ACGT"


def decode_dna(encoded: Iterable[int]) -> str:
    """Convert encoded bases (0=A, 1=C, 2=G, 3=T) to readable DNA."""
    return "".join(BASES[int(x)] if 0 <= int(x) < 4 else "N" for x in encoded)


def highlight_mismatches(target: Iterable[int], guide: Iterable[int]) -> Text:
    """Return a Rich Text sequence with mismatched target bases in red."""
    target_values = [int(x) for x in target]
    guide_values = [int(x) for x in guide]
    output = Text()
    for i, base in enumerate(target_values):
        letter = BASES[base] if 0 <= base < 4 else "N"
        if i < len(guide_values) and base != guide_values[i]:
            output.append(letter, style="bold red on #3a2020")
        else:
            output.append(letter, style="green")
    return output


class GeneWeaverDashboard(App):
    """Member 4 TUI: live run metrics, chunk progress, and mismatch table."""

    TITLE = "GeneWeaver | CRISPR Alignment Monitor"
    SUB_TITLE = "Member 4 — TUI Dashboard & Mismatch Visualization"
    CSS = """
    Screen { layout: vertical; }
    #topline { height: 3; padding: 1; background: $panel; }
    #metrics { height: 7; }
    .metric { width: 1fr; border: round $accent; padding: 1; margin: 0 1 0 0; }
    #progress-box { height: 5; padding: 1; border: round $primary; margin: 1 0; }
    #main { height: 1fr; }
    #matches { width: 3fr; border: round $accent; padding: 1; }
    #log-panel { width: 2fr; border: round $accent; padding: 1; }
    #match-table { height: 1fr; }
    #log { height: 1fr; }
    .heading { text-style: bold; color: $accent; }
    .value { text-style: bold; }
    """
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "clear_log", "Clear log"),
    ]

    completed_chunks = reactive(0)
    total_chunks = reactive(1)
    matches_found = reactive(0)
    positions_processed = reactive(0)
    gpu_memory_mb = reactive(0.0)
    gpu_utilization = reactive(0.0)
    backend_status = reactive("Starting")
    elapsed_seconds = reactive(0.0)

    def __init__(self, guide_rna: Optional[Iterable[int]] = None, **kwargs):
        super().__init__(**kwargs)
        self.guide_rna = list(guide_rna) if guide_rna is not None else []
        self._started_at = datetime.now()
        self._recent_matches = deque(maxlen=500)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Initializing alignment monitor…", id="topline")
        with Horizontal(id="metrics"):
            with Vertical(classes="metric"):
                yield Label("BACKEND", classes="heading")
                yield Static("Starting", id="backend-value", classes="value")
            with Vertical(classes="metric"):
                yield Label("GPU MEMORY", classes="heading")
                yield Static("0 MB", id="gpu-memory", classes="value")
            with Vertical(classes="metric"):
                yield Label("GPU UTILIZATION", classes="heading")
                yield Static("0%", id="gpu-util", classes="value")
            with Vertical(classes="metric"):
                yield Label("OFF-TARGETS", classes="heading")
                yield Static("0", id="match-count", classes="value")
        with Vertical(id="progress-box"):
            yield Label("Genome scan progress", classes="heading")
            yield ProgressBar(total=100, show_eta=True, id="progress")
            yield Static("0 / 1 chunks · 0 positions processed", id="progress-label")
        with Horizontal(id="main"):
            with Vertical(id="matches"):
                yield Label("Recent candidate sites (red bases = mismatches)", classes="heading")
                table = DataTable(id="match-table", zebra_stripes=True)
                table.add_columns("Position", "Mismatches", "Target sequence", "Guide RNA")
                yield table
            with Vertical(id="log-panel"):
                yield Label("Run log", classes="heading")
                yield RichLog(id="log", wrap=True, markup=True, highlight=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#log", RichLog).write("[bold green]Dashboard ready.[/bold green]")
        self.set_interval(1.0, self._refresh_elapsed)

    def _refresh_elapsed(self) -> None:
        self.elapsed_seconds = (datetime.now() - self._started_at).total_seconds()
        self.query_one("#topline", Static).update(
            f"GeneWeaver • {self.backend_status} • Elapsed {self.elapsed_seconds:.1f}s"
        )

    def watch_backend_status(self, value: str) -> None:
        if self.is_mounted:
            self.query_one("#backend-value", Static).update(value)

    def watch_gpu_memory_mb(self, value: float) -> None:
        if self.is_mounted:
            self.query_one("#gpu-memory", Static).update(f"{value:,.0f} MB")

    def watch_gpu_utilization(self, value: float) -> None:
        if self.is_mounted:
            self.query_one("#gpu-util", Static).update(f"{value:.0f}%")

    def watch_matches_found(self, value: int) -> None:
        if self.is_mounted:
            self.query_one("#match-count", Static).update(f"{value:,}")

    def watch_completed_chunks(self, value: int) -> None:
        self._update_progress()

    def watch_total_chunks(self, value: int) -> None:
        self._update_progress()

    def watch_positions_processed(self, value: int) -> None:
        self._update_progress()

    def _update_progress(self) -> None:
        if not self.is_mounted:
            return
        total = max(1, self.total_chunks)
        percent = min(100, int(self.completed_chunks * 100 / total))
        self.query_one("#progress", ProgressBar).update(progress=percent)
        self.query_one("#progress-label", Static).update(
            f"{self.completed_chunks:,} / {total:,} chunks · "
            f"{self.positions_processed:,} positions processed"
        )

    def log_event(self, message: str) -> None:
        if self.is_mounted:
            self.query_one("#log", RichLog).write(message)

    def set_run_status(self, status: str) -> None:
        self.backend_status = status
        self.log_event(f"[cyan]{status}[/cyan]")

    def update_hardware(self, memory_mb: float = 0.0, utilization: float = 0.0) -> None:
        """Call with sampled GPU metrics; pass 0/0 when no compatible GPU is available."""
        self.gpu_memory_mb = max(0.0, float(memory_mb))
        self.gpu_utilization = max(0.0, min(100.0, float(utilization)))

    def set_chunk_progress(self, completed: int, total: int, positions: int) -> None:
        self.total_chunks = max(1, int(total))
        self.completed_chunks = max(0, min(int(completed), self.total_chunks))
        self.positions_processed = max(0, int(positions))

    def add_match(
        self,
        position: int,
        mismatch_count: int,
        target_encoded: Iterable[int],
        guide_encoded: Optional[Iterable[int]] = None,
    ) -> None:
        """Add one candidate result. Position is a zero-based genome coordinate."""
        target = list(target_encoded)
        guide = list(guide_encoded) if guide_encoded is not None else self.guide_rna
        if mismatch_count < 0:
            return
        table = self.query_one("#match-table", DataTable)
        target_text = highlight_mismatches(target, guide)
        guide_text = decode_dna(guide)
        table.add_row(
            f"{int(position):,}",
            str(int(mismatch_count)),
            target_text,
            guide_text,
        )
        self.matches_found += 1
        self._recent_matches.append((int(position), int(mismatch_count)))
        self.query_one("#log", RichLog).write(
            f"[yellow]Candidate[/yellow] at position {int(position):,}: "
            f"{int(mismatch_count)} mismatch(es)"
        )

    def add_match_strings(
        self, position: int, mismatch_count: int, target: str, guide: str
    ) -> None:
        """Convenience adapter if the engine already returns A/C/G/T strings."""
        table = self.query_one("#match-table", DataTable)
        rendered = Text()
        for i, base in enumerate(target):
            if i < len(guide) and base != guide[i]:
                rendered.append(base, style="bold red on #3a2020")
            else:
                rendered.append(base, style="green")
        table.add_row(f"{position:,}", str(mismatch_count), rendered, guide)
        self.matches_found += 1

    def finish_run(self, summary: str = "Alignment completed") -> None:
        self.backend_status = "Completed"
        self.log_event(f"[bold green]{summary}[/bold green]")
        self.set_chunk_progress(self.total_chunks, self.total_chunks, self.positions_processed)

    def action_clear_log(self) -> None:
        self.query_one("#log", RichLog).clear()


def main() -> None:
    """Run the dashboard with demo data; useful before integrating the engine."""
    import random
    import threading
    import time

    guide = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    app = GeneWeaverDashboard(guide_rna=guide)

    def demo_worker() -> None:
        time.sleep(1)
        app.call_from_thread(app.set_run_status, "CPU demo mode")
        total = 20
        for chunk in range(1, total + 1):
            time.sleep(0.25)
            app.call_from_thread(app.set_chunk_progress, chunk, total, chunk * 100_000)
            if chunk % 3 == 0:
                target = guide.copy()
                idx = random.randrange(len(target))
                target[idx] = (target[idx] + 1) % 4
                app.call_from_thread(app.add_match, chunk * 100_000, 1, target, guide)
        app.call_from_thread(app.finish_run, "Demo completed. Connect the real scheduler to replace this worker.")

    # Textual's run loop owns the UI; update it safely from a worker thread.
    def start_worker():
        threading.Thread(target=demo_worker, daemon=True).start()

    app.run()
    # Demo updates are intentionally illustrative; use the integration pattern in README.

if __name__ == "__main__":
    main()
