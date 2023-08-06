import requests

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from operator import itemgetter


class Contributions:
    def __init__(self, username):
        url = f"https://github.com/users/{username}/contributions"
        r = requests.get(url)
        self.contributions_soup = BeautifulSoup(r.text, "html.parser")

    def total(self):
        """Return the total contributions in the last year."""
        # Find the h2 title text that contains the total contributions.
        title = self.contributions_soup.find("h2").text

        # Extracting the number from the title.
        return int(title.strip().split("contributions")[0].strip().replace(",", ""))

    def daily(self):
        """
        Return a list of tuples, each with the format (date, number_contributions_on_date). The list has an element
        for each day in the last year.
        """
        days = self.contributions_soup.find_all("rect", class_="day")

        dates = [datetime.strptime(day["data-date"], "%Y-%m-%d").date() for day in days]
        number_contributions = [int(day["data-count"]) for day in days]

        return list(zip(dates, number_contributions))

    @staticmethod
    def current_streak(daily_contributions):
        """
        Return the length of the current commit streak as well as the two dates specifying the period.
        The output is a three-tuple with the format (streak_length, from, to). If the user is not on a streak then
        from and to will be None.
        """
        reversed_daily_contributions = daily_contributions[::-1]

        to_date = None
        from_date = None
        streak_counter = 0

        current_day = reversed_daily_contributions.pop(0)
        # If the user is currently on a streak then find out when the streak started.
        if current_day[1] > 0:
            to_date = current_day[0]
            streak_counter += 1
            for day in reversed_daily_contributions:
                if day[1] > 0:
                    streak_counter += 1
                else:
                    from_date = day[0] + timedelta(days=1)
                    break

        return streak_counter, from_date, to_date

    @staticmethod
    def longest_streak(daily_contributions):
        """
        Return the length of the longest commit streak as well as the two dates specifying the period.
        The output is a three-tuple with the format (streak_length, from, to). If the user has never committed then
        from and to will be None.
        """
        streaks = []
        from_date = None
        streak_counter = 0

        # Iterate through days to find all streaks of length at least 1.
        for day in daily_contributions:
            if day[1] > 0:
                # If there is an active streak at this date.
                if from_date:
                    streak_counter += 1
                else:
                    # Start a new streak.
                    from_date = day[0]
                    streak_counter += 1
            else:
                # If a streak is ending.
                if from_date:
                    streaks.append((streak_counter, from_date, day[0] - timedelta(days=1)))
                    from_date = None
                    streak_counter = 0

        # If the user has a currently active streak then add it.
        if from_date:
            streaks.append((streak_counter, from_date, datetime.today().date()))

        # Return the longest streak, if any exist.
        return max(streaks, key=itemgetter(0))
