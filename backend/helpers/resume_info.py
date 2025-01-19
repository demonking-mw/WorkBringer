"""
Information container and processor to be used in resume_pdf_builder
Goal: takes as little params as possible for __init__
Note: attributes are indicated with a start of /=-z+f]j
(random shit that for sure wont be used by anything else)
Attribute cell should have 3 things separated by a space:
start-string, attribute name(all cap) and value
Example: (/=-z+f]j JAVA 8)
where the value is fixed to the range of 0-10 inclusive
Default attribute value should be a 0
"""

import dataclasses
import math
from reportlab.lib.pagesizes import A4

from . import styles
from . import standard_section
from . import gpt_attribute
from . import file_parse


@dataclasses.dataclass
class AuxSectionsInfo:
    """
    Dataclass for both the header and the skills section.
    """

    top_space: int  # Header Only
    title: str  # Header Only
    header_basic_info: str  # Header Only
    skills_list: list  # Skills Only
    height_buffer: int  # Both
    trait_subtrait_list: list


class ResumeInfo:
    """
    Contains the information that goes into the resume
    The resume pdf builder calls this to get the texts
    Sections: Skills, Education, Experiences, Projects
    """

    def get_header_height(self, header_data_class) -> int:
        """
        Gets the supposed height for the header
        """
        result = 0
        result += header_data_class.top_space
        result += self.resume_style.subsections["HEADING"].subsections["heading_name_font"].font_attributes.leading
        #result += self.custom_fonts.name_font.leading
        result += self.resume_style.subsections["HEADING"].subsections["heading_desc_font"].font_attributes.leading
        #result += self.custom_fonts.personal_info_font.leading
        result += header_data_class.height_buffer
        return result

    def get_skills_height(self, skills_data_class):
        """
        Gets the supposed height for the skills section
        """
        result = 0

        result += self.resume_style.subsections["SKILLS"].subsections["title_font"].font_attributes.leading
        #result += self.custom_fonts.section_title.leading
        vert = math.ceil(len(skills_data_class.skills_list) / 2)
        result += vert * self.resume_style.subsections["SKILLS"].subsections["point_right_font"].font_attributes.leading
        #self.custom_fonts.point_right.leading
        result += skills_data_class.height_buffer
        return result

    def parse_heading(self, info_list: list[list]) -> AuxSectionsInfo:
        """
        Returns info about the heading
        Heading file format:
        "HEADING", Top_Margin(int)
        Name, Personal_Info, height_buffer
        """
        if not info_list[0][0] == "HEADING":
            print("ERROR: HEADING FILE MISMATCH")
            return None
        return AuxSectionsInfo(
            top_space=int(info_list[0][1]),
            title=info_list[1][0],
            header_basic_info=info_list[1][1],
            skills_list=[],
            height_buffer=int(info_list[1][2]),
            trait_subtrait_list=[],
        )

    def parse_skills(
        self, info_list: list[list], selection_list=None
    ) -> AuxSectionsInfo:
        """
        Returns info about the skills section
        Skills file format:
        "Skills", Height_buffer
        Skill 1, ATT1, ATT2,...
        Skill 2, ATT1, ATT2,...
        Skill 3, ATT1, ATT2,...
        ...
        """
        if not info_list[0][0] == "SKILLS":
            print("ERROR: SKILLS FILE MISMATCH")
            return None

        selection = range(len(info_list) - 1)
        if selection_list:
            selection = selection_list
        selected_info = []
        ts_list = []
        for i in selection:
            ts_sub1 = []
            ts_sub2 = []
            ts_sub1.append(info_list[i + 1][0])
            with_dot = "• " + info_list[i + 1][0]
            selected_info.append(with_dot)
            for k in range(len(info_list[i + 1]) - 1):
                ts_sub2.append(info_list[i + 1][k + 1])
            ts_sub1.append(ts_sub2)
            ts_list.append(ts_sub1)
        return AuxSectionsInfo(
            top_space=0,
            title="SKILLS",
            header_basic_info="",
            skills_list=selected_info,
            height_buffer=int(info_list[0][1]),
            trait_subtrait_list=ts_list,
        )

    def parse_standard(
        self, target_type: str, info_list: list[list]
    ) -> standard_section.StandardSection:
        """
        Parse a standard section, can be education, experience, or porjects
        File format:
        Type,
        sub_top_right, sub_top_left, sub_content
        ...
        ...
        """
        if not info_list[0][0] == target_type:
            print("ERROR: " + target_type + " FILE MISMATCH")
            return None
        selection = list(range(len(info_list) - 1))
        if info_list[0][1] == "BP":
            is_bp = True
        else:
            is_bp = False

        selected_info = []
        for i in selection:
            selected_info.append(info_list[i + 1])
        return standard_section.StandardSection(
            target_type, selected_info, bullet_point=is_bp
        )

    def mod_standard(
        self, standard_sec: standard_section.StandardSection, selection_list: list
    ) -> standard_section.StandardSection:
        """
        Modify a full standard_section by only keeping what's been selected
        """
        sec_title = standard_sec.title
        bull_point = standard_sec.bullet_point
        full_info_list = standard_sec.raw_info_list
        refined_list = []
        for i in selection_list:
            refined_list.append(full_info_list[i])
        return standard_section.StandardSection(
            sec_title, refined_list, bullet_point=bull_point
        )

    def get_mega_list(self, sec_info: list[standard_section.StandardSection]) -> list:
        """
        Gets an overarching list containing everything abount the entir resume
        """
        result = []
        for i in range(len(sec_info)):
            sub = []
            for n in range(len(sec_info[i].attribute_weight_list)):
                sub.append(
                    [
                        sec_info[i].attribute_weight_list[n],
                        sec_info[i].sub_height_list[n],
                    ]
                )
            result.append(sub)
        return result

    def get_all_skills_att(self) -> list:
        """
        potentially useful in the get_desired_traits
        gets all skills there exists in the entire resume
        """
        result = []
        print(self.skills_att_list)
        print()
        for skills in self.all_edu_info.attribute_weight_list:
            for skill_pair in skills:
                if skill_pair[0] not in result:
                    result.append(skill_pair[0])
        for skills in self.all_proj_info.attribute_weight_list:
            for skill_pair in skills:
                if skill_pair[0] not in result:
                    result.append(skill_pair[0])
        for skills in self.all_exp_info.attribute_weight_list:
            for skill_pair in skills:
                if skill_pair[0] not in result:
                    result.append(skill_pair[0])
        result = [item for item in result if item != "MANDATORY_INCLUDE"]
        return result

    def get_desire(self, gpt_model: str) -> list[list]:
        """
        GPT intergration
        """
        # TEMPORARY: SIMPLE SOLUTION: everything in the skills section
        ################################################
        empty_template = []
        for att in self.all_att_in_skills:
            empty_template.append([att, 1])
        # CHATGPT HERE
        gpt_response = gpt_attribute.GPT_Attribute(
            empty_template,
            gpt_model,
            self.job_sum,
            self.job_resp,
            self.job_req,
            self.all_job_info,
        )
        result = gpt_response.gpt_modded_list
        # Add mandatory_inclusion
        result.append(["MANDATORY_INCLUDE", 100000])
        return result
        ################################################

    def calc_score(self, att_list: list) -> int:
        """
        calculate the score of an item in a section, add one at the end since
        anything is better than nothing
        """
        result = 0
        for att in att_list:
            for req in self.desired_skillset:
                if att[0] == req[0]:
                    result += att[1] * req[1]
        return result + 1

    def build_score_height_list(self) -> list[list]:
        """
        Builds a list of lists of:
        section_num, item_num, score, height
        """
        result = []
        for n in range(len(self.sections_mega_list)):
            section_att_list = self.sections_mega_list[n]
            for i in range(len(section_att_list)):
                sc = self.calc_score(section_att_list[i][0])
                result.append([n, i, sc, section_att_list[i][1]])
        return result

    def generate_resume_list(self) -> list[list]:
        """
        THIS IS THE HEART OF THE BACK-END
        Generates the selection list for each section
        Takes in: skills, mega_list, desired_skillset
        Outputs a selection list for skills,
        and a list of selection lists for each section
        """
        sc_height_list = self.build_score_height_list()
        avail_height = int(A4[1]) - self.existing_height
        DP = [0] * (avail_height + 1)
        selected = [[] for _ in range(avail_height + 1)]
        for point in sc_height_list:
            for i in range(avail_height, int(point[3]) - 1, -1):
                if DP[i - int(point[3])] + point[2] > DP[i]:
                    DP[i] = DP[i - int(point[3])] + point[2]
                    selected[i] = selected[i - int(point[3])] + [point]
        # now unpack the selected array and return the right thing

        result = [[] for _ in range(len(self.sections_mega_list))]
        for point in selected[avail_height - 1]:
            result[point[0]].append(point[1])
        return result

    def __init__(
        self,
        folder_name: str,
        gpt_model: str,
        job_sum: str,
        job_resp: str,
        job_req: str,
        all_job_info: str = "",
    ) -> None:
        """
        Defining the ResumeInfo
        Grab information from file
        Purpose: feed info to resume_pdf_builder
        Note: print something if the pdf cannot be fully built on page
        """

        # Parse Requirement
        ##################################################################
        # Basic Info
        ##################################################################
        
        self.resume_style = styles.ALlStyles().resume_style_0
        #StyleInfo as a resume
        #self.custom_fonts = fonts.AllFonts()
        self.topic_list = ["HEADING", "SKILLS", "EDUCATION", "EXPERIENCE", "PROJECTS"]
        self.section_filenames = [
            "HEADING.csv",
            "SKILLS.csv",
            "EDUCATION.csv",
            "EXPERIENCE.csv",
            "PROJECTS.csv",
        ]
        ################################################################

        # Reads file
        ################################################################
        # Parse
        self.job_sum = job_sum
        self.job_resp = job_resp
        self.job_req = job_req
        self.all_job_info = all_job_info
        self.height_list = []
        self.file_parser = file_parse.FileAccMod()
        self.all_info_list = self.file_parser.get_all(
            self.section_filenames, folder_name
        )
        self.skills_info = self.parse_skills(self.all_info_list[1])
        self.all_edu_info = self.parse_standard("EDUCATION", self.all_info_list[2])
        self.all_exp_info = self.parse_standard("EXPERIENCE", self.all_info_list[3])
        self.all_proj_info = self.parse_standard("PROJECTS", self.all_info_list[4])
        self.heading_info = self.parse_heading(self.all_info_list[0])

        # Deal with file
        self.existing_height = (
            self.get_header_height(self.heading_info)
            + self.get_skills_height(self.skills_info)
            + self.all_edu_info.empty_height
            + self.all_exp_info.empty_height
            + self.all_proj_info.empty_height
            + 5
        )
        self.skills_att_list = self.skills_info.trait_subtrait_list
        self.sections_mega_list = self.get_mega_list(
            [self.all_edu_info, self.all_exp_info, self.all_proj_info]
        )
        # Note: the bug is here
        self.all_att_in_skills = self.get_all_skills_att()
        self.desired_skillset = self.get_desire(gpt_model)
        self.resume_selection_list = self.generate_resume_list()

        # Add
        self.edu_info = self.mod_standard(
            self.all_edu_info, self.resume_selection_list[0]
        )
        self.exp_info = self.mod_standard(
            self.all_exp_info, self.resume_selection_list[1]
        )
        self.proj_info = self.mod_standard(
            self.all_proj_info, self.resume_selection_list[2]
        )
        self.height_list.append(self.get_header_height(self.heading_info))
        self.height_list.append(self.get_skills_height(self.skills_info))
        self.height_list.append(self.edu_info.total_height)
        self.height_list.append(self.exp_info.total_height)
        self.height_list.append(self.proj_info.total_height)
        ###############################################################
