from datetime import datetime

from pylatex.base_classes import Environment, CommandBase, Arguments
from pylatex.basic import NewLine, HFill
from pylatex import (
    Document,
    Section,
    Subsection,
    Command,
    TikZ,
    TikZNode,
    TikZDraw,
    TikZCoordinate,
    TikZUserPath,
    TikZOptions,
    Package,
    UnsafeCommand,
    VerticalSpace,
)
from pylatex.utils import italic, NoEscape


class menuSection(Environment):
    """
    A class representing a custom LaTeX environment.

    This class represents a custom LaTeX environment named
    ``menuSection``.
    """

    _latex_name = "menuSection"


class menuEntry(CommandBase):
    """
    A class representing a custom LaTeX command.

    This class represents a custom LaTeX command named
    ``menuEntry``.
    """

    _latex_name = "menuEntry"


class menuSubEntry(CommandBase):
    """
    A class representing a custom LaTeX command.

    This class represents a custom LaTeX command named
    ``menuSubEntry``.
    """

    _latex_name = "menuSubEntry"


class colourText(CommandBase):
    """
    A class representing a custom LaTeX command.

    This class represents a custom LaTeX command named
    ``ColourText``.
    """

    _latex_name = "colourText"


def init_env(kwargs):
    # Pass in document key-word parameters (page_type, font, ect)
    doc = Document(**document_params)

    # Add Packages for text styling
    doc.packages.append(Package("textcomp"))
    doc.packages.append(Package("xcolor", ["x11names"]))

    # Add Packages for border
    doc.packages.append(Package("pgfornament", ["object=vectorian"]))
    doc.packages.append(Package(NoEscape("eso-pic")))

    # Remove Pagenumbering
    doc.append(NoEscape(r"\pagenumbering{gobble}"))

    doc.preamble.append(
        NoEscape(r"\newcommand*\wb[3]{{\fontsize{#1}{#2}\usefont{U}{webo}{xl}{n}#3}}")
    )

    # Init menu functions
    doc.preamble.append(
        UnsafeCommand(
            "newcommand", "\menuEntry", options=2, extra_arguments=r"\sffamily#1 & #2"
        )
    )

    doc.preamble.append(
        UnsafeCommand(
            "newcommand",
            "\menuSubEntry",
            options=1,
            extra_arguments=r"\hspace*{1em}\footnotesize #1",
        )
    )

    doc.preamble.append(
        UnsafeCommand(
            "newcommand",
            "\colourText",
            options=1,
            extra_arguments=r"\textcolor{Goldenrod3}{#1}",
        )
    )

    new_env = UnsafeCommand(
        "newenvironment",
        "menuSection",
        options=1,
        extra_arguments=[
            r"\noindent\begin{tabular*}{\textwidth}{@{}p{.8\linewidth}@{\extracolsep{\fill}}r@{}}{\fontsize{24}{29}\selectfont\colourText{#1}}\\[0.8em]}{\end{tabular*}",
        ],
    )
    doc.preamble.append(new_env)
    return doc


def fill_pageframe(doc):
    # add our sample drawings
    doc.append(NoEscape(r"\makeatletter"))
    doc.append(NoEscape(r"\AddToShipoutPicture{"))
    doc.append(NoEscape(r"\begingroup"))
    doc.append(
        NoEscape(
            r"\setlength{\@tempdima}{2mm}% \setlength{\@tempdimb}{\paperwidth-\@tempdima-2cm}% \setlength{\@tempdimc}{\paperheight-\@tempdima}% \put(\LenToUnit{\@tempdima},\LenToUnit{\@tempdimc}){"
        )
    )
    doc.append(
        NoEscape(
            r"\pgfornament[anchor=north west,width=2cm]{63}} \put(\LenToUnit{\@tempdima},\LenToUnit{\@tempdima}){"
        )
    )
    doc.append(
        NoEscape(
            r"\pgfornament[anchor=south west,width=2cm,symmetry=h]{63}} \put(\LenToUnit{\@tempdimb},\LenToUnit{\@tempdimc}){"
        )
    )
    doc.append(
        NoEscape(
            r"\pgfornament[anchor=north east,width=2cm,symmetry=v]{63}} \put(\LenToUnit{\@tempdimb},\LenToUnit{\@tempdima}){"
        )
    )
    doc.append(NoEscape(r"\endgroup"))
    doc.append(NoEscape(r"}"))
    doc.append(NoEscape(r"\makeatother"))


def fill_document(environmentdoc):
    with doc.create(menuSection(arguments=Arguments("Meat"))) as environment:
        environment.append(menuEntry(arguments=Arguments("Steak au Povre", "$12")))
        environment.append(NoEscape(r"\\"))
        environment.append(
            menuSubEntry(arguments=Arguments("Delicious Steak with pepper sause"))
        )
        doc.append(NoEscape(r"\\"))
        environment.append(menuEntry(arguments=Arguments("Beef tartar", "$8")))
        environment.append(NoEscape(r"\\"))
        environment.append(
            menuSubEntry(arguments=Arguments("Raw beef serve with a raw egg"))
        )
        doc.append(NoEscape(r"\\"))
        environment.append(menuEntry(arguments=Arguments("Beef burgenion", "$12")))
        environment.append(NoEscape(r"\\"))
        environment.append(menuSubEntry(arguments=Arguments("I spelt this one wrong")))
        doc.append(NoEscape(r"\\"))
    doc.append(NoEscape(r"\vfill"))
    with doc.create(menuSection(arguments=Arguments("Pasta"))) as environment:
        environment.append(
            menuEntry(arguments=Arguments("Spagetti and Meatballs", "$12"))
        )
        environment.append(NoEscape(r"\\"))
        environment.append(
            menuSubEntry(arguments=Arguments("Spagetti served with a rich meatsause"))
        )
        environment.append(NoEscape(r"\\"))


if __name__ == "__main__":
    paper_type = "letterpaper"  # a4paper
    document_params = {
        "default_filepath": "Admin_{}".format(datetime.now().isoformat()),
        "document_options": [paper_type],
        "geometry_options": ["centering", "textwidth=12cm"],
    }
    # Basic document
    doc = init_env(document_params)
    fill_pageframe(doc)
    fill_document(doc)

    doc.generate_pdf(clean=True, clean_tex=False)
