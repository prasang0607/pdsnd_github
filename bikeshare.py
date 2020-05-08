from os import name, system
from pprint import pprint
import pandas as pd
import time

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def clear_console():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    month = None
    day = None

    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n> ').strip().lower()
        if city not in CITY_DATA:
            print('Please enter a valid city.')
        else:
            break

    while True:
        prompt_msg = 'Would you like to filter data by month, day, both, or not at all? Type "none" for no time filter.\n> '
        filt = input(prompt_msg).strip().lower()
        if filt in ('both', 'month', 'day', 'none'):
            break
        else:
            print('Please enter a valid filter.')
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    if filt in ('both', 'month'):
        while True:
            month = input('Which month? January, February, March, April, May, June.\n> ').strip().lower()
            if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print('Please enter a valid month.')
            else:
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if filt in ('both', 'day'):
        while True:
            day = input(
                'Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Firday, Saturday.\n> ').strip().lower()
            if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
                print('Please enter a valid day.')
            else:
                break

    clear_console()
    print('-' * 40)
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
    print('Reading data and applying filters(if any)...')

    # reading the file
    df = pd.read_csv(CITY_DATA[city], index_col=0)

    # ---- data cleaning and manipulation ----
    # renaming columns for ease
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]

    # changing datatype into required format
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df['start_station'] = df['start_station'].astype('category')
    df['end_station'] = df['end_station'].astype('category')
    df['user_type'] = df['user_type'].astype('category')

    # since we don't have gender and birth year in Washington Dataset, let's limit the operations to remaining datasets
    if city != 'washington':
        df['gender'] = df['gender'].astype('category')

        # birth year column has some NA values, let's fill it and change its datatype as well
        df['birth_year'].fillna(0, inplace=True)
        df['birth_year'] = df['birth_year'].astype(int)

    # deriving new columns for month, day and start hour
    df['day_of_week'] = df['start_time'].dt.day_name().str.lower().astype('category')
    df['month'] = df['start_time'].dt.month_name().str.lower().astype('category')
    df['start_hour'] = df['start_time'].dt.hour.astype('category')

    # filtering the data
    if month:
        df = df[df['month'] == month]

    if day:
        df = df[df['day_of_week'] == day]

    print('Done...')
    print('-' * 40)
    time.sleep(2)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].value_counts()
    common_month = most_common_month.index[0].title()
    common_month_count = most_common_month.values[0]
    print(f'Most common month: "{common_month}", Count: {common_month_count}')

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].value_counts()
    common_day = most_common_day.index[0].title()
    common_day_count = most_common_day.values[0]
    print(f'Most common day of week: "{common_day}", Count: {common_day_count}')

    # TO DO: display the most common start hour
    most_common_hour = df['start_hour'].value_counts()
    common_hour = most_common_hour.index[0]
    common_hour_count = most_common_hour.values[0]
    print(f'Most common start hour: {common_hour}, Count: {common_hour_count}')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-' * 40)
    time.sleep(5)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['start_station'].value_counts()
    common_start_station = most_common_start_station.index[0]
    common_start_station_count = most_common_start_station.values[0]
    print(f'Most common start station: "{common_start_station}", Count: {common_start_station_count}')

    # TO DO: display most commonly used end station
    most_common_end_station = df['end_station'].value_counts()
    common_end_station = most_common_end_station.index[0]
    common_end_station_count = most_common_end_station.values[0]
    print(f'Most common end station: "{common_end_station}", Count: {common_end_station_count}')

    # TO DO: display most frequent combination of start station and end station trip
    most_common_station_combination = df.groupby(['start_station', 'end_station'])['start_time'].count().nlargest(1)
    start_station = most_common_station_combination.index[0][0]
    end_station = most_common_station_combination.index[0][1]
    count = most_common_station_combination.values[0]
    print(f'Most common combination of start & end station: "{start_station}" to "{end_station}", Count: {count}')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-' * 40)
    time.sleep(5)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['trip_duration'].sum()
    total_travel_time = round(total_travel_time / 60, 2)
    print(f'Total travel time: {total_travel_time} minutes')

    # TO DO: display mean travel time
    mean_travel_time = df['trip_duration'].mean()
    mean_travel_time = round(mean_travel_time / 60, 2)
    print(f'Mean travel time: {mean_travel_time} minutes')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-' * 40)
    time.sleep(5)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Count of user types:', end=' ')
    user_types_count = df['user_type'].value_counts().to_frame()
    data = zip(user_types_count.index.tolist(), user_types_count.values.reshape(1, -1)[0].tolist())
    for u_type, count in data:
        print(f'{u_type}-{count}', end=' ')
    print()

    # since we don't have gender and birth year in Washington Dataset, let's limit the operations to remaining datasets
    if city != 'washington':
        # TO DO: Display counts of gender
        print('Count of gender:', end=' ')
        gender_count = df['gender'].value_counts().to_frame()
        data = zip(gender_count.index.tolist(), gender_count.values.reshape(1, -1)[0].tolist())
        for gender, count in data:
            print(f'{gender}-{count}', end=' ')
        print()
        # TO DO: Display earliest, most recent, and most common year of birth
        # since I have filled the missing values with 0, filter the data where birth_year is not 0
        birth_year = df[df['birth_year'] != 0]['birth_year']
        print(f'Earliest birth year: {birth_year.min()}')
        print(f'Recent birth year: {birth_year.max()}')

        common_birth_year = birth_year.value_counts().nlargest(1)
        common_year = common_birth_year.index[0]
        common_year_count = common_birth_year.values[0]
        print(f'Most common year of birth: {common_year}, Count: {common_year_count}')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-' * 40)
    time.sleep(5)


def show_trip_data(df):
    """Displays individual trip data"""

    print('\nDisplaying individual trip data...\n')

    opt = 'yes'
    start = 0
    stop = 5
    col_names = df.columns

    while opt == 'yes':
        start_time = time.time()
        data = df.values[start:stop]
        for record in data:
            pprint(dict(zip(col_names, record)), indent=2)
            print()
        print("This took %s seconds.\n" % (time.time() - start_time))
        opt = input('Would you like to view individual trip data? Type \'yes\' or \'no\'.\n> ').strip().lower()
        start += 5
        stop += 5


def main():
    while True:
        clear_console()
        city, month, day = get_filters()
        time.sleep(1)
        df = load_data(city, month, day)
        time.sleep(1)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_trip_data(df)

        restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n> ').strip().lower()
        if restart.lower() != 'yes':
            print('\nGood bye.\n')
            break


if __name__ == "__main__":
    main()
