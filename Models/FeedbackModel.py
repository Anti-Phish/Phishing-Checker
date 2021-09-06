

class FeedbackModel:
    def __init__(self, name, email, subject, comment):
        self.name = name
        self.email = email
        self.subject = subject
        self.comment = comment
        self.feedback = {
            "name": name,
            "email": email,
            "subject": subject,
            "comment": comment
        }
