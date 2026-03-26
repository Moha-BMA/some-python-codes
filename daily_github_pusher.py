from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = REPO_ROOT / "projects_manifest.json"
README_PATH = REPO_ROOT / "README.md"
BASE_TRACKED_FILES = [
    ".gitignore",
    "README.md",
    "projects_manifest.json",
    "daily_github_pusher.py",
    "run_daily_publish.ps1",
]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def load_manifest() -> list[dict[str, object]]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def is_project_tracked(project_path: str) -> bool:
    result = run_git("ls-files", "--", project_path, check=False)
    return bool(result.stdout.strip())


def get_published_projects(manifest: list[dict[str, object]]) -> list[dict[str, object]]:
    return [project for project in manifest if is_project_tracked(str(project["path"]))]


def get_next_project(manifest: list[dict[str, object]]) -> dict[str, object] | None:
    for project in manifest:
        if not is_project_tracked(str(project["path"])):
            return project
    return None


def build_readme(
    manifest: list[dict[str, object]],
    published_paths: set[str],
) -> str:
    lines: list[str] = [
        "# Some Python Codes",
        "",
        "A growing collection of small Python projects. This repository is published gradually,",
        "with one project added per day by the automation scripts in this repo.",
        "",
        "## Publishing Roadmap",
        "",
        "| Order | Project | Folder | Main file | Status |",
        "| --- | --- | --- | --- | --- |",
    ]

    first_unpublished_path = next(
        (str(project["path"]) for project in manifest if str(project["path"]) not in published_paths),
        None,
    )

    for index, project in enumerate(manifest, start=1):
        project_path = str(project["path"])
        if project_path in published_paths:
            status = "Published"
        elif project_path == first_unpublished_path:
            status = "Next in queue"
        else:
            status = "Queued"

        lines.append(
            f"| {index} | {project['title']} | `{project_path}` | "
            f"`{project_path}/{project['main_file']}` | {status} |"
        )

    lines.extend(
        [
            "",
            "## Published Projects",
            "",
        ]
    )

    published_projects = [project for project in manifest if str(project["path"]) in published_paths]
    if not published_projects:
        lines.extend(
            [
                "No project has been published yet. The next run of the automation will add the",
                "first project in the roadmap.",
                "",
            ]
        )
    else:
        for index, project in enumerate(published_projects, start=1):
            project_path = str(project["path"])
            requirements = project.get("requirements", [])
            details = project.get("details", [])

            lines.extend(
                [
                    f"### {index}. {project['title']}",
                    "",
                    f"- Folder: `{project_path}`",
                    f"- Main file: `{project_path}/{project['main_file']}`",
                    f"- Summary: {project['summary']}",
                    "- Highlights:",
                ]
            )

            for detail in details:
                lines.append(f"  - {detail}")

            if requirements:
                lines.append("- Requirements:")
                for requirement in requirements:
                    lines.append(f"  - {requirement}")

            lines.append("")

    lines.extend(
        [
            "## Automation",
            "",
            "- `daily_github_pusher.py` publishes the next unpublished project, regenerates this",
            "  README, commits the changes, and pushes them to `origin/main`.",
            "- `run_daily_publish.ps1` runs the publisher and stores a log file in",
            "  `.publish_logs/`.",
            "- A Windows scheduled task can be registered once so `run_daily_publish.ps1` runs",
            "  automatically every day.",
            "",
            "## Manual Commands",
            "",
            "```powershell",
            "python .\\daily_github_pusher.py --dry-run",
            "python .\\daily_github_pusher.py --refresh-readme-only",
            ".\\run_daily_publish.ps1",
            "```",
            "",
            "The publish step uses your local git credentials, so the repository must exist on",
            "GitHub and your machine must already be able to push to `origin`.",
        ]
    )

    return "\n".join(lines).strip() + "\n"


def write_readme(content: str) -> bool:
    current = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
    if current == content:
        return False

    README_PATH.write_text(content, encoding="utf-8")
    return True


def would_update_readme(content: str) -> bool:
    current = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
    return current != content


def ensure_project_exists(project: dict[str, object]) -> None:
    project_dir = REPO_ROOT / str(project["path"])
    if not project_dir.exists():
        raise FileNotFoundError(f"Project folder does not exist: {project_dir}")


def stage_changes(next_project: dict[str, object] | None) -> None:
    paths_to_stage = [*BASE_TRACKED_FILES]
    if next_project is not None:
        paths_to_stage.append(str(next_project["path"]))
    run_git("add", "--", *paths_to_stage)


def has_staged_changes() -> bool:
    result = run_git("diff", "--cached", "--quiet", check=False)
    return result.returncode != 0


def get_last_publish_date() -> date | None:
    result = run_git(
        "log",
        "--date=short",
        "--format=%ad",
        "--grep=^feat: publish ",
        "-n",
        "1",
        check=False,
    )
    output = result.stdout.strip()
    if not output:
        return None
    return date.fromisoformat(output.splitlines()[0])


def refresh_readme_only(dry_run: bool) -> int:
    manifest = load_manifest()
    published_paths = {str(project["path"]) for project in get_published_projects(manifest)}
    readme_content = build_readme(manifest, published_paths)

    if dry_run:
        print(f"README would be updated: {'yes' if would_update_readme(readme_content) else 'no'}")
        return 0

    changed = write_readme(readme_content)
    print(f"README updated: {'yes' if changed else 'no'}")
    return 0


def publish_next_project(skip_push: bool, dry_run: bool) -> int:
    manifest = load_manifest()
    last_publish_date = get_last_publish_date()

    if last_publish_date == date.today():
        print(f"A project was already published on {last_publish_date.isoformat()}.")
        print("Skipping this run to keep the one-project-per-day schedule.")
        return 0

    next_project = get_next_project(manifest)
    published_paths = {str(project["path"]) for project in get_published_projects(manifest)}

    if next_project is not None:
        ensure_project_exists(next_project)
        planned_published_paths = published_paths | {str(next_project["path"])}
    else:
        planned_published_paths = published_paths

    readme_content = build_readme(manifest, planned_published_paths)

    if dry_run:
        if next_project is None:
            print("All listed projects are already published.")
        else:
            print(f"Next project to publish: {next_project['title']}")
        print(f"README would be updated: {'yes' if would_update_readme(readme_content) else 'no'}")
        return 0

    write_readme(readme_content)
    stage_changes(next_project)
    if not has_staged_changes():
        print("Nothing new to commit.")
        return 0

    if next_project is None:
        commit_message = "docs: refresh repository catalog"
        print("No unpublished projects remain. Committing README refresh only.")
    else:
        commit_message = f"feat: publish {next_project['title']}"
        print(f"Publishing project: {next_project['title']}")

    commit_result = run_git("commit", "-m", commit_message)
    if commit_result.stdout.strip():
        print(commit_result.stdout.strip())

    if skip_push:
        print("Push skipped because --skip-push was used.")
        return 0

    push_result = run_git("push", "-u", "origin", "main", check=False)
    if push_result.returncode != 0:
        error_text = push_result.stderr.strip() or push_result.stdout.strip() or "git push failed"
        print(error_text, file=sys.stderr)
        return push_result.returncode

    success_text = push_result.stderr.strip() or push_result.stdout.strip()
    if success_text:
        print(success_text)
    print("Push completed successfully.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish one Python project per run, update the README, and push to GitHub."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which project would be published next without committing anything.",
    )
    parser.add_argument(
        "--skip-push",
        action="store_true",
        help="Commit locally but do not push to GitHub.",
    )
    parser.add_argument(
        "--refresh-readme-only",
        action="store_true",
        help="Regenerate README.md from the projects that are already tracked in git.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.refresh_readme_only:
            return refresh_readme_only(dry_run=args.dry_run)
        return publish_next_project(skip_push=args.skip_push, dry_run=args.dry_run)
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.strip() if error.stderr else ""
        stdout = error.stdout.strip() if error.stdout else ""
        message = stderr or stdout or str(error)
        print(message, file=sys.stderr)
        return error.returncode or 1
    except Exception as error:  # pragma: no cover
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
