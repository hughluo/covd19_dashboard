# covid19_dashboard

Powered by [Dash](https://dash.plotly.com/)

Screenshot

![Screenshot](/screenshot.png?raw=true "Screenshot")


## TODOS
for cases, tests, deaths:
* increase_rate(event_time) = (num_today - num_yesterday) / num_yesterday 
* avg_increase_rate_after_event(event_time) = avg(increase_rate(origin to today))
* avg_increase_rate_before_event(event_time) = avg(increase_rate(origin to today))

