# WorkBringer
That one thing that brings work, whether it is internship or an actual job. It is not a blade of any sort, regardless which one you have in mind.

DATA DEFINITION:

User: 
- uid: str
- pw: str
- account type: int
- rsid_list: list of int(rsids that belongs to the user)

Section: A section of the resume
- rsid: int (resume_section_id)
- header_name: str
- sect_type: int (whether it is 2x1, 2x2, etc)
- item_list: list of int (iid)

Item: A specific thing in the resume
- iid: int (item_id)
- type: int (for varification)
- header_list: list of str: maybe have the length as the type? One for heading perhaps
- contents: list of strings
- attributes: JSON

Stored in Backend:
A StyleInfo as a font is StyleInfo(style_id=123, font_attributes=FontAttributes(...))
    
A StyleInfo as a section is:
StyleInfo(style_id=123, section_attributes=SectionAttributes(...), other_attributes, font_lib={listof StyleInfo-as-font})

A StyleInfo as a resume is:
StyleInfo(style_id=123, section_attributes=SectionAttributes(...(default behavior)), other_attributes, subStyleInfo={listof StyleInfo-as-section}, font_lib={listof StyleInfo-as-font})

NOTE FOR STYLEINFO:
Need to change to encorporate different types of sections


LATEX GEN:
https://jeltef.github.io/PyLaTeX/current/



venv activate:
venv\Scripts\activate.bat