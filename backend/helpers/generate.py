from . import db_fetch
from . import resume_pdf_builder
from . import resume_info


class ResumeGenerator:
    """
    Class to generate resume
    """

    def __init__(self) -> None:
        self.db_fetch = db_fetch.DBFetch()
        self.job_description = input("Enter the job description for testing: ")
        self.testing_selection = ["HEADING", "EXPERIENCE"]

    def generate(self, user_id: int) -> None:
        """
        Generate the resume
        """
        user_info = self.db_fetch.fetch_all(user_id, self.testing_selection)
        pdf_name = "BobSmithResume1.pdf"
        side_margin = 25
        r = resume_pdf_builder.ResumeBuilder(
            pdf_name, user_info, "", "", "", 10, self.job_description
        )
        r.build()
        print("Resume generated successfully")


if __name__ == "__main__":
    user_id = input("Enter the user ID: ")
    generator = ResumeGenerator()
    generator.generate(user_id)
