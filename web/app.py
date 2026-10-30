"""FastAPI application for Haunted Repo."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from haunted.analyzer import analyze_repository
from haunted.flakes import detect_flaky_tests
from haunted.deps import audit_dependencies
from haunted.planner import generate_plan

app = FastAPI(
    title="Haunted Repo",
    description="Find and exorcise dead code, flaky tests, and cursed dependencies",
    version="0.1.0",
)

web_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=web_dir / "static"), name="static")
templates = Jinja2Templates(directory=web_dir / "templates")


@app.get("/", response_class=HTMLResponse)
async def graveyard(request: Request):
    """Render the graveyard UI with sample data."""
    sample_zombies = [
        {"name": "old_utils.py", "lines": 142, "reason": "No imports found"},
        {"name": "legacy_api.py", "lines": 89, "reason": "Zero test coverage"},
    ]
    sample_poltergeists = [
        {"name": "test_flaky_math", "flips": 3, "runs": 5},
    ]
    sample_cursed = [
        {"name": "requests", "version": "2.20.0", "issue": "CVE-2023-32681"},
    ]

    return templates.TemplateResponse(
        request,
        "graveyard.html",
        {
            "repo_url": "https://github.com/example/demo-repo",
            "zombies": sample_zombies,
            "poltergeists": sample_poltergeists,
            "cursed": sample_cursed,
            "status": "sample",
        },
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "haunted-repo", "version": "0.1.0"}


@app.get("/api/analyze")
async def analyze(repo_url: str):
    """
    Trigger analysis of a repository.

    This is a stub that returns sample data. Full implementation will:
    1. Clone the repository
    2. Run analyzer, flakes, and deps modules
    3. Generate resurrection plan
    """
    sample_path = Path("/tmp/sample")

    analyzer_results = analyze_repository(sample_path)
    flakes_results = detect_flaky_tests(sample_path)
    deps_results = audit_dependencies(sample_path)

    plan = generate_plan(repo_url, analyzer_results, flakes_results, deps_results)

    return {
        "repo_url": repo_url,
        "analyzer": analyzer_results,
        "flakes": flakes_results,
        "deps": deps_results,
        "plan_markdown": plan.to_markdown(),
        "status": "stub",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
