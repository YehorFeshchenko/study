from sqlalchemy import Column, Integer, ForeignKey, Text, Time, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    api_city_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    children1 = relationship('Weather')
    children2 = relationship('AirPollution')
    children3 = relationship('Forecast')

    def __init__(self, api_city_id, name):
        self.api_city_id = api_city_id
        self.name = name


class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    timestap = Column(Time, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    children1 = relationship('Wind')
    children2 = relationship('Metrics')
    children3 = relationship('Clouds')
    children4 = relationship('Rain')
    children5 = relationship('Snow')

    def __init__(self, description, timestap, city_id):
        self.description = description
        self.timestap = timestap
        self.city_id = city_id


class Wind(Base):
    __tablename__ = "wind"
    id = Column(Integer, primary_key=True)
    speed = Column(Integer, nullable=False)
    deg = Column(Integer, nullable=False)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)

    def __init__(self, speed, deg, weather_id):
        self.weather_id = weather_id
        self.speed = speed
        self.deg = deg


class Metrics(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True)
    temp = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp_max = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)

    def __init__(self, temp, temp_min, temp_max, feels_like, humidity, pressure, weather_id):
        self.weather_id = weather_id
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.feels_like = feels_like
        self.humidity = humidity
        self.pressure = pressure


class Rain(Base):
    __tablename__ = "rain"
    id = Column(Integer, primary_key=True)
    volume_hour = Column(Float, nullable=False)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)

    def __init__(self, volume_hour, weather_id):
        self.weather_id = weather_id
        self.volume_hour = volume_hour


class Clouds(Base):
    __tablename__ = "clouds"
    id = Column(Integer, primary_key=True)
    cloudiness = Column(Integer, nullable=False)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)

    def __init__(self, cloudiness, weather_id):
        self.weather_id = weather_id
        self.cloudiness = cloudiness


class Snow(Base):
    __tablename__ = "snow"
    id = Column(Integer, primary_key=True)
    volume_hour = Column(Float, nullable=False)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)

    def __init__(self, volume_hour, weather_id):
        self.weather_id = weather_id
        self.volume_hour = volume_hour


class AirPollution(Base):
    __tablename__ = "air_pollution"
    id = Column(Integer, primary_key=True)
    timestap = Column(Time, nullable=False)
    aqi = Column(Integer, nullable=False)
    comp_CO = Column(Float, nullable=False)
    comp_NO = Column(Float, nullable=False)
    comp_NO2 = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)

    def __init__(self, timestap, aqi, comp_CO, comp_NO, comp_NO2,  city_id):
        self.city_id = city_id
        self.timestap = timestap
        self.aqi = aqi
        self.comp_CO = comp_CO
        self.comp_NO = comp_NO
        self.comp_NO2 = comp_NO2


class Forecast(Base):
    __tablename__ = "forecast"
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    timestap = Column(Time, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    children = relationship('Indicators')

    def __init__(self, description, timestap, city_id):
        self.city_id = city_id
        self.timestap = timestap
        self.description = description


class Indicators(Base):
    __tablename__ = "indicators"
    id = Column(Integer, primary_key=True)
    temp_max = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    cloudiness = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    pop = Column(Float, nullable=False)
    forecast_id = Column(Integer, ForeignKey('forecast.id'), nullable=False)

    def __init__(self, temp_max, temp_min, cloudiness, wind_speed, pop, forecast_id):
        self.forecast_id = forecast_id
        self.temp_max = temp_max
        self.temp_min = temp_min
        self.cloudiness = cloudiness
        self.wind_speed = wind_speed
        self.pop = pop
