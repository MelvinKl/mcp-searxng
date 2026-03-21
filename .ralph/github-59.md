# GitHub Issue Task: AI removal

Issue Number: 59
Branch: ai/issue-59-ai-removal

## Required Task

Remove beads, Agents.md, opencode.json, etc from the repository. Every artifact that can be attributed to either an LLM tool or beads should be removed from the repository

## Steps

- [x] 1. Remove the `beads/` directory and all its contents from the repository.
  - Acceptance Criteria:
    - The `beads/` directory is completely removed from the filesystem
    - All tracked files within `beads/` are staged for deletion
    - `beads/example.txt` is no longer present
    - `beads/mcp_fsm.bead` is no longer present
    - `beads/mcp_fsm.py` is no longer present
    - `beads/mcp_fsm.txt` is no longer present
    - `beads/simple_fsm.txt` is no longer present

- [x] 2. Remove the `agents.md` file from the repository root.
  - Acceptance Criteria:
    - The `agents.md` file at `/root/git/managed/mcp-searxng/agents.md` is deleted from the filesystem
    - The file is staged for deletion
    - No `agents.md` or `Agents.md` file exists in the repository root

- [x] 3. Remove the `tests/test_beads.py` test file.
   - Acceptance Criteria:
     - The `tests/test_beads.py` file at `/root/git/managed/mcp-searxng/tests/test_beads.py` (11,844 bytes) is deleted from the filesystem
     - The file is staged for deletion
     - No test files reference beads functionality
     - Follows same deletion pattern as step 2 (delete from filesystem, stage for deletion)

- [x] 4. Remove the `.git/opencode` file from the git metadata directory.
   - Acceptance Criteria:
     - The `.git/opencode` file at `/root/git/managed/mcp-searxng/.git/opencode` (40 bytes) is deleted from the filesystem
     - The file is staged for deletion
     - The file is no longer present in `.git/` directory

  - [x] 5. Verify that no other AI-related artifacts remain in the repository.
    - Acceptance Criteria:
      - No files or directories containing "beads", "agent", or "opencode" exist in the repository (excluding .venv)
      - Verify `opencode.json` does not exist in the repository root (confirmed not present)
      - Verify `.git/opencode` file has been removed as confirmed in step 4
      - Search results for these terms return no tracked files
      - No beads-related branches exist locally
      - Search for both lowercase and uppercase variants (e.g., "beads"/"Beads", "agent"/"Agent") based on step 2 learnings
      - Confirm `agents.md` is fully removed as verified in step 2
      - Verify no test files reference beads functionality as confirmed in step 3
      - Check git metadata directories (like `.git/`) for opencode-related files

   - [x] 6. Run `make test` and confirm it succeeds.
     - Acceptance Criteria:
       - `make test` exits successfully with exit code 0
       - All tests pass
       - No errors related to missing beads dependencies or deleted files from steps 1-4
       - Tests do not reference removed beads/ directory contents (beads/example.txt, beads/mcp_fsm.bead, beads/mcp_fsm.py, beads/mcp_fsm.txt, beads/simple_fsm.txt)
       - No test failures related to agents.md removal
       - No test failures related to tests/test_beads.py removal
       - No test failures related to .git/opencode file removal
       - Confirms that all AI-related artifacts (beads, agent, opencode) have been properly removed without breaking test suite
