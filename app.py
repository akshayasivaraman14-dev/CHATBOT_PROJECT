from flask import Flask, render_template, request, jsonify, redirect, url_for
from ai.gemini_engine import ask_gemini
from ai.ollama_engine import ask_ollama
from ai.faq_engine import search_incidents
import sqlite3

app = Flask(__name__)


# -----------------------------
# DATABASE FUNCTIONS
# -----------------------------

def save_chat(question, answer):

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute(
        """
        INSERT INTO chat_history
        (question, answer)
        VALUES (?,?)
        """,
        (question, answer)
    )

    conn.commit()
    conn.close()


# -----------------------------
# PAGE ROUTES
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin-login", methods=["POST"])
def admin_login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin123":
        return redirect("/admin")

    return """
    <h2>❌ Invalid Username or Password</h2>
    <br>
    <a href='/login'>Try Again</a>
    """


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/ticket")
def ticket():
    return render_template("ticket.html")


# ----------------------------#
# CHAT API
# -----------------------------

@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        question = data.get("message", "").strip()

        if not question:
            return jsonify({
                "reply": "Please enter a message."
            })

        reply = None

        # STEP 1 - Search Company Incident CSV
        csv_answer = search_incidents(question)

        if csv_answer:

            reply = (
                "📁 Found in company incidents:\n\n"
                + csv_answer
            )

        # STEP 2 - Gemini
        if not reply:

            print("Trying Gemini...")

            reply = ask_gemini(question)

        # STEP 3 - Ollama Backup
        if not reply:

            print("Gemini unavailable. Trying Ollama...")

            reply = ask_ollama(question)

        # STEP 4 - Final Fallback
        if not reply:

            reply = """
I couldn't find an answer.

Please raise a support ticket.
"""

        save_chat(question, reply)

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "reply": f"Server Error: {str(e)}"
        })

# -----------------------------
# RAISE TICKET
# -----------------------------

@app.route("/raise-ticket", methods=["POST"])
def raise_ticket():

    try:

        name = request.form.get("name")
        department = request.form.get("department")
        subject = request.form.get("subject")
        description = request.form.get("description")

        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            subject TEXT,
            description TEXT,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        INSERT INTO tickets
        (name, department, subject, description)
        VALUES (?,?,?,?)
        """,
        (
            name,
            department,
            subject,
            description
        ))

        conn.commit()
        conn.close()

        return """
        <h2>✅ Ticket Raised Successfully</h2>
        <a href='/chat'>Back To Chat</a>
        """

    except Exception as e:

        return f"Error: {e}"


# -----------------------------
# ADMIN STATS
# -----------------------------

@app.route("/stats")
def stats():

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT COUNT(*) FROM chat_history"
        )
        total_chats = cursor.fetchone()[0]

    except:
        total_chats = 0

    try:

        cursor.execute(
            "SELECT COUNT(*) FROM tickets"
        )
        total_tickets = cursor.fetchone()[0]

    except:
        total_tickets = 0

    try:

        cursor.execute(
            "SELECT COUNT(*) FROM tickets WHERE status='Open'"
        )
        open_tickets = cursor.fetchone()[0]

    except:
        open_tickets = 0

    conn.close()

    return jsonify({
        "total_chats": total_chats,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets
    })
@app.route("/tickets")
def get_tickets():

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        id,
        name,
        department,
        subject,
        status,
        created_at
        FROM tickets
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    conn.close()

    return jsonify(tickets)


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )