import os

class EvaluationCriterion:
  def __init__(self, title, description):
    self.title = title
    self.description = description

class Assignment:
    def __init__(self, title, description, deadline, evaluation_criteria):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.evaluation_criteria = [EvaluationCriterion(criteria['title'], criteria['description']) for criteria in evaluation_criteria]
        self.submissions = []

    def upload_submission(self, student, file):
        submission = {
            'student': student,
            'file': file,
            'feedback': [],
            'grade': None
        }
        self.submissions.append(submission)

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


# Example usage:

evaluation_criteria = [
    {"title": "Originality", "description": "The extent to which the work is original and creative."},
    {"title": "Clarity", "description": "The clarity and coherence of the work."},
    {"title": "Grammar and Spelling", "description": "The correctness of grammar, spelling, and punctuation."},
    {"title": "Use of Sources", "description": "The appropriate use of sources and references."}
]

assignment = Assignment("Intro to Swaggery Assignment #1", "Write a short essay about Swag in modern society", "2024-01-01", evaluation_criteria)
assignment.add_submission("John Doe", "/path/to/johndoe_essay.pdf")
assignment.display_details()
