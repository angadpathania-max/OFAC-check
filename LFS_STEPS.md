# Get sdn_advanced.xml pushed with Git LFS

Your `git status` shows `.gitattributes` staged and no `sdn_advanced.xml` in the list. Do these steps in order in PowerShell.

---

## Step 1: See how Git stores the path

Run:

```powershell
cd "D:\Personal\Courses\Cursor\OFAC check"
git ls-files "OFAC DB/"
```

Note the **exact** path(s) shown (e.g. `OFAC DB/cons_advanced.xml` or `OFAC DB\sdn_advanced.xml`).  
If **sdn_advanced.xml** appears, copy that exact path for Step 3.

---

## Step 2: Confirm the file exists on disk

```powershell
dir "OFAC DB"
```

You should see `sdn_advanced.xml` (and `cons_advanced.xml`). If `sdn_advanced.xml` is missing, add it to the folder first.

---

## Step 3: If sdn_advanced.xml appeared in Step 1 – remove it from the index

Use the **exact** path from Step 1 (forward or backslash). Examples:

```powershell
git rm --cached "OFAC DB/sdn_advanced.xml"
```

or, if Git showed a backslash path:

```powershell
git rm --cached "OFAC DB\sdn_advanced.xml"
```

If you get "did not match any files", skip to Step 4.

---

## Step 4: Add .gitattributes and the file (so LFS tracks it)

```powershell
git add .gitattributes
git add "OFAC DB/sdn_advanced.xml"
```

If that fails, try:

```powershell
git add "OFAC DB\sdn_advanced.xml"
```

---

## Step 5: Check status

```powershell
git status
git lfs status
```

- In `git status` you should see `OFAC DB/sdn_advanced.xml` (or similar) under “Changes to be committed”.
- In `git lfs status` you should see `sdn_advanced.xml` as an LFS file to be committed.

---

## Step 6: Commit

If this is the first time adding sdn with LFS:

```powershell
git commit -m "Add OFAC XML data (sdn_advanced.xml via LFS)"
```

If you had already committed sdn before (and we removed it in Step 3), replace that commit with an LFS version:

```powershell
git commit --amend -m "Add OFAC XML data (sdn_advanced.xml via LFS)"
```

---

## Step 7: Push

```powershell
git push -u origin main
```

If Git says the push was rejected (e.g. “non-fast-forward”):

```powershell
git push --force-with-lease origin main
```

---

**If `git ls-files "OFAC DB/"` in Step 1 does not list sdn_advanced.xml:**  
Then Git has never had that file. Do only Steps 2, 4, 5, 6 (first commit option), and 7 – no Step 3 and no `--amend`.
