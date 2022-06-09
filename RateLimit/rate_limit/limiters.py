from rate_limit.exceptions import InvalidConfig
from rate_limit.db_manager_interfaces import RateLimiterInterface

from rate_limit.load_config import LimitBy, LoadKeyPerfix, TimeLimit

from django.conf import settings

from rate_limit.tools import get_ip
from rate_limit.db_manager_interfaces import PerformActionDBInterface


class BaseRateLimit(RateLimiterInterface):
    """Base Class For Creating New Limiters,
    Providing Some Of Common Base Method For Limiters

    Args:
        RateLimiterInterface (interface): Interface of Limiters
    """

    def __init__(self, max_rate=None, time="min", type_limit="") -> None:
        self.type_limit = type_limit
        self.load_config()
        #  if specify a new rate limit then should select a time for limiting access
        if max_rate:
            self.max_rate_count = max_rate
            self.time = time

    def load_config(self):
        """Load Max Rate and Time Limit From Settings"""
        self.max_rate_count, self.time = LimitBy(
            settings, [self.type_limit]
        ).extract_config()
        self.max_rate_count = int(self.max_rate_count)

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
