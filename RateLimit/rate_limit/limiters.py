from rate_limit.db_manager_interfaces import RateLimiterInterface

from rate_limit.load_config import LimitBy, LoadKeyPerfix

from django.conf import settings

from rate_limit.tools import get_ip


class BaseRateLimit(RateLimiterInterface):
    def __init__(self, max_rate=None, time="min", type_limit="") -> None:

        self.type_limit = type_limit
        self.load_config()
        #  if specify a new rate limit then should select a time for limiting access
        if max_rate:
            self.max_rate_count = max_rate
            self.time = time

    def load_config(self):
        self.max_rate_count, self.time = LimitBy(
            settings, [self.type_limit]
        ).extract_config()
        self.max_rate_count = int(self.max_rate_count)

    def set_db(self, performer_action_db):
        self.performer_action_db = performer_action_db

    @property
    def max_rate(self):
        return self.max_rate_count

    def expireing(self, key):
        MIN_SEC = 60
        HOURS_SEC = MIN_SEC * 60
        DAY_SEC = HOURS_SEC * 24
        MONTH_SEC = DAY_SEC * 30
        YEAR_SEC = MONTH_SEC * 12
        if self.time == "min":
            self.time = MIN_SEC
        elif self.time == "hours":
            self.time = HOURS_SEC
        elif self.time == "day":
            self.time = DAY_SEC
        elif self.time == "month":
            self.time = MONTH_SEC
        elif self.time == "year":
            self.time = YEAR_SEC
        # else:
        #     self.time = 0
        ttl = self.performer_action_db.show_ttl(key)
        print("ttl", ttl)

        if ttl < 0:
            self.performer_action_db.set_expire(key, self.time)


class RateLimitUser(BaseRateLimit):
    def __init__(self, max_rate=None, time="min", type_limit="user") -> None:

        super().__init__(max_rate, time, type_limit)

    def get_rate(self, request):
        user = request.user
        if not user.is_anonymous:
            key = f"{self.type_limit}:{user.username}"
            count = self.performer_action_db.show_view(key)
            return count
        return 0

    def new_view(self, request):
        user = request.user
        if not user.is_anonymous:
            key = f"{self.type_limit}:{user.username}"
            count = self.performer_action_db.new_view(key)
            self.expireing(key)
            return count


class RateLimitAnonymous(BaseRateLimit):
    def __init__(self, max_rate=None, time="min", type_limit="anonymous") -> None:
        super().__init__(max_rate, time, type_limit)

    def get_rate(self, request):
        user = request.user
        ip = get_ip(request)
        if user.is_anonymous:
            key = f"{self.type_limit}:{ip}"
            count = self.performer_action_db.show_view(key)
            self.expireing(key)
            return count
        return 0

    def new_view(self, request):
        user = request.user
        ip = get_ip(request)
        if user.is_anonymous:
            key = f"{self.type_limit}:{ip}"
            count = self.performer_action_db.new_view(key)
            self.expireing(key)
            return count


class RateLimitIP(BaseRateLimit):
    def __init__(self, max_rate=None, time="min", type_limit="ip") -> None:
        super().__init__(max_rate, time, type_limit)

    def get_rate(self, request):
        ip = get_ip(request)

        key = f"{self.type_limit}:{ip}"
        count = self.performer_action_db.show_view(key)
        return count

    def new_view(self, request):
        ip = get_ip(request)
        key = f"{self.type_limit}:{ip}"
        print(key)
        count = self.performer_action_db.new_view(key)
        self.expireing(key)
        return count
