# 538monitor
## Automated email alerts for movement of electoral forecasts by 538

This script was cooked up to help avoid checking the [fivethirtyeight](https://fivethirtyeight.com/) forecast every five seconds and to sooth some friends' anxiety during the 2020 US election.  Its obviously not as useful at the time its being posted here but it can serve as a template for future election monitoring as minimal changes would be needed monitor other races, and probably only one or two changes for the next US presidential elecition.

Usage is pretty simple, just set your preferred winner, your email address(es), an [oauth file for yagmail](https://yagmail.readthedocs.io/en/latest/setup.html#using-oauth2) to authenticate with, and schedule it to run at your desired intervals.  It'll create the required file for tracking on its first run, and it'll print a status update on each run if you want to ouput the results to a log.  If you wanted to track changes over time in a more elegant manner this could be adjusted to append the results of each update to the csv file rather than overwriting them but I wasn't concerned with that, just wanted email alerts.  

Updates were only intended to be emailed when the race moves in your preferred direction, but in some cases you will get alerts that show your candidate's odds have gone down if their opponent's odds go down at the same time (typically when the odds of a tie expand).  This could be resolved by splitting the candidate's odds to be handled separately rather than as a fixed pair but the election had ended by the time I had time to resolve that oversight so it's on the docket for the next one.
