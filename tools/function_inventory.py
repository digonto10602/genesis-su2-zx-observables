"""Generate a source-linked callable and test-assertion inventory for the final report."""

from __future__ import annotations

import ast

from su2zx.paths import project_path


def main() -> None:
    root = project_path(".")
    lines = [
        "# Python function and test inventory",
        "",
        "Generated from the shipped source AST. Calls are syntactic expressions,",
        "not a resolved runtime call graph. Full code is included at each linked path.",
        "Test assertions describe checks; execution outcomes are in the JUnit/log files.",
        "",
    ]
    for directory in ("src", "tests", "tools"):
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
                if directory == "tests":
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
    project_path("docs/CODE_FUNCTION_INVENTORY.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
