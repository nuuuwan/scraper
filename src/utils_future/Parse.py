from dateutil import parser


class Parse:
    TIME_FORMAT = "%Y-%m-%d %H:%M"

    @staticmethod
    def time_str(x) -> str:
        dt = parser.parse(x)
        return dt.strftime(Parse.TIME_FORMAT)

    @staticmethod
    def badge(x) -> str:
        for before, after in [("-", "--"), (" ", "_")]:
            x = x.replace(before, after)
        return x
