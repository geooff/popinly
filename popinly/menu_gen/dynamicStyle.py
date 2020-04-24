def userColourTemplate():
    return """$primary-color: {};
        $secondary-color: {};
        $accent-color: {};"""


def userFontTemplate():
    return """@import url('https://fonts.googleapis.com/css2?family={impact_web}&display=swap');
@import url('https://fonts.googleapis.com/css2?family={base_web}&display=swap');

$impact-font: '{impact}', sans-serif;
$base-font: '{base}', sans-serif;"""
