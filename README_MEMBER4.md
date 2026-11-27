# GeneWeaver — Member 4: TUI Dashboard & Mismatch Visualization

This module provides the Textual terminal dashboard for the GeneWeaver CRISPR alignment project. It is designed to be integrated with the parser, GPU aligner, and Dask scheduler built by other team members.

## Features

- Live chunk progress and positions processed
- Backend status and elapsed time
- GPU memory/utilization fields (fed by the engine or a hardware monitor)
- Recent candidate off-target sites in a table
- DNA bases that differ from the guide RNA are highlighted in red
- Run log and keyboard shortcuts (`q` to quit, `c` to clear log)

**Important:** GPU memory/utilization are not magically detected by this UI. The engine must periodically call `update_hardware(...)` with measured values. The project should fall back to CPU mode when CUDA/NVIDIA hardware is unavailable. Do not claim 100x speedup unless it is measured on the same dataset and machine.

## 1. Create a virtual environment

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-member4.txt
```

If PowerShell blocks activation, use:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Run the dashboard

From the project root:
```powershell
python demo_dashboard.py
```

This opens the TUI shell. The dashboard is the UI component; actual alignment results appear when the scheduler/engine calls the methods below.

## 3. Integration contract for Member 2 / Member 1

Create the dashboard in your main runner and pass the encoded guide RNA (0=A, 1=C, 2=G, 3=T):

```python
from ui.dashboard import GeneWeaverDashboard

dashboard = GeneWeaverDashboard(guide_rna=grna)
dashboard.run()
```

For a real app, run the alignment worker in a background thread or Textual worker so the UI event loop remains responsive. From that worker, use `dashboard.call_from_thread(...)` to update UI state:

```python
dashboard.call_from_thread(dashboard.set_run_status, "Dask + CUDA")
dashboard.call_from_thread(dashboard.set_chunk_progress, completed_chunks, total_chunks, positions_processed)
dashboard.call_from_thread(dashboard.update_hardware, gpu_memory_mb, gpu_utilization_percent)
dashboard.call_from_thread(dashboard.add_match, genome_position, mismatch_count, target_encoded, grna)
dashboard.call_from_thread(dashboard.finish_run, "Alignment completed")
```

Only call `call_from_thread` after `dashboard.run()` has started. Do not call UI widgets directly from a Dask worker process. Have the main process receive task results and update the dashboard.

### Suggested result format

For each chunk, the engine/scheduler should provide:
- chunk index and total chunks
- number of genome positions processed
- candidate hit positions
- mismatch count at each candidate
- target sequence window and guide RNA

If your current scheduler returns only a NumPy array of mismatch counts, Member 2 should expose candidate positions as well; otherwise Member 4 cannot accurately display genomic coordinates or target sequence windows.

## 4. Suggested project structure

```text
GeneWeaver/
├── engine/
│   └── gpu_aligner.py          # Member 1
├── scheduler.py                # Member 2
├── parser/                      # Member 3
├── ui/
│   ├── __init__.py
│   └── dashboard.py            # Member 4 (this contribution)
├── demo_dashboard.py
├── requirements-member4.txt
└── README_MEMBER4.md
```

## 5. Git upload process (GitHub)

Run these commands from the existing repository root. Do not create a nested Git repository inside the project.

```powershell
git status
git switch -c feature/member4-tui-dashboard
git add ui/dashboard.py ui/__init__.py demo_dashboard.py requirements-member4.txt README_MEMBER4.md
git commit -m "Add GeneWeaver Textual dashboard and mismatch visualization"
git push -u origin feature/member4-tui-dashboard
```

Then open the GitHub repository in your browser:
1. Open the repository.
2. Select the `feature/member4-tui-dashboard` branch.
3. Click **Compare & pull request**.
4. Set the base branch to your team's integration branch (often `main` or `develop`—confirm with your team).
5. Describe your contribution and create the pull request.
6. Ask the team lead to review and merge it.

### If your team wants you to commit directly to an existing branch

First inspect branches:
```powershell
git branch
git branch -r
```
Switch to the agreed branch, then pull before editing:
```powershell
git switch main
git pull origin main
```
Do not force-push. If Git reports conflicts, stop and resolve them with your team rather than overwriting their work.

## 6. Common Git errors

- `fatal: not a git repository`: run `cd` into the folder containing `.git`.
- `src refspec ... does not match any`: create a commit first, then push the correct branch name.
- `rejected (non-fast-forward)`: run `git pull --rebase origin <your-branch>` only if that branch is yours and you understand any conflicts.
- Authentication prompts: use GitHub's browser/device login or configured SSH; GitHub no longer accepts account passwords for Git operations.

## 7. Team integration notes

The scheduler code shared by your teammate has a likely typo:
```python
def _init_(...)
```
Python constructors must be named:
```python
def __init__(...)
```
Otherwise `GeneDaskScheduler()` will not initialize `cluster` and `client`.

The dashboard expects mismatch count plus candidate position and sequence window to display meaningful hits. Coordinate the result schema with Members 1–3 before final integration.
