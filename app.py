from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "secret_key_for_sessions"  # Needed for sessions

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        # If difficulty is not set, set it from form
        if "difficulty" not in session:
            difficulty = request.form.get("difficulty")
            if difficulty == "easy":
                session["max_attempts"] = 5
            elif difficulty == "hard":
                session["max_attempts"] = 3
            else:
                message = "❌ Invalid difficulty selected."
                return render_template("index.html", message=message)

            session["secret_number"] = random.randint(1, 5)
            session["attempts"] = 0
            session["difficulty"] = difficulty
            message = f"🎮 Difficulty set to {difficulty.title()}! Start guessing."

        elif "guess" in request.form:
            # Get guess and update attempts
            guess = int(request.form.get("guess"))
            secret_number = session["secret_number"]
            attempts = session["attempts"]
            max_attempts = session["max_attempts"]

            if guess < 1 or guess > 5:
                message = "🚫 Guess must be between 1 and 5."
            else:
                session["attempts"] += 1
                if guess < secret_number:
                    message = "📉 Too low!"
                elif guess > secret_number:
                    message = "📈 Too high!"
                else:
                    message = f"🎉 Correct! You guessed it in {attempts + 1} attempts."
                    session.clear()  # Reset game
                    return render_template("index.html", message=message, play_again=True)

                # Check if attempts exhausted
                if session["attempts"] >= max_attempts:
                    message += f" 💀 Game Over! The number was {secret_number}."
                    session.clear()
                    return render_template("index.html", message=message, play_again=True)

    return render_template("index.html", message=message)

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
