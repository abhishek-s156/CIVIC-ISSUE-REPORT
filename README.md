# Civic Issue Reporter 🏙️

A simple **Crowdsourced Civic Issue Reporting and Resolution System**
built with Django. Citizens can report local problems (potholes,
garbage, broken street lights, etc.), upvote issues that matter to
them, comment, and track the status until it is resolved.

This project is written in a **beginner-friendly style**:
- Simple, clear file and folder names
- Simple variable and function names
- Lots of comments explaining what each part does

---

## ✨ Features

- 📝 Report a civic issue with title, description, category, location, and photo
- 👍 Upvote issues to show they matter
- 💬 Comment on issues to give updates
- 📊 Track status: Pending → In Progress → Resolved
- 🔍 Filter issues by category or status
- 🙋 "My Issues" page to see what you personally reported
- 🛠️ Staff/admin can update issue status
- 🤖 **Simple AI helper** (`smart_helper.py`): before you submit a new
  issue, the app compares your text with existing issues (a very
  basic version of a "vector search" / RAG idea) and warns you if
  a similar issue was already reported — helps avoid duplicates!

> 💡 The AI helper currently uses Python's built-in `difflib` library
> (no API key needed, works fully offline). If you want to upgrade it
> to a real LLM / embeddings + vector database (like OpenAI or Gemini
> embeddings with FAISS/Chroma), you only need to change the
> `find_similar_issues()` function inside `issue_app/smart_helper.py`.
> The rest of the app will keep working exactly the same way.

---

## 📁 Project Structure (simple names, easy to understand)

```
civic_issue_project/            <- main project folder
│
├── civic_issue_project/        <- Django settings folder
│   ├── settings.py              (project configuration)
│   ├── urls.py                  (main URL routing)
│   └── ...
│
├── issue_app/                   <- our main app (all the real logic)
│   ├── models.py                (database tables: Issue, Comment)
│   ├── views.py                 (page logic / what happens on each page)
│   ├── forms.py                 (input forms: report issue, sign up, comment)
│   ├── urls.py                  (page addresses inside our app)
│   ├── admin.py                 (admin panel setup)
│   ├── smart_helper.py          (simple AI helper - duplicate issue checker)
│   ├── templates/issue_app/     (all HTML pages)
│   │   ├── base.html            (common layout: navbar, footer)
│   │   ├── home.html            (list of all issues)
│   │   ├── report_issue.html    (form to report new issue)
│   │   ├── issue_detail.html    (one issue's full details + comments)
│   │   ├── my_issues.html       (issues reported by logged-in user)
│   │   ├── login.html
│   │   └── signup.html
│   └── static/issue_app/
│       └── style.css            (simple CSS styling)
│
├── media/                       <- uploaded issue photos go here
├── manage.py                    <- used to run Django commands
├── requirements.txt             <- list of Python packages needed
└── README.md                    <- this file
```

---

## 🚀 How to Run This Project (Step by Step)

### 1. Install Python packages
Open a terminal inside the `civic_issue_project` folder and run:

```bash
pip install -r requirements.txt
```

### 2. Create the database tables

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create an admin (superuser) account
This account can log into `/admin/` and update issue status.

```bash
python manage.py createsuperuser
```
Follow the prompts (username, email, password).

### 4. Run the website

```bash
python manage.py runserver
```

Now open your browser and go to:
```
http://127.0.0.1:8000/
```

### 5. Try it out
1. Click **Sign Up** and create a normal user account.
2. Click **Report Issue** and submit a civic problem (try adding a photo too).
3. Try submitting a very similar issue again — the simple AI helper
   should warn you that a similar issue already exists!
4. Log in as your **superuser** (from step 3) — on any issue page you
   will now see **Staff Controls** to change the status.
5. Explore filtering issues by category/status on the Home page.

---

## 🧠 About the "AI" Feature (Beginner Explanation)

Real-world crowdsourced platforms use AI to detect duplicate reports
so the same pothole doesn't get reported 50 times. We built a very
simple version of that idea:

1. When you type a new issue's title + description...
2. `smart_helper.py` compares your text with every existing issue's text.
3. It calculates a "similarity score" (0.0 = totally different, 1.0 = same).
4. If the score is high enough, we show you those issues as a warning.

This is the same basic *concept* used in real AI-powered RAG (Retrieval
Augmented Generation) and vector database search — just using simple
text comparison instead of AI embeddings. It's a great first step
before plugging in a real LLM API!

---

## 🛠️ Tech Used

- **Backend:** Django (Python web framework)
- **Database:** SQLite (comes free with Django, no setup needed)
- **Frontend:** HTML + Bootstrap (for simple, clean styling)
- **"AI" Feature:** Python `difflib` (can be upgraded to real LLM/embeddings later)

---

## 📌 Ideas to Extend This Project (for practice)

- Add real LLM-based duplicate detection using OpenAI/Gemini embeddings + a vector DB (FAISS, Chroma, Pinecone)
- Add an LLM chatbot that helps citizens describe their issue better
- Add email/SMS notifications when issue status changes
- Add a map view to show issues by location
- Add issue priority scoring based on number of upvotes
