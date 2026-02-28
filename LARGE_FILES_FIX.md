# Fix: "File exceeds GitHub's 100 MB limit"

Your OFAC XML files are larger than 100 MB. Use **Git LFS** (Large File Storage) so GitHub accepts them.

---

## Step 1: Install Git LFS

1. Go to **https://git-lfs.com**
2. Click **Download** and get the **Windows** installer.
3. Run it and finish the setup.
4. **Close and reopen PowerShell** so the `git lfs` command is available.

Check it worked:

```powershell
git lfs version
```

You should see a version number.

---

## Step 2: Open Your Project in PowerShell

```powershell
cd "D:\Personal\Courses\Cursor\OFAC check"
```

---

## Step 3: Enable LFS and Track the Large XMLs

Run these **one at a time**:

```powershell
git lfs install
```

```powershell
git lfs track "OFAC DB/*.xml"
```

That creates (or updates) `.gitattributes` so all XML files in `OFAC DB` use LFS.

---

## Step 4: Add the Large XML(s) with LFS

**If `git ls-files "OFAC DB/"` only lists cons_advanced.xml** then sdn_advanced.xml was never in Git (too large). You only add it now with LFS; no need to remove anything for sdn.

**4a) Add the LFS config and the large XML:**

```powershell
git add .gitattributes
git add "OFAC DB/sdn_advanced.xml"
```

**4b) Optional – cons_advanced.xml:**  
If **cons_advanced.xml** is over 100 MB, switch it to LFS too (otherwise GitHub will reject the push):

```powershell
git rm --cached "OFAC DB/cons_advanced.xml"
git add "OFAC DB/cons_advanced.xml"
```

If cons_advanced.xml is under 100 MB, you can leave it as is (or do the above to keep both on LFS).

**4c) Commit:**

If you only added sdn (and didn’t remove cons):

```powershell
git commit -m "Add OFAC XML data (sdn_advanced.xml via LFS)"
```

If you also re-added cons_advanced.xml, amend the last commit so both use LFS:

```powershell
git commit --amend -m "Initial commit: OFAC screening site"
```

---

## Step 5: Push to GitHub

```powershell
git push -u origin main
```

Git will upload the XMLs via LFS. The first push can take a few minutes because of the file size.

---

## Summary

| What you did |
|--------------|
| Installed Git LFS |
| Told Git to store `OFAC DB/*.xml` with LFS |
| Removed the big file from the commit and re-added it with LFS |
| Amended the commit and pushed |

From now on, any changes to those XML files will use LFS automatically. Netlify supports Git LFS, so your build will still have the XMLs when it runs.
