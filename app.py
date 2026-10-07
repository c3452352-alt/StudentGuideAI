from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import serpapi

load_dotenv()

app = Flask(__name__)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = serpapi.Client(api_key=SERPAPI_KEY)


def get_guidance(guidance):
    """Give simple guidance based on the student's question."""

    text = guidance.lower()

    if "python" in text:
        return (
            "🐍 Python Path: Start with Python basics, problem solving and "
            "DSA. Build 2-3 small projects and then apply for beginner "
            "Python internships and hackathons."
        )

    elif "web" in text or "website" in text:
        return (
            "🌐 Web Development Path: Learn HTML, CSS and JavaScript first. "
            "Then learn a backend technology such as Flask. Build a "
            "portfolio website and 2-3 projects before applying for "
            "internships."
        )

    elif "hackathon" in text:
        return (
            "🏆 Hackathon Path: Start with beginner-friendly hackathons. "
            "Choose a small real-world problem, build a working prototype "
            "and prepare a short demo. Focus on solving a useful problem "
            "rather than making the project unnecessarily complicated."
        )

    elif "internship" in text:
        return (
            "💼 Internship Path: Identify your strongest skill, build "
            "2-3 projects and prepare a simple resume and portfolio. "
            "Start with beginner-friendly internships and apply regularly."
        )

    elif "job" in text:
        return (
            "💻 Job Path: Improve your programming fundamentals, DSA and "
            "communication skills. Build projects and prepare your resume "
            "before applying for entry-level opportunities."
        )

    elif "course" in text or "learn" in text or "learning" in text:
        return (
            "📚 Learning Path: Choose one skill first instead of learning "
            "many technologies at once. Follow a structured course, "
            "practice regularly and build projects to demonstrate your skills."
        )

    else:
        return (
            "🎯 Student Career Path: First identify your goal and current "
            "skills. Then learn the required skills, build small projects "
            "and look for internships, hackathons, jobs and courses that "
            "match your level."
        )


@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    query = ""
    guidance_result = ""

    if request.method == "POST":

        query = request.form.get("query", "").strip()
        guidance = request.form.get("guidance", "").strip()

        # -------------------------
        # AI STUDENT GUIDANCE
        # -------------------------

        if guidance:

            guidance_result = get_guidance(guidance)

            # Also search the web for opportunities related
            # to the student's guidance question.
            search_query = guidance + " students opportunities India"

            try:

                response = client.search({
                    "engine": "google",
                    "q": search_query,
                    "num": 10
                })

                results = response.get("organic_results", [])

            except Exception as e:

                print("Guidance search error:", e)

        # -------------------------
        # NORMAL SEARCH
        # -------------------------

        elif query:

            try:

                response = client.search({
                    "engine": "google",
                    "q": query,
                    "num": 10
                })

                results = response.get("organic_results", [])

            except Exception as e:

                print("Search error:", e)

    return render_template(
        "index.html",
        results=results,
        query=query,
        guidance_result=guidance_result
    )


# -------------------------
# CATEGORY SEARCH
# -------------------------

@app.route("/category/<category>")
def category(category):

    category_queries = {

        "internship":
            "student internships college students India",

        "hackathon":
            "upcoming student hackathons India 2026",

        "jobs":
            "entry level jobs CSE students India",

        "learning":
            "free courses certifications computer science students"

    }

    query = category_queries.get(
        category,
        "student opportunities India"
    )

    results = []
    guidance_result = ""

    try:

        response = client.search({
            "engine": "google",
            "q": query,
            "num": 10
        })

        results = response.get("organic_results", [])

    except Exception as e:

        print("Category search error:", e)

    return render_template(
        "index.html",
        results=results,
        query=query,
        guidance_result=guidance_result
    )


if __name__ == "__main__":
    app.run(debug=True)