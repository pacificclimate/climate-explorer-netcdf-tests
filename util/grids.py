import datetime

# Approximate representation of PRISM 400m grid
bc_400m = {'lon': {'start': -140, 'step': 0.008333333, 'count': 1680 },
           'lat': {'start': 48, 'step': 0.008333333, 'count': 3241 } }

# Approximate representation of BCSD/BCCAQ grid
canada_5k = {'lon': {'start': -141, 'step': 0.08333333, 'count': 1068 },
             'lat': {'start': 41, 'step': 0.08333333, 'count': 510 } }

# Approximate representation of high res CMIP5 (MIROC5) grid
world_125k = {'lon': {'start': 0, 'step': 1.40625, 'count': 256 },
             'lat': {'start': -89.296875, 'step': 1.40625, 'count': 128 } }

# Approximate representation of standard CMIP5 (CanESM) grid
world_250k = {'lon': {'start': 0, 'step': 2.8125, 'count': 128 },
             'lat': {'start': -88.59375, 'step': 2.8125, 'count': 64 } }

# Timescales
start_day = datetime.date(1950,1,1)
end_day = datetime.date(2100,1,1)
timescales = {'seasonal': range(17), # the seasonal index
              'annual': range(1950, 2100), # the year
              'monthly': range(12 * 150), # months since January 1950
              'daily':range((end_day - start_day).days)} # days since January 1, 1950