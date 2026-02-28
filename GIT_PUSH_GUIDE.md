# How to Push This Project to Git (Beginner Guide)

> **If you get an error like "File exceeds GitHub's 100 MB limit"** (e.g. for `OFAC DB/sdn_advanced.xml`), use **LARGE_FILES_FIX.md** in this folder. You’ll install Git LFS and re-push; then the push will succeed.

You’ve never used Git before—that’s fine. This guide gets your OFAC project onto GitHub so you can deploy it on Netlify (or just keep a backup in the cloud).

---

## What You’re Doing in Simple Terms

- **Git** = tool that tracks changes in your project (like “save versions” of your files).
- **GitHub** = website where you store that project online (so Netlify can read it and deploy your site).
- **Push** = upload your project from your computer to GitHub.

---

## Step 1: Install Git

1. Go to **https://git-scm.com/download/win**
2. Download **Windows 64-bit** (or whatever it suggests).
3. Run the installer. You can leave most options as default; click **Next** until **Finish**.
4. Close and reopen any terminal (PowerShell or Command Prompt) so Git is available.

To check it worked, open PowerShell and type:

```powershell
git --version
```

You should see something like `git version 2.43.0`.

---

## Step 2: Create a GitHub Account (if you don’t have one)

1. Go to **https://github.com**
2. Click **Sign up** and create a free account (email, password, username).

---

## Step 3: Create a New Repository on GitHub

1. Log in to GitHub.
2. Click the **+** (plus) at the top right → **New repository**.
3. Fill in:
   - **Repository name:** e.g. `ofac-screening` (no spaces).
   - **Description:** optional, e.g. “OFAC business screening tool”.
   - Leave **Public** selected.
   - **Do not** check “Add a README” or “Add .gitignore”—your project already has files.
4. Click **Create repository**.

You’ll see a page that says “Quick setup” and shows a URL like:

`https://github.com/YOUR_USERNAME/ofac-screening.git`

Keep this page open; you’ll use that URL in Step 6.

---

## Step 4: Open Terminal in Your Project Folder

1. Press **Windows key**, type **PowerShell**, and open **Windows PowerShell**.
2. Go to your project folder:

```powershell
cd "D:\Personal\Courses\Cursor\OFAC check"
```

3. Confirm you’re in the right place:

```powershell
dir
```

You should see folders like `OFAC DB`, `netlify`, `public`, and files like `app.py`, `README.md`.

---

## Step 5: Turn This Folder Into a Git Project and Make the First “Save”

Run these commands **one at a time** in PowerShell.

**5a) Tell Git this folder is a project:**

```powershell
git init
```

You’ll see: `Initialized empty Git repository in ...`

**5b) Tell Git who you are (use your real name and the email you used for GitHub):**

```powershell
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

Replace `Your Name` and `your.email@example.com` with your own.

**5c) Add all project files:**

```powershell
git add .
```

The dot (`.`) means “everything in this folder.” Git will ignore files listed in `.gitignore` (e.g. the database and generated JSON).

**5d) Create the first “saved version” (commit):**

```powershell
git commit -m "Initial commit: OFAC screening site"
```

You should see a list of files added and a line like `1 file changed` (or many files). That’s your first version saved locally.

---

## Step 6: Connect Your Project to GitHub and Push

**6a) Add GitHub as the remote (use YOUR repo URL from Step 3):**

```powershell
git remote add origin https://github.com/YOUR_USERNAME/ofac-screening.git
```

Replace `YOUR_USERNAME` with your GitHub username and `ofac-screening` with your repo name if you chose something else.

**6b) Rename the branch to `main` (GitHub’s default):**

```powershell
git branch -M main
```

**6c) Push (upload) to GitHub:**

```powershell
git push -u origin main
```

- GitHub will ask you to **log in**. Use your GitHub username and either:
  - Your **password** (if you have one), or  
  - A **Personal Access Token** (if GitHub says “password not supported”).
- To create a token: GitHub → your profile picture → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token**. Give it a name, check **repo**, generate, then copy the token and paste it when Git asks for a password.

After a few seconds you should see something like:

`Branch 'main' set up to track remote branch 'main' from 'origin'.`

**6d) Check on GitHub:**

Open your repository in the browser (e.g. `https://github.com/YOUR_USERNAME/ofac-screening`). You should see all your project files there.

---

## When You Change Something (e.g. New OFAC XMLs)

After you update files (e.g. put new XMLs in `OFAC DB`), run these three from your project folder:

```powershell
cd "D:\Personal\Courses\Cursor\OFAC check"

git add .
git commit -m "Updated OFAC list for January 2026"
git push
```

That’s it. Your changes are on GitHub, and Netlify will rebuild your site if it’s connected to this repo.

---

## Quick Reference

| What you want to do        | Command |
|---------------------------|--------|
| Go to project folder      | `cd "D:\Personal\Courses\Cursor\OFAC check"` |
| See status of files       | `git status` |
| Add all changes            | `git add .` |
| Save a version (commit)    | `git commit -m "Short description"` |
| Upload to GitHub (push)   | `git push` |

If anything errors, read the message—it often says exactly what to fix (e.g. wrong password, wrong URL, or run `git add` before `git commit`).
