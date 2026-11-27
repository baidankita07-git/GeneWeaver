"""Launch the Member 4 dashboard with synthetic data to test the UI."""
import random
from ui.dashboard import GeneWeaverDashboard


class DemoDashboard(GeneWeaverDashboard):
    def on_mount(self) -> None:
        super().on_mount()
        self.set_run_status("CPU demo mode")
        self._demo_chunk = 0
        self._demo_guide = self.guide_rna or [0, 1, 2, 3] * 5
        self.total_chunks = 20
        self.set_interval(0.35, self._demo_tick)

    def _demo_tick(self) -> None:
        if self._demo_chunk >= self.total_chunks:
            return
        self._demo_chunk += 1
        self.set_chunk_progress(
            self._demo_chunk, self.total_chunks, self._demo_chunk * 100_000
        )
        if self._demo_chunk % 3 == 0:
            target = self._demo_guide.copy()
            idx = random.randrange(len(target))
            target[idx] = (target[idx] + 1) % 4
            self.add_match(
                self._demo_chunk * 100_000, 1, target, self._demo_guide
            )
        if self._demo_chunk == self.total_chunks:
            self.finish_run("Demo completed. Replace synthetic updates with scheduler events.")


if __name__ == "__main__":
    DemoDashboard(
        guide_rna=[0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    ).run()
