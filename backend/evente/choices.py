from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class Fonts(TextChoices):
    POPPINS = "poppins", _("Font Poppins")
    UNBOUNDED = "unbounded", _("Font Unbounded")


class TailwindLightness(IntegerChoices):
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


class TailwindColors(TextChoices):
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

    def display(self, obj: str, lightness: TailwindLightness | None):
        assert obj in ("border", "bg", "text")
        lightness = TailwindLightness.get_default(lightness)
        return f"{obj}-{self}" if self.is_absolute else f"{obj}-{self}-{lightness}"


class TailwindWidth(TextChoices):
    """https://tailwindcss.com/docs/colors"""

    W1 = "w-1/12", _("1/12")  # md:-1/12 lg:w-1/12 xl:w-1/12
    W2 = "w-2/12", _("2/12 Sixth")  # md:-2/12 lg:w-2/12 xl:w-2/12
    W3 = "w-3/12", _("3/12 Fourth")  # md:-3/12 lg:w-3/12 xl:w-3/12
    W4 = "w-4/12", _("4/12 Third")  # md:-4/12 lg:w-4/12 xl:w-4/12
    W5 = "w-5/12", _("5/12")  # md:-5/12 lg:w-5/12 xl:w-5/12
    W6 = "w-6/12", _("6/12 Half")  # md:-6/12 lg:w-6/12 xl:w-6/12
    W7 = "w-7/12", _("7/12")  # md:-7/12 lg:w-7/12 xl:w-7/12
    W8 = "w-8/12", _("8/12 Two thirds")  # md:-8/12 lg:w-8/12 xl:w-8/12
    W9 = "w-9/12", _("9/12 Three fourths")  # md:-9/12 lg:w-9/12 xl:w-9/12
    W10 = "w-10/12", _("10/12")  # md:-10/12 lg:w-10/12 xl:w-10/12
    W11 = "w-11/12", _("11/12")  # md:-11/12 lg:w-11/12 xl:w-11/12
    W12 = "w-12/12", _("12/12 Full width")  # md:-12/12 lg:w-12/12 xl:w-12/12


class TailwindBackgroundPosition(TextChoices):
    TOP_LEFT = "bg-top-left", _("Top left")
    TOP = "bg-top", _("Top")
    TOP_RIGHT = "bg-top-right", _("Top right")
    LEFT = "bg-left", _("Left")
    CENTER = "bg-center", _("Center")
    RIGHT = "bg-right", _("Right")
    BOTTOM_LEFT = "bg-bottom-left", _("Bottom left")
    BOTTOM = "bg-bottom", _("Bottom")
    BOTTOM_RIGHT = "bg-bottom-right", _("Bottom right")


class TailwindBackgroundRepeat(TextChoices):
    REPEAT = "bg-repeat", _("Repeat")
    REPEAT_X = "bg-repeat-x", _("X")
    REPEAT_Y = "bg-repeat-y", _("Y")
    REPEAT_SPACE = "bg-repeat-space", _("Space")
    REPEAT_ROUND = "bg-repeat-round", _("Round")
    NO_REPEAT = "bg-no-repeat", _("No repeat")


class TailwindBackgroundSize(TextChoices):
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


class Flaticons(TextChoices):
    ACCOUNT = "flaticon-account", _("Account")
    ANNOUNCEMENT = "flaticon-announcement", _("Announcement")
    CALENDAR = "flaticon-calendar", _("Calendar")
    CHAT_BOX = "flaticon-chat-box", _("Chat box")
    DEAL = "flaticon-deal", _("Deal")
    FASTFOOD = "flaticon-fastfood", _("Fastfood")
    GPS = "flaticon-gps", _("GPS")
    HANDSHAKE = "flaticon-handshake", _("Handshake")
    MAIL = "flaticon-mail", _("Mail")
    MEETING = "flaticon-meeting", _("Meeting")
    MEGAPHONE = "flaticon-megaphone", _("Megaphone")
    PHONE = "flaticon-phone", _("Phone")
    PLUS = "flaticon-plus", _("Plus")
    PUZZLE = "flaticon-puzzle", _("Puzzle")
    REQUEST = "flaticon-request", _("Request")
    SEARCH = "flaticon-search", _("Search")
    SHARE = "flaticon-share", _("Share")
    SHOPPING_CART = "flaticon-shopping-cart", _("Shopping cart")
    SPEAKER = "flaticon-speaker", _("Speaker")
    SURPRISE = "flaticon-surprise", _("Surprise")
    TEAMWORK = "flaticon-teamwork", _("Teamwork")
    TEAMWORK_1 = "flaticon-teamwork-1", _("Teamwork 1")
    TEAMWORK_2 = "flaticon-teamwork-2", _("Teamwork 2")
    TIME = "flaticon-time", _("Time")
    UP_RIGHT_ARROW = "flaticon-up-right-arrow", _("Up right arrow")
    UP_RIGHT_ARROW_1 = "flaticon-up-right-arrow-1", _("Up right arrow 1")


class FontAwesomeStyles(TextChoices):
    REGULAR = "fa-regular", _("Regular")
    LIGHT = "fa-light", _("Light")
    BRANDS = "fa-brands", _("Brands")
    SOLID = "fa-solid", _("Solid")


class TimeUnits(TextChoices):
    YEARS = "years", _("Years")
    MONTHS = "months", _("Months")
    WEEKS = "weeks", _("Weeks")
    DAYS = "days", _("Days")
    HOURS = "hours", _("Hours")
    MINUTES = "minutes", _("Minutes")
    SECONDS = "seconds", _("Seconds")

    @property
    def js_sum(self):
        # const sec = Math.floor((start - new Date()) / 1000)
        return {
            self.YEARS: f"sec / {60 * 60 * 24 * 365}",
            self.MONTHS: f"sec / {60 * 60 * 24 * 365 / 12}",
            self.WEEKS: f"sec / {60 * 60 * 24 * 7}",
            self.DAYS: f"sec / {60 * 60 * 24}",
            self.HOURS: f"sec / {60 * 60}",
            self.MINUTES: "sec / 60",
            self.SECONDS: "sec",
        }[self]

    @property
    def js_sum_with_modulo(self):
        return {
            self.YEARS: self.js_sum,
            self.MONTHS: f"({self.js_sum}) % 12",
            self.WEEKS: f"({self.js_sum}) % 51.145",
            self.DAYS: f"({self.js_sum}) % 30.4",
            self.HOURS: f"({self.js_sum}) % 24",
            self.MINUTES: f"({self.js_sum}) % 60",
            self.SECONDS: f"{self.js_sum} % 60",
        }[self]
