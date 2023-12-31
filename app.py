from flask import Flask, render_template, request
from datetime import datetime

import os
import random

class EvaluationCriterion:
  def __init__(self, title, description):
    self.title = title
    self.description = description

class Assignment:
    def __init__(self, title, description, deadline, evaluation_criteria, anonymity):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.evaluation_criteria = [EvaluationCriterion(criteria['title'], criteria['description']) for criteria in evaluation_criteria]
        self.submissions = []
        self.anonymity = anonymity

    def upload_submission(self, student, file):
        submission = {
            'student': student,
            'file': file,
            'feedback': [],
            'grade': None,
            'reviewer': None
        }
        self.submissions.append(submission)

    def assign_peer_reviews(self):
        if len(self.submissions) < 2:
            print("Not enough submissions to assign peer reviews.")
            return

        for submission in self.submissions:
            reviewer = random.choice([s['student'] for s in self.submissions if s != submission])
            submission['reviewer'] = reviewer

    def provide_peer_feedback(self, evaluation_criteria):
        for submission in self.submissions:
            if self.anonymity == True:
                student = "Anonymous"
                reviewer = "Anonymous"
            else:
                student = submission['student']
                reviewer = submission['reviewer']
            print(f"{reviewer}, please provide feedback and grade {student}'s work based on the following criteria:")
            for criterion in evaluation_criteria:
                print(f"- {criterion['title']}")
            feedback = {}
            for criterion in evaluation_criteria:
                feedback[criterion['title']] = int(input(f"{reviewer}, please provide a score for {student}'s work on {criterion['title']}: "))
            grade = sum(feedback.values())
            submission['feedback'].append({'reviewer': reviewer, 'feedback': feedback, 'grade': grade})

    def _save_file(self, file_path):
        if not os.path.exists('submissions'):
            os.makedirs('submissions')
        file_name = os.path.basename(file_path)
        new_file_path = os.path.join('submissions', file_name)
        with open(new_file_path, 'wb') as f:
            with open(file_path, 'rb') as g:
                f.write(g.read())
        return new_file_path

    def display_details(self):
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Deadline: {self.deadline}")
        print("Evaluation Criteria:")
        for criteria in self.evaluation_criteria:
            print(f"- {criteria.title}: {criteria.description}")

'''
# Example usage:

# Create evaluation criteria
'''
evaluation_criteria = [
    {"title": "Originality", "description": "The extent to which the work is original and creative."},
    {"title": "Clarity", "description": "The clarity and coherence of the work."},
    {"title": "Grammar and Spelling", "description": "The correctness of grammar, spelling, and punctuation."},
    {"title": "Use of Sources", "description": "The appropriate use of sources and references."}
]
'''
# Create assignment
assignment = Assignment(
    title='Research Paper',
    description='Write a 10-page research paper on a topic of your choice.',
    deadline='2023-05-01',
    evaluation_criteria=evaluation_criteria,
    anonymity=True
)

assignment.display_details() # display assignment details

# Upload submissions
assignment.upload_submission("John Doe", "pdf1")
assignment.upload_submission("John Doe2", "pdf2")

# Assign peer reviews
assignment.assign_peer_reviews()
assignment.provide_peer_feedback(evaluation_criteria)

for submission in assignment.submissions:
    #print(f"{submission['student']} will review {submission['reviewer']}'s work.")
    print(f"{submission['student']}'s work received the following feedback:")
    for review in submission['feedback']:
        if review['reviewer'] == "Anonymous":
            print(f"- {review['reviewer']}: {review['feedback']} (Grade: {review['grade']})")
        else:
            print(f"- {review['reviewer']}: {review['feedback']} (Grade: {review['grade']})")
'''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        # Get the input data
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']
        deadline = datetime.strptime(deadline, '%Y-%m-%d')

        # Convert evaluation criteria list to dictionaries
        evaluation_criteria = [
            {"title": test, "description": test}
            for test in request.form.getlist('criteria[]')
            ]

        print(evaluation_criteria)

        anonymity = request.form.get('anonymity')

        # Create Assignment object here using the input data
        assignment = Assignment(title, description, deadline, evaluation_criteria, anonymity)
        assignment.display_details()

        # Save the assignment object to a file or database here

        return render_template('display_assignment.html', assignment=assignment)

    return render_template('create_assignment.html')

if __name__ == '__main__':
    app.run(debug=True)
