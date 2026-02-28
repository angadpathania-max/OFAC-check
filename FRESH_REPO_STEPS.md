# Fresh repo: both XMLs with LFS from the start

This removes all Git history and makes one new first commit with both `cons_advanced.xml` and `sdn_advanced.xml` tracked by LFS. Run in PowerShell.

---

## Step 1: Go to project folder

```powershell
cd "D:\Personal\Courses\Cursor\OFAC check"
```

---

## Step 2: Remove the old Git repo

```powershell
Remove-Item -Recurse -Force .git
```

Your files stay; only the `.git` folder (all history and config) is deleted.

---

## Step 3: Start a new repo and set up LFS

```powershell
git init
git lfs install
git lfs track "OFAC DB/*.xml"
```

---

## Step 4: Add everything and check LFS

```powershell
git add .gitattributes
git add .
git status
git lfs status
```

In `git lfs status` you should see both `sdn_advanced.xml` and `cons_advanced.xml` as LFS files to be committed.

---

## Step 5: First commit

```powershell
git branch -M main
git commit -m "Initial commit: OFAC screening site"
```

---

## Step 6: Connect to GitHub and push

Use your real repo URL (replace YOUR_USERNAME and REPO_NAME):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

If GitHub already has commits from before, push once with force:

```powershell
git push --force origin main
```

Then set upstream:

```powershell
git push -u origin main
```

---

## Summary

| Step | What it does |
|------|----------------|
| Remove .git | Deletes all old history |
| git init | New repo |
| git lfs track "OFAC DB/*.xml" | Both XMLs use LFS |
| git add . → commit | Single clean first commit |
| git push | Upload to GitHub |

After this you have one commit and both XMLs stored via LFS.
