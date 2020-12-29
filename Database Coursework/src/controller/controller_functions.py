from datetime import *
from ..model.DBModel import DBModel
import matplotlib.pyplot as plt
from ..storage.tables import Wind, Weather, Snow, Indicators, Metrics, Forecast, City, Clouds, Rain, AirPollution
import numpy as np


def get_password():
    f = open(r"D:\Job\Apps\password.txt", "r")
    data = f.read()
    f.close()
    return data


password = get_password()
dbModel = DBModel('Coursework', 'postgres', password, 'localhost:5432')
PLOT_LABEL_FONT_SIZE = 14
PLOT_MEANING_FONT_SIZE = 6


def get_weather_list_by_date(city_name, date_):
    metrics = dbModel.do_request("Select * from metrics")
    wind = dbModel.do_request("Select * from wind")
    rain = dbModel.do_request("Select * from rain")
    clouds = dbModel.do_request("Select * from clouds")
    snow = dbModel.do_request("Select * from snow")
    cities = dbModel.do_request("Select * from city")
    weather = dbModel.do_request("Select * from weather")

    result_list = {}

    city_id = None
    for city in cities:
        if city.name == city_name:
            city_id = city.id
            break
    if city_id is None:
        result_list['error'] = "City not found"
        return result_list

    hours_delta = timedelta(hours=4)
    weather_id = None
    for w in weather:
        if w.city_id == city_id:
            if date_ + hours_delta >= w.timestap >= date_ - hours_delta:
                result_list['desc'] = w.description
                weather_id = w.id
    if weather_id is None:
        result_list['error'] = "No data about weather at this time found"
        return result_list

    for m in metrics:
        if m.weather_id == weather_id:
            result_list['temp'] = m.temp
            result_list['feels_like'] = m.feels_like
            result_list['humidity'] = m.humidity
            break

    for w in wind:
        if w.weather_id == weather_id:
            result_list['wind_speed'] = w.speed
            break
    if 'wind_speed' not in result_list:
        result_list['wind_speed'] = None

    for cl in clouds:
        if cl.weather_id == weather_id:
            result_list['cloudiness'] = cl.cloudiness
            break
    if 'cloudiness' not in result_list:
        result_list['cloudiness'] = None

    for r in rain:
        if r.weather_id == weather_id:
            result_list['rain'] = r.volume_hour
            break
    if 'rain' not in result_list:
        result_list['rain'] = None

    for s in snow:
        if s.weather_id == weather_id:
            result_list['snow'] = s.volume_hour
            break
    if 'snow' not in result_list:
        result_list['snow'] = None

    return result_list


def get_forecast_list_by_date(date_chosen, city_name):
    cities = dbModel.do_request("Select * from city")
    forecast = dbModel.do_request("Select * from forecast")
    indicators = dbModel.do_request("Select * from indicators")

    result_list = {}

    city_id = None
    for city in cities:
        if city.name == city_name:
            city_id = city.id
            break
    if city_id is None:
        result_list['error'] = "City not found"
        return result_list

    hours_delta = timedelta(hours=4)
    forecast_id = None
    for f in forecast:
        if f.city_id == city_id:
            if date_chosen + hours_delta >= f.timestap >= date_chosen - hours_delta:
                result_list['desc'] = f.description
                forecast_id = f.id
                break
    if forecast_id is None:
        result_list['error'] = "No data about forecast at this time found"
        return result_list

    for i in indicators:
        if i.forecast_id == forecast_id:
            result_list['temp_max'] = i.temp_max
            result_list['temp_min'] = i.temp_min
            result_list['cloudiness'] = i.cloudiness
            result_list['wind_speed'] = i.wind_speed
            result_list['pop'] = i.pop
            break

    return result_list


def get_ap_by_date(date_, city_name):
    cities = dbModel.do_request("Select * from city")
    ap = dbModel.do_request("Select * from air_pollution")

    result_list = {}

    city_id = None
    for city in cities:
        if city.name == city_name:
            city_id = city.id
            break
    if city_id is None:
        result_list['error'] = "City not found"
        return result_list

    hours_delta = timedelta(hours=23, minutes=59, seconds=59)
    for a in ap:
        if a.city_id == city_id:
            if date_ <= a.timestap <= date_ + hours_delta:
                result_list['aqi'] = a.aqi
                result_list['comp_CO'] = a.comp_CO
                result_list['comp_NO'] = a.comp_NO
                result_list['comp_NO2'] = a.comp_NO2
                break
    if 'aqi' not in result_list:
        result_list['error'] = "Data not found"

    return result_list


def get_colors(n):
    colors = []
    cm = plt.cm.get_cmap('hsv', n)
    for i in np.arange(n):
        colors.append(cm(i))
    return colors


def has_city_name(data_list, city_name):
    for d in data_list:
        if d['city_name'] == city_name:
            return True
    return False


def get_hottest_cities(date_chosen):
    hours_delta = timedelta(hours=23, minutes=59, seconds=59)
    date_to = date_chosen + hours_delta
    dataset = dbModel.do_request("""with weather_city as (select weather.id as weather_id, city."name" as city_name,
    timestap from weather inner join city on city.id = weather.city_id
    where timestap > '{}' and timestap < '{}' order by "name"),
    metrics_city as (select * from metrics inner join weather_city on metrics.weather_id = weather_city.weather_id)
    select "temp", city_name from metrics_city order by "temp" desc""".format(date_chosen, date_to))

    result = []
    count = 0
    for data in dataset:
        if count == 10:
            break
        if not has_city_name(result, data.city_name):
            result.append({'city_name': data.city_name, 'temp': data.temp})
            count += 1

    names = []
    temps = []
    for r in result:
        names.append(r['city_name'])
        temps.append(r['temp'])

    plt.title('Cities with highest temperature for {}'.format(datetime.strftime(date_chosen, "%Y-%m-%d")),
              fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(names, temps, color=get_colors(len(names)))
    plt.ylabel('Temperatures', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.xticks(rotation=90, fontsize=PLOT_MEANING_FONT_SIZE)
    plt.show()


def get_highest_wind_cities(date_chosen):
    hours_delta = timedelta(hours=23, minutes=59, seconds=59)
    date_to = date_chosen + hours_delta
    dataset = dbModel.do_request("""with weather_city as (select weather.id as weather_id, city."name" as city_name,
                    timestap from weather inner join city on city.id = weather.city_id
                    where timestap > '{}' and timestap < '{}' order by "name"),
                wind_city as (select * from wind inner join weather_city on wind.weather_id = weather_city.weather_id)
                    select speed, city_name from wind_city order by speed desc""".format(date_chosen, date_to))

    if len(dataset) == 0:
        return "No data found"
    result = []
    count = 0
    for data in dataset:
        if count == 10:
            break
        if not has_city_name(result, data.city_name):
            result.append({'city_name': data.city_name, 'speed': data.speed})
            count += 1

    names = []
    temps = []
    for r in result:
        names.append(r['city_name'])
        temps.append(r['speed'])

    plt.title('Cities with highest wind speed for {}'.format(datetime.strftime(date_chosen, "%Y-%m-%d")),
              fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(names, temps, color=get_colors(len(names)))
    plt.ylabel('Wind speed in m/s', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.xticks(rotation=90, fontsize=PLOT_MEANING_FONT_SIZE)
    plt.show()


def get_highest_cloud_cities(date_chosen):
    hours_delta = timedelta(hours=23, minutes=59, seconds=59)
    date_to = date_chosen + hours_delta
    dataset = dbModel.do_request("""with weather_city as (select weather.id as weather_id, city."name" as city_name, 
    timestap from weather inner join city on city.id = weather.city_id
    where timestap > '{}' and timestap < '{}' order by "name"),
    clouds_city as (select * from clouds inner join weather_city on clouds.weather_id = weather_city.weather_id)
    select cloudiness, city_name from clouds_city order by cloudiness desc""".format(date_chosen, date_to))

    if len(dataset) == 0:
        return "No data found"
    result = []
    count = 0
    for data in dataset:
        if count == 10:
            break
        if not has_city_name(result, data.city_name):
            result.append({'city_name': data.city_name, 'cloudiness': data.cloudiness})
            count += 1

    names = []
    temps = []
    for r in result:
        names.append(r['city_name'])
        temps.append(r['cloudiness'])

    plt.title('cities with highest cloudiness level for {}'.format(datetime.strftime(date_chosen, "%Y-%m-%d")),
              fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(names, temps, color=get_colors(len(names)))
    plt.ylabel('Cloudiness in %', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.xticks(rotation=90, fontsize=PLOT_MEANING_FONT_SIZE)
    plt.show()


def get_cities_highest_pop(date_chosen):
    hours_delta = timedelta(hours=23, minutes=59, seconds=59)
    date_to = date_chosen + hours_delta
    dataset = dbModel.do_request("""with forecast_city as (select forecast.id as forecast_id, city."name" as city_name, 
    timestap from forecast inner join city on city.id = forecast.city_id 
    where timestap > '{}' and timestap < '{}' order by "name"),
    forecast_indicators as (select * from indicators inner join 
    forecast_city on indicators.forecast_id = forecast_city.forecast_id)
    select pop, city_name from forecast_indicators order by pop desc""".format(date_chosen, date_to))

    if len(dataset) == 0:
        return "No data found"
    result = []
    count = 0
    for data in dataset:
        if count == 10:
            break
        if not has_city_name(result, data.city_name):
            result.append({'city_name': data.city_name, 'pop': data.pop})
            count += 1

    names = []
    temps = []
    for r in result:
        names.append(r['city_name'])
        temps.append(r['pop'])

    plt.title('Forecasts with highest probability of precipitation during {}'
              .format(datetime.strftime(date_chosen, "%Y-%m-%d")),
              fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(names, temps, color=get_colors(len(names)))
    plt.ylabel('Probability of precipitation (*100%)', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.xticks(rotation=90, fontsize=PLOT_MEANING_FONT_SIZE)
    plt.show()


def get_cities_highest_air_pollution(date_chosen):
    hours_delta = timedelta(hours=23, minutes=59, seconds=59)
    date_to = date_chosen + hours_delta
    dataset = dbModel.do_request("""with air_pollution_city as (select air_pollution.id as ap_id,
     city."name" as city_name, timestap, "comp_NO2" from air_pollution
    inner join city on city.id = air_pollution.city_id where timestap > '{}' and timestap < '{}' order by "name")
    select * from air_pollution_city order by "comp_NO2" desc""".format(date_chosen, date_to))

    if len(dataset) == 0:
        return "No data found"
    result = []
    count = 0
    for data in dataset:
        if count == 10:
            break
        if not has_city_name(result, data.city_name):
            result.append({'city_name': data.city_name, 'comp_NO2': data.comp_NO2})
            count += 1

    names = []
    temps = []
    for r in result:
        names.append(r['city_name'])
        temps.append(r['comp_NO2'])

    plt.title('Cities that contain highest NO2 component for {}'
              .format(datetime.strftime(date_chosen, "%Y-%m-%d")),
              fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(names, temps, color=get_colors(len(names)))
    plt.ylabel('NO2 component (μg/m3)', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.xticks(rotation=90, fontsize=PLOT_MEANING_FONT_SIZE)
    plt.show()
