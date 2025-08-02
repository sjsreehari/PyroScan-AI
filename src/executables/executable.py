from src.tools.fire_data import get_fire_data
from src.agent.desicion_maker import PredictFirePlaces


def executable():
    get_fire_data()
    PredictFirePlaces()
