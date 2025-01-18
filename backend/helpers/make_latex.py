from dataclasses import dataclass
from pathlib import Path
"""
Takes in an info class, builds the resume in latex, and returns the latex string

Info taken in must be latex ready: that is, each string should be ready to be
thrown right into latex parser.
"""
@dataclass
class ResumeInfoSet:
    '''
    sect_info_list: each item is a section:
    section_name, section_type, list_of_items
    
    each item in list_of_items is:
    list_of_headings, list_of_contents
    '''
    person_name: str
    person_info: str # latex string
    sect_info_list: list
    
class LatexMaker:
    def __init__(self, info: ResumeInfoSet):
        self.info = info
               

    def build(self):
        script_dir = Path(__file__).parent
        file_path = script_dir / 'latex_template.txt'
        with file_path.open('r') as file:
            result = file.read()
        
        result += f"""
        \\begin{{document}}

        \\begin{{center}}
            \\textbf{{\\Huge \\scshape {self.info.person_name}}} \\\\ \\vspace{{1pt}}
            \\small {self.info.person_info}
        \\end{{center}}
        """
        for sect in self.info.sect_info_list:
            section_name = sect[0]
            section_type = sect[1]
            list_of_items = sect[2]
            # build the section header
            result += f'\\section{{{section_name}}}\n'
            result += "\\resumeSubHeadingListStart"
            for item in list_of_items:
                if section_type == 2:
                    # two item heading format
                    result += f"""
                    \\resumeProjectHeading
                    {{\\textbf{{{item[0][0]}}}}}{{{item[0][1]}}}
                    \\resumeItemListStart
                    """
                elif section_type == 3:
                    # three item heading format
                    result += f"""
                    \\resumeProjectHeading
                    {{\\textbf{{{item[0][0]}}} $|$ \\emph{{{item[0][1]}}}}}{{{item[0][2]}}}
                    \\resumeItemListStart
                    """
                elif section_type == 4:
                    # four item heading format
                    result += f"""
                    \\resumeSubheading
                    {{{item[0][0]}}}{{{item[0][1]}}}
                    {{{item[0][2]}}}{{{item[0][3]}}}
                    \\resumeItemListStart
                    """
                else:
                    # five item heading format
                    result += f"""
                    \\resumeSubheading
                    {{\\textbf{{{item[0][0]}}} $|$ \\emph{{{item[0][1]}}}}}{{{item[0][2]}}}
                    {{{item[0][3]}}}{{{item[0][4]}}}
                    \\resumeItemListStart
                    """
                for content in item[1]:
                    result += f"\\resumeItem{{{content}}}\n"
                result += "\\resumeItemListEnd\n"
            result += "\\resumeSubHeadingListEnd\n"
        result += "\\end{document}\n"
        return result

if __name__ == "__main__":
    # Sample data for testing
    sample_info = ResumeInfoSet(
        person_name="John Doe",
        person_info="Software Engineer with 5 years of experience",
        sect_info_list=[
            ("Education", 3, [
                (["B.Sc in Computer Science", "University XYZ", "2015-2019"], ["Graduated with honors", "GPA: 3.8/4.0"]),
                (["M.Sc in Computer Science", "University ABC", "2019-2021"], ["Thesis on AI", "GPA: 4.0/4.0"])
            ]),
            ("Experience", 4, [
                (["Software Engineer", "Tech Company", "2021-Present", "City, Country"], ["Developed various applications", "Led a team of 5 engineers"]),
                (["Intern", "Another Tech Company", "Summer 2020", "City, Country"], ["Worked on backend systems", "Improved performance by 20\\%"])
            ])
        ]
    )

    latex_maker = LatexMaker(sample_info)
    latex_content = latex_maker.build()
    print(latex_content)