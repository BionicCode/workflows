---
Version: 1
Created: 2026-10-13T20:32:55+00:00
Updated: 2026-10-13T20:32:55+00:00
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

Test roots: tool-specific tests below .github/scripts/. Follow each tool's existing unittest and PowerShell fixture conventions and its documented runtime dependencies. There is no .NET solution in this repository. Keep fixtures and test-only helpers with the owning tool tests.

For agent-package maintenance, the required acceptance command from repository root is:

```powershell
python -B -m unittest discover -s .github/scripts/agent-package/tests -p "test_*.py"
```

Missing required test dependencies fail this gate; do not skip required cases. Actual installation checks are read-only; mutations use disposable fixtures. Static Claude checks do not establish native compatibility.
