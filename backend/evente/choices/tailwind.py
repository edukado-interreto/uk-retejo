from typing import Self

from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


BREAKPOINTS = ["sm", "md", "lg", "xl", "2xl"]


class Fonts(TextChoices):
    RALEWAY = "font-raleway", "Raleway"
    POPPINS = "font-poppins", "Poppins"
    UNBOUNDED = "font-unbounded", "Unbounded"


class FontWeights(TextChoices):
    THIN = "font-thin", _("Thin")
    EXTRALIGHT = "font-extralight", _("Extra light")
    LIGHT = "font-light", _("Light")
    NORMAL = "font-normal", _("Normal")
    MEDIUM = "font-medium", _("Medium")
    SEMIBOLD = "font-semibold", _("Semi bold")
    BOLD = "font-bold", _("Bold")
    EXTRABOLD = "font-extrabold", _("Extra bold")
    BLACK = "font-black", _("Black")


class FontSizes(TextChoices):
    SM = "text-sm", _("SM")
    MD = "text-md", _("MD")
    LG = "text-lg", _("LG")
    XL = "text-xl", _("XL")
    XL2 = "text-2xl", _("2 XL")
    XL3 = "text-3xl", _("3 XL")
    XL4 = "text-4xl", _("4 XL")
    XL5 = "text-5xl", _("5 XL")
    XL6 = "text-6xl", _("6 XL")
    XL7 = "text-7xl", _("7 XL")
    XL8 = "text-8xl", _("8 XL")
    XL9 = "text-9xl", _("9 XL")

    def dynamic(self, breakpoints=None) -> list[str]:
        """Generate font sizes with breakpoints.

        >>> FontSizes.XL2.dynamic()
        ['text-lg', 'md:text-xl', 'lg:text-2l']
        """
        if breakpoints is None:
            breakpoints = ["md", "lg"]
        if isinstance(breakpoints, str):
            breakpoints = breakpoints.split(",")

        values = list(self.__class__)
        curr: int = values.index(self)
        sizes = [values[max(i, 0)] for i in range(curr - len(breakpoints), curr + 1)]

        smallest = str(sizes.pop(0))
        others = [f"{b}:{s}" for b, s in zip(breakpoints, sizes)]
        return [smallest, *others]


class TextAlign(TextChoices):
    CENTER = "text-center", _("Center")
    JUSTIFY = "text-justify", _("Justify")
    START = "text-start", _("Start")
    END = "text-end", _("End")


class TextDecoration(TextChoices):
    UNDERLINE = "underline", _("Underline")
    OVERLINE = "overline", _("Overline")
    LINE_THROUGH = "line-through", _("Line through")
    NO_UNDERLINE = "no-underline", _("No underline")


class TextTransform(TextChoices):
    UPPERCASE = "uppercase", _("Uppercase")
    LOWERCASE = "lowercase", _("Lowercase")
    CAPITALIZE = "capitalize", _("Capitalize")
    NORMAL_CASE = "normal-case", _("Normal case")


class Lightness(IntegerChoices):
    """https://tailwindcss.com/docs/colors"""

    L50 = 50, "50"
    L100 = 100, "100"
    L200 = 200, "200"
    L300 = 300, "300"
    L400 = 400, "400"
    L500 = 500, "500"
    L600 = 600, "600"
    L700 = 700, "700"
    L800 = 800, "800"
    L900 = 900, "900"
    L950 = 950, "950"

    @classmethod
    def get_default(cls, value):
        if value:
            return cls(int(value))
        return cls.L500


class Colors(TextChoices):
    """https://tailwindcss.com/docs/colors"""

    PRIMARY = "primary", _("Primary")
    SECONDARY = "secondary", _("Secondary")
    WHITE = "white", _("White")
    BLACK = "black", _("Black")
    RED = "red", _("Red")
    ORANGE = "orange", _("Orange")
    AMBER = "amber", _("Amber")
    YELLOW = "yellow", _("Yellow")
    LIME = "lime", _("Lime")
    GREEN = "green", _("Green")
    EMERALD = "emerald", _("Emerald")
    TEAL = "teal", _("Teal")
    CYAN = "cyan", _("Cyan")
    SKY = "sky", _("Sky")
    BLUE = "blue", _("Blue")
    INDIGO = "indigo", _("Indigo")
    VIOLET = "violet", _("Violet")
    PURPLE = "purple", _("Purple")
    FUCHSIA = "fuchsia", _("Fuchsia")
    PINK = "pink", _("Pink")
    ROSE = "rose", _("Rose")
    SLATE = "slate", _("Slate")
    GRAY = "gray", _("Gray")
    ZINC = "zinc", _("Zinc")
    NEUTRAL = "neutral", _("Neutral")
    STONE = "stone", _("Stone")
    TAUPE = "taupe", _("Taupe")
    MAUVE = "mauve", _("Mauve")
    MIST = "mist", _("Mist")
    OLIVE = "olive", _("Olive")

    @classmethod
    def absolute_colors(cls):
        return [cls.PRIMARY, cls.SECONDARY, cls.WHITE, cls.BLACK]

    @property
    def is_absolute(self):
        return self in self.absolute_colors()

    def display(self, obj: str, lightness: Lightness | None, opacity=None):
        assert obj in ("border", "bg", "text")
        lightness = Lightness.get_default(lightness)
        opacity = f"/{opacity}" if opacity else ""
        return (
            f"{obj}-{self}{opacity}"
            if self.is_absolute
            else f"{obj}-{self}-{lightness}{opacity}"
        )


class Widths(TextChoices):
    """https://tailwindcss.com/docs/colors"""

    W1 = "w-1/12", _("1/12")
    W2 = "w-1/6", _("2/12")
    W3 = "w-1/4", _("3/12")
    W4 = "w-1/3", _("4/12")
    W5 = "w-5/12", _("5/12")
    W6 = "w-1/2", _("6/12")
    W7 = "w-7/12", _("7/12")
    W8 = "w-2/3", _("8/12")
    W9 = "w-3/4", _("9/12")
    W10 = "w-5/6", _("10/12")
    W11 = "w-11/12", _("11/12")
    W12 = "w-full", _("12/12")

    @classmethod
    def display(cls, widths: dict[str, Self]):
        classes = []
        if default_value := widths.pop("", False):
            classes += [str(default_value)]
        classes.extend(f"{size}:{value}" for size, value in widths.items())
        return " ".join(classes).strip()


class BackgroundPosition(TextChoices):
    TOP_LEFT = "bg-top-left", _("Top left")
    TOP = "bg-top", _("Top")
    TOP_RIGHT = "bg-top-right", _("Top right")
    LEFT = "bg-left", _("Left")
    CENTER = "bg-center", _("Center")
    RIGHT = "bg-right", _("Right")
    BOTTOM_LEFT = "bg-bottom-left", _("Bottom left")
    BOTTOM = "bg-bottom", _("Bottom")
    BOTTOM_RIGHT = "bg-bottom-right", _("Bottom right")


class BackgroundRepeat(TextChoices):
    REPEAT = "bg-repeat", _("Repeat")
    REPEAT_X = "bg-repeat-x", _("X")
    REPEAT_Y = "bg-repeat-y", _("Y")
    REPEAT_SPACE = "bg-repeat-space", _("Space")
    REPEAT_ROUND = "bg-repeat-round", _("Round")
    NO_REPEAT = "bg-no-repeat", _("No repeat")


class BackgroundSize(TextChoices):
    AUTO = "bg-auto", _("Auto")
    COVER = "bg-cover", _("Cover")
    CONTAIN = "bg-contain", _("Contain")


class PaddingTop(TextChoices):
    PT80 = "pt-[80px]", _("80px")
    PT110 = "pt-[110px] max-2xl:!pt-[70px]", _("110px")
    PT130 = "pt-[130px] max-2xl:!pt-[90px]", _("130px")
    PT140 = "pt-[140px] max-2xl:!pt-[100px]", _("140px")
    PT155 = "pt-[155px] max-2xl:!pt-[100px]", _("155px")
    PT200 = "pt-[200px]", _("200px")


class PaddingBottom(TextChoices):
    PB80 = "pb-[80px]", _("80px")
    PB110 = "pb-[110px] max-2xl:!pb-[70px]", _("110px")
    PB130 = "pb-[130px] max-2xl:!pb-[90px]", _("130px")
    PB140 = "pb-[140px] max-2xl:!pb-[100px]", _("140px")
    PB155 = "pb-[155px] max-2xl:!pb-[100px]", _("155px")
    PB200 = "pb-[200px]", _("200px")
