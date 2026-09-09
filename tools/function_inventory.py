"""Generate a source-linked callable and test-assertion inventory for the final report."""

from __future__ import annotations

import ast

from su2zx.paths import project_path


def main() -> str:
    root = ROOT
    lines = [
        "# Python function and test inventory",
        "",
        "Generated from the shipped source AST. Calls are syntactic expressions,",
        "not a resolved runtime call graph. Full code is included at each linked path.",
        "Test assertions describe checks; execution outcomes are in the JUnit/log files.",
        "",
    ]
    for directory in DIRECTORIES:
        for path in sorted((root / directory).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            relative = path.relative_to(root).as_posix()
            tree = ast.parse(path.read_text())
            lines.extend([f"## [{relative}](../{relative})", ""])
            doc = ast.get_docstring(tree)
            if doc:
                lines.extend([doc, ""])
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                signature = f"{node.name}({ast.unparse(node.args)})"
                lines.extend([f"### `{signature}` — line {node.lineno}", ""])
                doc = ast.get_docstring(node)
                if doc:
                    lines.extend([doc, ""])
                calls = sorted(
                    {
                        ast.unparse(item.func)
                        for item in ast.walk(node)
                        if isinstance(item, ast.Call)
                    }
                )
                lines.extend(
                    [
                        "Direct call expressions: "
                        + (", ".join(f"`{c}`" for c in calls) or "none"),
                        "",
                    ]
                )
                if directory in TEST_DIRECTORIES:
                    for decorator in node.decorator_list:
                        lines.extend([f"Decorator: `{ast.unparse(decorator)}`", ""])
                    checks = [
                        ast.unparse(item)
                        for item in ast.walk(node)
                        if isinstance(item, ast.Assert)
                        or (
                            isinstance(item, ast.Call)
                            and any(
                                word in ast.unparse(item.func) for word in ("assert", "raises")
                            )
                        )
                    ]
                    if checks:
                        lines.extend(["```python", *checks, "```", ""])
    if OUTPUT == "docs/CODE_FUNCTION_INVENTORY.md":
        project_path("docs/CODE_FUNCTION_INVENTORY.md").write_text("\n".join(lines))
    return "\n".join(lines)


# Keep configuration below main: the legacy inventory includes this tool's AST,
# including main's starting line and direct-call expressions.
ROOT = project_path(".")
DIRECTORIES = ("src", "tests", "tools")
TEST_DIRECTORIES = ("tests",)
OUTPUT = "docs/CODE_FUNCTION_INVENTORY.md"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=".", help="Root for source-relative links")
    parser.add_argument("--roots", nargs="+", default=DIRECTORIES)
    parser.add_argument("--output", default=OUTPUT, help="Output path, relative to repository cwd")
    arguments = parser.parse_args()
    ROOT = project_path(arguments.base)
    DIRECTORIES = tuple(dict.fromkeys(arguments.roots))
    for directory in DIRECTORIES:
        selected = (ROOT / directory).resolve()
        if not selected.is_relative_to(ROOT):
            parser.error(f"source root escapes selected base: {directory}")
        if not selected.is_dir():
            parser.error(f"source root is not a directory: {directory}")
        for candidate in selected.rglob("*"):
            if candidate.is_symlink():
                parser.error(f"symlink source is not allowed: {candidate.relative_to(ROOT)}")
    OUTPUT = arguments.output
    destination = project_path(OUTPUT)
    if destination == project_path("docs/CODE_FUNCTION_INVENTORY.md") and (
        ROOT != project_path(".") or DIRECTORIES != ("src", "tests", "tools")
    ):
        parser.error("legacy output is reserved for the original roots; specify --output")
    TEST_DIRECTORIES = tuple(
        directory for directory in DIRECTORIES if (ROOT / directory).name in {"tests", "gates"}
    )
    text = main()
    if OUTPUT != "docs/CODE_FUNCTION_INVENTORY.md":
        destination.write_text(text)
