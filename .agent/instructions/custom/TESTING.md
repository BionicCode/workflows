---
Version: 1
Created: 2026-10-27T21:11:00+00:00
Updated: 2026-10-27T21:11:00+00:00
Author: BionicCode
---
<!-- doc-metadata-presentation:start -->
<details>
<summary>Change History</summary>


</details>

---

<br>
<br>
<!-- doc-metadata-presentation:end -->

# Workflows testing companion

Tool-specific tests and fixtures live below `.github/scripts/`. Follow each tool's
existing unittest, PowerShell and fixture conventions and documented runtime dependencies.

For agent-package maintenance, run this acceptance command from repository root:

```powershell
python -B -m unittest discover -s .github/scripts/agent-package/tests -p "test_*.py"
```

Missing required dependencies fail this gate; do not silently skip required cases.
Actual installation checks are read-only; mutating tests use disposable environments.
Static tests do not establish native-client compatibility.
