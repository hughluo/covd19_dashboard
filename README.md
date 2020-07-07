# covid19_dashboard

Powered by [Dash](https://dash.plotly.com/) (React + Flask)

* Load csv from s3 into pandas DataFrame
* Dataframe transformation
* Use Dash to illustrate transformed DataFrame
* Package into a docker image

## Get started
```
docker build --tag covid19dashboard:1.0 .
docker run --publish 8050:8050 covid19dashboard:1.0
```
Check it out in web browser: http://localhost:8050/

## Screenshot

![Screenshot](/screenshot.png?raw=true "Screenshot")


