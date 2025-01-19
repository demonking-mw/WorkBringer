from flask import Flask, Response
from flask_restful import Api, Resource, reqparse
import psycopg
import io

from ..helpers import resume_pdf_builder
from ..helpers import file_parse

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
        buffer = io.BytesIO()
        args = resume_gen_arg.parse_args()
        pdf_name = args["filename"] + ".pdf"
        side_margin = 25
        r = resume_pdf_builder.ResumeBuilder(
            buffer,
            side_margin,
            "Set3_CURRENT",
            "",
            "",
            "",
            all_job_info=args["jobinfo"],
        )
        r.build()
        buffer.seek(0)
        return Response(
            buffer, mimetype='application/pdf', headers={
            "Content-Disposition": f"inline; filename={args['filename']}.pdf"
        })

api.add_resource(Generate, "/generate")

resume_fetch_arg = reqparse.RequestParser()
resume_gen_arg.add_argument("type", type=str, help="short or regular", required=True)
resume_gen_arg.add_argument("section", type=str, help="specify section. empty str for all", required=True)

resume_post_arg = reqparse.RequestParser()
resume_post_arg.add_argument("filename", type=str, help="Name of the user", required=True)
resume_post_arg.add_argument("jobinfo", type=str, help="Paste in job info", required=True)

class File(Resource):
    '''
    This is for the file page
    '''
    def get(self):
        '''
        Get a file
        '''
        args = resume_fetch_arg.parse_args()
        folder = "Set3_CURRENT"
        if args["type"] == "short":
            if args["section"] == "":
                rand, target = file_parse.print_folder(folder, brief = True)
                return{"file": target}
            else:
                rand, target = file_parse.print_folder_list(folder, args["section"])
                return {"file": target}
        else:
            if args["section"] == "":
                rand, target = file_parse.print_folder(folder)
                return {"file": target}
            else:
                rand, target = file_parse.print_folder_list(folder, args["section"])
                return {"file": target}
        return "File"
    def post(self):
        '''
        Post a file
        '''
        
api.add_resource(File, "/file")

if __name__ == "__main__":
    app.run(debug=True)
