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


@dataclasses.dataclass
class FullResumeInfo:
    """
    Dataclass to pass everything about a resume
    all_info_list: a list of sections
    each section is:standard_section.SecInfo

    sect_list serves as ordering
    """

    sect_list: list
    all_info_list: list


@dataclasses.dataclass
class HeaderInfo:
    """
    Dataclass for both the header and the skills section.
    """

    top_space: int  # Header Only
    title: str  # Header Only
    header_basic_info: str  # Header Only
    height_buffer: int  # Both


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
        result += (
            self.resume_style.subsections[0]
            .subsections["heading_name_font"]
            .font_attributes.leading
        )
        # result += self.custom_fonts.name_font.leading
        result += (
            self.resume_style.subsections[0]
            .subsections["heading_desc_font"]
            .font_attributes.leading
        )
        # result += self.custom_fonts.personal_info_font.leading
        result += header_data_class.height_buffer
        return result

    '''
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
    '''

    def parse_heading(self, info_list) -> HeaderInfo:
        """
        Returns info about the heading
        Heading file format:
        "HEADING", Top_Margin(int)
        Name, Personal_Info, height_buffer
        """
        return HeaderInfo(
            top_space=10,
            
            title=info_list.all_info[0][0][0],
            header_basic_info=info_list.all_info[0][0][1],
            height_buffer=10,
        )

    '''
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
    '''

    def mod_standard(
        self, standard_sect: standard_section.StandardSectionInfo, selection_list: list
    ) -> standard_section.StandardSectionInfo:
        """
        Modify a full standard_section by only keeping what's been selected
        """
        sect_title = standard_sect.titles
        bull_point = standard_sect.bullet_point
        sect_style = standard_sect.sect_style
        full_info_list = standard_sect.sect_info.all_info
        refined_list = []
        for i in selection_list:
            refined_list.append(full_info_list[i])
        return standard_section.StandardSectionInfo(
            standard_section.SectInfo(sect_title, refined_list, sect_style, bull_point)
        )

    def get_all_skills(self) -> dict:
        """
        Returns a dictionary of all the skills in the resume
        """
        result = {"tech": [], "soft": [], "asset": []}
        for sect in self.all_sect_list:
            for item in sect.sect_info.all_info:
                for att in item[2]["tech"]:
                    if att[0] not in result["tech"]:
                        result["tech"].append([att[0], 1])
                for att in item[2]["soft"]:
                    if att[0] not in result["soft"]:
                        result["soft"].append([att[0], 1])
                for att in item[2]["asset"]:
                    if att[0] not in result["asset"]:
                        result["asset"].append([att[0], 1])
        return result

    def get_desire(self, gpt_model: str) -> list[list]:
        """
        GPT intergration
        """
        # TEMPORARY: SIMPLE SOLUTION: everything in the skills section
        ################################################
       
        # CHATGPT HERE
        gpt_response = gpt_attribute.GPT_Attribute(
            self.get_all_skills(),
            gpt_model,
            self.job_sum,
            self.job_resp,
            self.job_req,
            self.all_job_info,
        )
        result = gpt_response.gpt_modded_list
        # Add mandatory_inclusion
        result["asset"].append(["MANDATORY_INCLUDE", 100000])
        return result
        ################################################

    def calc_score(self, att_list: dict) -> int:
        """
        calculate the score of an item in a section, add one at the end since
        anything is better than nothing
        """
        result = 0
        # param
        tech_max_of = 3
        soft_top_bonus_rate = 1.5
        asset_thresh = 25
        # tech
        tech_score_list = []
        for att in att_list["tech"]:
            for req in self.desired_skillset["tech"]:
                if att[0] == req[0]:
                    tech_score_list.append(att[1] * req[1])
        tech_score_list.sort(reverse=True)
        result += sum(tech_score_list[:tech_max_of])

        # soft
        soft_score_list = []
        for att in att_list["soft"]:
            for req in self.desired_skillset["soft"]:
                if att[0] == req[0]:
                    soft_score_list.append(att[1] * req[1])
        soft_score_list.sort(reverse=True)
        if soft_score_list:
            soft_score_list[0] *= soft_top_bonus_rate
        result += sum(soft_score_list) / len(soft_score_list)

        # asset
        for att in att_list["asset"]:
            for req in self.desired_skillset["asset"]:
                if att[0] == req[0]:
                    asset_power = att[1] * req[1]
                    if asset_power > asset_thresh:
                        result += asset_power
        return result + 1

    def build_score_height_list(self) -> list[list]:
        """
        Builds a list of lists of:
        section_num, item_num, score, height
        """
        result = []
        for n in range(len(self.all_sect_list)):
            section_list = self.all_sect_list[n]
            for i in range(len(section_list.sect_info.all_info)):
                sc = self.calc_score(section_list.sect_info.all_info[i][2])
                result.append([n, i, sc, self.all_sect_list[n].sub_height_list[i]])
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

        result = [[] for _ in range(len(self.all_sect_list))]
        for point in selected[avail_height - 1]:
            result[point[0]].append(point[1])
        return result

    def __init__(
        self,
        all_resume_info: FullResumeInfo,
        gpt_model: str,
        job_sum: str,
        job_resp: str,
        job_req: str,
        all_job_info: str = "",
    ) -> None:
        """
        Defining the ResumeInfo
        Grab information from full_resume_info
        Purpose: feed info to resume_pdf_builder
        Note: print something if the pdf cannot be fully built on page
        """
        

        # Parse Requirement
        ##################################################################
        # Basic Info
        ##################################################################
        self.all_resume_info = all_resume_info
        self.resume_style = styles.ALlStyles().resume_style_0
        # StyleInfo as a resume
        # self.custom_fonts = fonts.AllFonts()
        self.topic_list = self.all_resume_info.sect_list
        ################################################################

        # Reads file
        ################################################################
        # Parse
        self.job_sum = job_sum
        self.job_resp = job_resp
        self.job_req = job_req
        self.all_job_info = all_job_info
        self.height_list = []
        self.all_info_list = []
        for sect_name in self.all_resume_info.sect_list:
            for section in self.all_resume_info.all_info_list:
                if section.title == sect_name:
                    self.all_info_list.append(section)
        self.all_sect_list = []
        # each item in all_sect_list is either a HeaderInfo or StandardSection
        for section in self.all_info_list:
            if section.title == "HEADING":
                self.heading_info = self.parse_heading(section)
            else:
                self.all_sect_list.append(standard_section.StandardSectionInfo(section))

        # Deal with file
        self.existing_height = self.get_header_height(self.heading_info) + 5
        for stand_sec in self.all_sect_list:
            self.existing_height += stand_sec.empty_height

        # Note: the sections_mega_list is basically all_sect_list
        
        self.desired_skillset = self.get_desire(gpt_model)
        self.resume_selection_list = self.generate_resume_list()

        self.all_parsed_ss = []
        for i in range(len(self.all_sect_list)):
            self.all_parsed_ss.append(
                self.mod_standard(self.all_sect_list[i], self.resume_selection_list[i])
            )
            self.height_list.append(self.all_sect_list[i].total_height)

