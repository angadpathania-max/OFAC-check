# Fix: "sdn_advanced.xml exceeds 100 MB" on push

The file was committed as a normal file instead of via Git LFS. Fix it by re-adding it with LFS and amending the last commit. Run these in **PowerShell** in your project folder.

---

## Step 1: Go to project folder

```powershell
cd "D:\Personal\Courses\Cursor\OFAC check"
```

---

## Step 2: Make sure Git LFS is active in this repo

```powershell
git lfs install
```

You should see: `Updated Git hooks.`

---

## Step 3: Remove the big file from the index (file stays on disk)

```powershell
git rm --cached "OFAC DB/sdn_advanced.xml"
```

You should see: `rm 'OFAC DB/sdn_advanced.xml'`

---

## Step 4: Add .gitattributes and the file again (LFS will track it this time)

```powershell
git add .gitattributes
git add "OFAC DB/sdn_advanced.xml"
```

Check that LFS is handling it:

```powershell
git status
```

You should see something like: **`OFAC DB/sdn_advanced.xml`** and possibly **"Git LFS"** in the output. If you run:

```powershell
git lfs status
```

it should list `sdn_advanced.xml` as tracked by LFS.

---

## Step 5: Amend the last commit so it uses the LFS version

```powershell
git commit --amend -m "Add OFAC XML data (sdn_advanced.xml via LFS)"
```

---

## Step 6: Push to GitHub

```powershell
git push -u origin main
```

If you get a message that the remote has different history (e.g. "rejected" or "non-fast-forward"), use:

```powershell
git push --force-with-lease origin main
```

The first push can take several minutes while the 114 MB file is uploaded via LFS.
