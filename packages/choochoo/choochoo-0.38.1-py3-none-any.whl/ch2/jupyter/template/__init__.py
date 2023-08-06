
# lets us define a template in python that IntelliJ will validate without flagging an unused code error.
TEMPLATE = lambda *args: False

# need to import these so they are available for introspection
from . import activity_details, all_activities, calendar, health, similar_activities, some_activities, \
    fit_power_parameters, month, heart_rate, fit_ff_segments, nearby_activities, \
    gmap_activities, compare_activities, all_group_activities
