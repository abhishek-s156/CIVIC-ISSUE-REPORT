"""
smart_helper.py
----------------
This file has a small "AI-like" helper function for our project.

The idea (this is a simple version of what people call "RAG" /
"vector search"):
  When a citizen reports a new issue, we compare its text with
  all the OLD issues already stored in the database, and find
  the ones that look most similar. This helps us warn the user
  "hey, this problem might already be reported!" so we don't
  get duplicate reports for the same pothole again and again.

We are using Python's built-in "difflib" library to compare text.
It is not a big fancy AI model, but it works the same basic way:
  text -> compare -> similarity score -> most similar results first.

If you want, later you can replace this function with a real
LLM/embedding based search (like OpenAI/Gemini embeddings + a
vector database such as FAISS or Chroma). The rest of the project
will keep working the same way, because views.py only calls this
one function: find_similar_issues().
"""

import difflib


def find_similar_issues(new_title, new_description, all_issues, top_n=3):
    """
    Compare a new issue (title + description) with a list of old issues,
    and return the ones that look the most similar.

    Parameters:
        new_title (str): title typed by the user for the new issue
        new_description (str): description typed by the user
        all_issues (list): list of Issue objects already in database
        top_n (int): how many similar issues to return (default 3)

    Returns:
        list of Issue objects, most similar first
    """
    new_text = (new_title + " " + new_description).lower().strip()

    # if there is no old issue yet, there is nothing to compare
    if not all_issues:
        return []

    scored_list = []  # will hold pairs like (issue, score)

    for old_issue in all_issues:
        old_text = (old_issue.title + " " + old_issue.description).lower().strip()

        # this one line does the "AI-like" comparison
        # it returns a score between 0.0 (totally different) and 1.0 (same)
        similarity_score = difflib.SequenceMatcher(None, new_text, old_text).ratio()

        scored_list.append((old_issue, similarity_score))

    # put the highest similarity score first
    scored_list.sort(key=lambda pair: pair[1], reverse=True)

    # we only care about issues that are reasonably similar
    # (score above 0.35 out of 1.0), not just random matches
    similar_issues = [issue for issue, score in scored_list if score > 0.35]

    return similar_issues[:top_n]
