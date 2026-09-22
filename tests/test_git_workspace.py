from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from hermes_jev.remote.git_workspace import GitWorkspaceManager


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=True)
    return proc.stdout.strip()


class GitWorkspaceTests(unittest.TestCase):
    def test_exact_head_dirty_overlay_and_result_ref_without_branch_move(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            root.mkdir()
            git(root, "init", "-b", "main")
            git(root, "config", "user.email", "test@example.com")
            git(root, "config", "user.name", "Test")
            (root / "tracked.txt").write_text("base\n")
            git(root, "add", "tracked.txt")
            git(root, "commit", "-m", "base")
            base = git(root, "rev-parse", "HEAD")
            (root / "tracked.txt").write_text("dirty\n")
            (root / "new.txt").write_text("untracked\n")

            mgr = GitWorkspaceManager()
            snap = mgr.capture(root)
            self.assertEqual(snap.head, base)
            self.assertIn("new.txt", snap.untracked)

            wt = Path(td) / "run-worktree"
            mgr.create_run_worktree(root, wt, snap)
            self.assertEqual((wt / "tracked.txt").read_text(), "dirty\n")
            self.assertEqual((wt / "new.txt").read_text(), "untracked\n")
            (wt / "worker.txt").write_text("remote result\n")

            branch_before = git(root, "branch", "--show-current")
            head_before = git(root, "rev-parse", "HEAD")
            result = mgr.publish_result_ref(root, wt, task_id="t-42", run_id=7)
            self.assertEqual(git(root, "branch", "--show-current"), branch_before)
            self.assertEqual(git(root, "rev-parse", "HEAD"), head_before)
            self.assertEqual(git(root, "rev-parse", result.ref), result.commit)
            self.assertNotEqual(result.commit, base)
            mgr.remove_run_worktree(root, wt)


if __name__ == "__main__":
    unittest.main()
