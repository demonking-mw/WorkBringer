"""
A class that stores all custom fonts 
"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from . import style_info

class ALlStyles:
    """
    A reworked class that stores all custom styles 
    (try to) implement multiple styles if possible
    Calling styles: use natural nums.
    Naming convention: name_type
    Example: title_font or title_bold_font
    """
    font_lib = {
        "title_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="title_font",
            font_name="Helvetica-Bold",
            font_size=13,
            text_color_hex="#000000",
            alignment=1,
            space_before=1,
            space_after=0,
            leading=17,
        )),
        "subtitle_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="subsection_title_font",
            font_name="Times-Bold",
            font_size=12,
            text_color_hex="#000000",
            alignment=0,
            space_before=5,
            space_after=0,
            leading=0,
        )),
        "subright_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="subright_font",
            font_name="Times-Bold",
            font_size=12,
            text_color_hex="#000000",
            alignment=2,
            space_before=0,
            space_after=0,
            leading=16,
        )),
        "standard_text_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="text_font_standard_sec",
            font_name="Times-Roman",
            font_size=11,
            text_color_hex="#000000",
            alignment=0,
            space_before=0,
            space_after=0,
            leading=14,
        )),
        "heading_name_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="name_font",
            font_name="Helvetica-Bold",
            font_size=16,
            text_color_hex="#000000",
            alignment=1,
            space_before=5,
            space_after=0,
            leading=25,
        )),
        "heading_desc_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="personal_info_font",
            font_name="Helvetica",
            font_size=11,
            text_color_hex="#000000",
            alignment=1,
            space_before=0,
            space_after=0,
            leading=15,
        )),
        "point_left_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="point_left",
            font_name="Times-Roman",
            font_size=11,
            text_color_hex="#000000",
            alignment=0,
            space_before=0,
            space_after=0,
            leading=0,
        )),
        "point_right_font": style_info.StyleInfo(font_attributes=style_info.FontAttributes(
            name="point_right",
            font_name="Times-Roman",
            font_size=11,
            text_color_hex="#000000",
            alignment=0,
            space_before=0,
            space_after=0,
            leading=14,
            left_indent=A4[0] / 2,
        )),
    }
    default_section_style_0 =style_info.SectionAttributes(
            side_margin=20,
            top_margin=5,
            height_buffer=3,
            wrap_forgive=5,
            bullet_symbol="• ",
            paper_width=A4[0],
        )
    
    section_att_lib_0 = {
        "HEADING": style_info.StyleInfo(
            section_attributes=style_info.SectionAttributes(
                side_margin=20,
                top_margin=5,
                height_buffer=10,
                wrap_forgive=20,
                paper_width=A4[0],
            ),
            subStyleInfo=font_lib
        ),
        "SKILLS": style_info.StyleInfo(
            section_attributes=default_section_style_0,
            subStyleInfo=font_lib
        ),
        "EDUCATION": style_info.StyleInfo(
            section_attributes=style_info.SectionAttributes(
                side_margin=20,
                top_margin=5,
                height_buffer=10,
                wrap_forgive=20,
                paper_width=A4[0],
            ),
            subStyleInfo=font_lib),
        "EXPERIENCE": style_info.StyleInfo(
            section_attributes=default_section_style_0,
            subStyleInfo=font_lib
        ),
        "PROJECTS": style_info.StyleInfo(
            section_attributes=default_section_style_0,
            subStyleInfo=font_lib
        ),
    }
    
    resume_style_0 = style_info.StyleInfo(subStyleInfo=section_att_lib_0)
    
    def __init__(self) -> None:
        print("styles init")
    
    
    
    
class AllFonts:
    """
    Stores all font info
    """
    resume_title = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Bold",
        fontSize=14,
        textColor=colors.black,
        alignment=1,
        spaceAfter=0,
        leading=12,
    )
    #
    section_title = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Bold",
        fontSize=14,
        textColor=colors.black,
        alignment=1,
        spaceAfter=0,
        leading=15,
    )
    subsection_title = ParagraphStyle(
        name="SubTitleFont",
        fontName="Times-Bold",
        fontSize=13,
        textColor=colors.black,
        spaceBefore=8,
        alignment=0,
        spaceAfter=0,
        leading=0,
    )
    subright_title = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Bold",
        fontSize=13,
        textColor=colors.black,
        alignment=2,
        spaceAfter=0,
        leading=18,
    )
    text_font_standard_sec = ParagraphStyle(
        name="paraFont",
        fontName="Times-Roman",
        fontSize=11,
        textColor=colors.black,
        alignment=0,
        spaceAfter=0,
        leading=16,
    )
    name_font = ParagraphStyle(
        name="nameFont",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=colors.black,
        alignment=1,
        spaceAfter=3,
        leading=18,
    )

    personal_info_font = ParagraphStyle(
        name="personalInfoFont",
        fontName="Times-Bold",
        fontSize=12,
        textColor=colors.black,
        alignment=1,
        spaceAfter=0,
        leading=15,
    )
    point_left = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Roman",
        fontSize=11,
        textColor=colors.black,
        spaceBefore=0,
        alignment=0,
        spaceAfter=0,
        leading=0,
    )
    point_right = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Roman",
        fontSize=11,
        textColor=colors.black,
        leftIndent=A4[0] / 2,
        alignment=0,
        spaceAfter=0,
        leading=14,
    )

    def __init__(self) -> None:
        print("fonts init")
