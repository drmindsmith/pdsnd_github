#Bikeshare project
"""This script gives the user access to bikeshare data from three cities, which can be sorted and returned with high-level stats and raw data."""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhat city are you interested in? Choose Chicago, New York City, or Washington:")
        if city.lower() not in CITY_DATA:
            print("\nWhat was that? You have to pick one of the three cities, bro.")
            continue
        else:
            print("\nAwesome, I can get info for {}.\n".format(city.title()))
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWould like like to filter by month? I have information from January through June. \n \n If you want to filter, type the month. If not, type 'all':")
        months = ('January', 'February', 'March', 'April', 'May', 'June', 'all')
        if month.lower() == 'all':
            print("\nAwesome-sauce - I won't use a month filter.")
            break
        elif month.title() in ('January', 'February', 'March', 'April', 'May', 'June'):
            print("\nSure thing - I'll filter by {}".format(month.title()))
            break
        elif month.title() not in months:
            print("\nSorry - I didn't catch that. Please try again\n")
            continue
        break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(print("\nWould you like to filter by a day of the week?\nIf so, type the day.\nIf not, type all"))
        if day.lower() == 'all':
            print("\nSure thing - I won't use a day-of-the-week filter.")
            break
        elif day.title() not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            print("\nSorry - could you try that again?")
            continue
        else:
            print("\nKiller - I'll get data for {}".format(day.title()))
        break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day.title())
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month for Bikeshare(tm) usage is: {}".format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print("The most common day of the week for usage is: {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print("The most common hour for a trip to start is: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common station for a trip to start is: {}".format(df['Start Station'].mode()[0]))


    # TO DO: display most commonly used end station
    print("The most common ending station for a trip: {}".format(df['End Station'].mode()[0]))


    # TO DO: display most frequent combination of start station and end station trip
    most_common_station_combo = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print("The most common station combination for a trip is starting at {} and ending at {}".format(((most_common_station_combo.index[0])[0]),((most_common_station_combo.index[0])[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total time spent on all trips was: {}".format(df['Trip Duration'].sum()))


    # TO DO: display mean travel time
    print("The average trip lasted {} minutes.".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The counts of various user types are in the table below:\n{}".format(df['User Type'].value_counts()))

    # TO DO: Display counts of gender
    try:
        print("The number of men and women who used bikeshare are:\n{}".format(df['Gender'].value_counts()))
    except:
        print("Washington has no data for gender, so I can't get you that information.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print("The oldest user was born in {}.".format(int(df['Birth Year'].min())))
        print("The youngest user was born in {}.".format(int(df['Birth Year'].max())))
        print("The most common birth year for all users was {}.".format(int(df['Birth Year'].mode())))
    except:
        print("Washington also has no information on age of users. Sorry - bad data collection!")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_five(df):
    """Gives users the option to display five lines of raw data at  time"""
    start_loc = 0
    i = input("\nWould you like to see five lines of raw data? Enter yes or no: ")
    i = i.lower()
    while i=="yes":
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc += 5
        i = input("\nWould you like to see five more lines of data? Enter yes or no: ")
        i = i.lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_five(df)

        restart = input('\nWould you like to restart? Enter yes or no.')
        if restart.lower() != 'yes':
            print("Thanks for working with me!")
            break

if __name__ == "__main__":

    main()
