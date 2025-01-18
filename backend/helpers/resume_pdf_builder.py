from reportlab.lib.pagesizes import A4
from reportlab import platypus
from reportlab.platypus import Frame, Paragraph, Spacer, BaseDocTemplate, PageTemplate
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from . import resume_info
from . import styles
from . import standard_section


class ResumeBuilder:
    """
    The class that builds the resume
    Calling workflow:
    b = ResumeBuilder(...)
    b.build()
    """

    def build_all_frames(self, frame_heights: list[int]) -> tuple[list, list]:
        """
        Builds the lists required for making the resume from each data file
        also return a list of horizontal lines
        """
        result = []
        lines = []
        total_height = -1
        for frame_h in frame_heights:
            total_height += frame_h
            new_frame = Frame(
                1,
                A4[1] - total_height,
                A4[0] - 2,
                frame_h,
                leftPadding=self.side_margin - 1,
                rightPadding=self.side_margin - 1,
                showBoundary=False,
            )
            lines.append(A4[1] - total_height)
            result.append(new_frame)
        return result, lines

    def build_skills(self, skills_info: resume_info.AuxSectionsInfo) -> list:
        """
        Builds the content list for a section that uses skills format
        """
        section_content = []
        section_title_1 = Paragraph(
            skills_info.title,
            self.resume_style.subsections["SKILLS"]
            .subsections["title_font"]
            .get_paragraph_style(),
        )
        section_content.append(section_title_1)
        skill_items = skills_info.skills_list
        counter = 0
        while counter < (len(skill_items) - 1):
            content_1 = Paragraph(
                skill_items[counter],
                self.resume_style.subsections["SKILLS"]
                .subsections["point_left_font"]
                .get_paragraph_style(),
            )
            counter += 1
            content_2 = Paragraph(
                skill_items[counter],
                self.resume_style.subsections["SKILLS"]
                .subsections["point_right_font"]
                .get_paragraph_style(),
            )
            section_content.append(content_1)
            section_content.append(content_2)
            counter += 1
        if counter < len(skill_items):
            content_1 = Paragraph(
                skill_items[counter],
                self.resume_style.subsections["SKILLS"]
                .subsections["point_left_font"]
                .get_paragraph_style(),
            )
            section_content.append(content_1)
        return section_content

    def build_standard_content_section(self, standard_sec) -> list:
        """
        Builds the content list for a section that uses standard format
        Here: each element of content is [title, date, description]
        Comm: takes in a standard section
        """
        section_content = []
        curr_title = standard_sec.title
        # Edit the title if necessary
        section_title_1 = Paragraph(curr_title, standard_sec.font_title)
        section_content.append(section_title_1)
        for content in standard_sec.info_list:
            if standard_sec.section_style.attributes.item_heading_type != 0:
                content_title_1 = Paragraph(content[0], standard_sec.font_subtitle)
                content_title_2 = Paragraph(content[1], standard_sec.font_subright)
                section_content.append(content_title_1)
                section_content.append(content_title_2)
            if standard_sec.section_style.attributes.item_heading_type > 3:
                content_title_3 = Paragraph(content[2], standard_sec.font_subtitle2)
                content_title_4 = Paragraph(content[3], standard_sec.font_subright2)
                section_content.append(content_title_3)
                section_content.append(content_title_4)
            content_para = Paragraph(content[2], standard_sec.font_text)

            section_content.append(content_para)
        return section_content

    def build(self) -> None:
        """
        builds the pdf
        """
        # Make the file path under Documents
        documents_folder = os.path.join(
            os.path.expanduser("~"), "OneDrive", "Documents", "Resumes"
        )
        os.makedirs(documents_folder, exist_ok=True)
        pdf_path = os.path.join(documents_folder, self.pdf_name)

        # REPORT LAB SPECIFIC
        ####################################################################################
        # Prepare a canvas object
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setLineWidth(0.5)

        master_frame = Frame(5, 0, A4[0] - 5, A4[1], showBoundary=True)

        frames, lines_y = self.build_all_frames(self.resume_informations.height_list)

        all_contents = []

        header_container = self.resume_informations.heading_info

        # Two paragraphs for the header
        custom_space = Spacer(width=0, height=header_container.top_space)
        title_text = Paragraph(
            header_container.title,
            self.resume_style.subsections["HEADING"]
            .subsections["heading_name_font"]
            .get_paragraph_style(),
        )
        basic_info_text = platypus.Paragraph(
            header_container.header_basic_info,
            self.resume_style.subsections["HEADING"]
            .subsections["heading_desc_font"]
            .get_paragraph_style(),
        )
        # self.all_fonts.personal_info_font

        # Add to this array in order to populate the title
        header_content = [custom_space, title_text, basic_info_text]
        all_contents.append(header_content)

        for section in self.resume_informations.all_parsed_ss:
            all_contents.append(self.build_standard_content_section(section))

        # Add content to frames using canvas
        for i in range(5):
            frames[i].addFromList(all_contents[i], c)
            if i < 4:
                c.line(15, lines_y[i], A4[0] - 15, lines_y[i])

        c.save()
        print("all done!")

    def __init__(
        self,
        target_pdf_name: str,
        overall_side_margin: int,
        info_folder: str,
        all_resume_info: standard_section.SectInfo,
        job_sum: str,
        job_resp: str,
        job_req: str,
        all_job_info: str = "",
        gpt_model: str = "gpt-4o-mini",
    ) -> None:
        self.pdf_name = target_pdf_name
        self.side_margin = overall_side_margin
        self.resume_informations = resume_info.ResumeInfo(
            all_resume_info,
            info_folder,
            gpt_model,
            job_sum,
            job_resp,
            job_req,
            all_job_info,
        )
        self.resume_style = styles.ALlStyles().resume_style_0
        # self.all_fonts = fonts.AllFonts()
