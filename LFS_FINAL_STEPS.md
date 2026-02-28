# Fix LFS – exact steps (path: OFAC DB/sdn_advanced.xml)

The file is in your commit but not in the index. Reset the index to match the commit, then switch the file to LFS and amend.

Run in PowerShell, one at a time:

```powershell
cd "D:\Personal\Courses\Cursor\OFAC check"
```

**1. Reset the index to match the last commit**  
(This puts OFAC DB/sdn_advanced.xml back into the index so we can remove it and re-add with LFS.)

```powershell
git reset HEAD
```

**2. Remove the big file from the index only** (file stays on disk)

```powershell
git rm --cached "OFAC DB/sdn_advanced.xml"
```

**3. Add LFS config and the file again** (LFS will track it)

```powershell
git add .gitattributes
git add "OFAC DB/sdn_advanced.xml"
```

**4. Check LFS**

```powershell
git lfs status
```
You should see `sdn_advanced.xml` listed.

**5. Amend the last commit** (replace the 114 MB file with the LFS pointer)

```powershell
git commit --amend -m "Add OFAC XML data (sdn_advanced.xml via LFS)"
```

**6. Push**

```powershell
git push -u origin main
```

If Git says the push was rejected (e.g. “non-fast-forward”):

```powershell
git push --force-with-lease origin main
```

The first push may take a few minutes while the file is uploaded via LFS.
