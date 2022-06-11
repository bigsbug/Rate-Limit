"""Offers Some Limiters and Limiter Creators
"""

from django.conf import settings

from rate_limit.exceptions import InvalidConfig
from rate_limit.load_config import LimitBy, LoadKeyPerfix, TimeLimit
from rate_limit.tools import get_ip
from rate_limit.db_manager_interfaces import (
    PerformActionDBInterface,
    RateLimiterInterface,
)


class BaseRateLimit(RateLimiterInterface):
    """Base Class For Creating New Limiters,
    Providing Some Of Common Base Method For Limiters

    Args:
        RateLimiterInterface (interface): Interface of Limiters
    """

    def __init__(self, max_rate, time) -> None:
        self.max_rate_count = int(max_rate)
        self.time = time

    def set_db(self, performer_action_db: PerformActionDBInterface):
        """Setting A Performer DB To Interacting With DataBase

        Args:
            performer_action_db (PerformActionDBInterface): get a Perform Action DB Interface instance
        """
        self.performer_action_db = performer_action_db

    @property
    def max_rate(self):
        """Return Max Rate Allowd For Limiter

        Returns:
            Int : Max Rate Allowd For This Limiter
        """
        return self.max_rate_count

    def expireing(self, key):
        """Expiring A Unique Key From Database After A Period Time Based Specified Time In Settings

        Args:
            key (Any): Unique Key For Detecting Which Data Should Be Expire

        Raises:
            InvalidConfig: The Time Limited in Settings Specified Is Incorrect
        """

        try:
            time = TimeLimit[str.upper(self.time)].value
        except KeyError:
            raise InvalidConfig("The time of rate limit is incorrect")

        ttl = self.performer_action_db.show_ttl(key)
        if ttl < 0:
            self.performer_action_db.set_expire(key, time)


class RateLimitUser(BaseRateLimit):
    def __init__(self, max_rate=None, time="min") -> None:
        if max_rate == None:
            max_rate, time = LimitBy(settings, ["user"]).extract_config()
        super().__init__(max_rate, time)

    def get_rate(self, request):
        user = request.user
        if not user.is_anonymous:
            key = f"user:{user.username}"
            count = self.performer_action_db.show_view(key)
            return count
        return 0

    def new_view(self, request):
        user = request.user
        if not user.is_anonymous:
            key = f"user:{user.username}"
            count = self.performer_action_db.new_view(key)
            self.expireing(key)
            return count


class RateLimitAnonymous(BaseRateLimit):
    def __init__(self, max_rate=None, time="min") -> None:
        if max_rate == None:
            max_rate, time = LimitBy(settings, ["anonymous"]).extract_config()
        super().__init__(max_rate, time)

    def get_rate(self, request):
        user = request.user
        ip = get_ip(request)
        if user.is_anonymous:
            key = f"anonymous:{ip}"
            count = self.performer_action_db.show_view(key)
            self.expireing(key)
            return count
        return 0

    def new_view(self, request):
        user = request.user
        ip = get_ip(request)
        if user.is_anonymous:
            key = f"anonymous:{ip}"
            count = self.performer_action_db.new_view(key)
            self.expireing(key)
            return count


class RateLimitIP(BaseRateLimit):
    def __init__(self, max_rate=None, time="min") -> None:
        if max_rate == None:
            max_rate, time = LimitBy(settings, ["ip"]).extract_config()
        super().__init__(max_rate, time)

    def get_rate(self, request):
        ip = get_ip(request)

        key = f"ip:{ip}"
        count = self.performer_action_db.show_view(key)
        return count

    def new_view(self, request):
        ip = get_ip(request)
        key = f"ip:{ip}"
        print(key)
        count = self.performer_action_db.new_view(key)
        self.expireing(key)
        return count
