from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg
from ..helpers import resume_pdf_builder

app = Flask(__name__)
api = Api(app)

resume_gen_arg = reqparse.RequestParser()
resume_gen_arg.add_argument("filename", type=str, help="Name of the user", required=True)
resume_gen_arg.add_argument("jobinfo", type=str, help="Paste in job info", required=True)

class Generate(Resource):
    '''
    This is for the gen page
    '''
    def post(self):
        '''
        Generate a resume
        '''
        args = resume_gen_arg.parse_args()
        pdf_name = args["filename"] + ".pdf"
        side_margin = 25
        r = resume_pdf_builder.ResumeBuilder(
            pdf_name,
            side_margin,
            "Set3_CURRENT",
            "",
            "",
            "",
            all_job_info=args["jobinfo"],
        )
        r.build()
        return {"data": "<div>Test</div>"}

api.add_resource(Generate, "/generate")

if __name__ == "__main__":
    app.run(debug=True)
