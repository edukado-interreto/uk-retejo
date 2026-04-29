from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from .tailwind import *  # noqa


class EventeIcons(TextChoices):
    MEETUP = "meetup", _("Meetup")
    HANDSHAKE = "handshake", _("Handshake")
    BRAIN_PUZZLE = "brain_puzzle", _("Brain puzzle")


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
