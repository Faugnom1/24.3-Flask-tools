from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

# Use the Flask Debug Toolbar for debugging
debug = DebugToolbarExtension(app)

@app.route('/')
def show_start_page():
    """Render the start page with survey title and instructions."""
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/start', methods=['POST'])
def start_survey():
    """Initialize the session for the survey."""
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Render the question page for the specified question ID."""
    responses = session.get('responses')
    
    # Check if the question ID is valid
    if question_id == len(responses):
        if question_id < len(satisfaction_survey.questions):
            question = satisfaction_survey.questions[question_id]
            return render_template('question.html', question=question, question_id=question_id)
        else:
            return redirect('/thank-you')
    else:
        flash("Invalid question access. Please answer questions in order.", "error")
        return redirect(f'/questions/{len(responses)}')

@app.route('/answer', methods=['POST'])
def handle_answer():
    """Handle user's answer and redirect to the next question or thank you page."""
    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    
    # Check if all questions are answered
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank-you')
def thank_you():
    """Render the thank you page."""
    responses = session.get('responses')
    if len(responses) != len(satisfaction_survey.questions):
        return redirect('/')
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run()
