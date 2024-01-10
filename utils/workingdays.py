import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

def n_business_days_earlier(n):
    # Define U.S. business day calendar (excluding weekends and federal holidays)
    us_business_day = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    
    # Get today's date
    current_date = pd.Timestamp.now().normalize()
    
    # Calculate the date n U.S. business days earlier
    n_business_days_earlier_date = current_date - n * us_business_day
    
    # Return the resulting date
    return n_business_days_earlier_date

def previous_n_business_days(n):
    # Define U.S. business day calendar (excluding weekends and federal holidays)
    us_business_day = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    
    # Get today's date
    current_date = pd.Timestamp.now().normalize()
    
    # Generate the previous n U.S. business days
    business_days = [current_date - i * us_business_day for i in range(1, n+1)]
    
    # Return the list of dates
    return business_days

def next_n_business_days(n):
    # Define U.S. business day calendar (excluding weekends and federal holidays)
    us_business_day = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    
    # Get today's date
    current_date = pd.Timestamp.now().normalize()
    
    # Generate the previous n U.S. business days
    business_days = [current_date + i * us_business_day for i in range(1, n+1)]
    
    # Return the list of dates
    return business_days

if __name__ == '__main__':
    print(n_business_days_earlier(10))
    print(previous_n_business_days(10)[-1])



