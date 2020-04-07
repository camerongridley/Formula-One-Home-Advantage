import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import driver
from data_cleaner import DataCleaner
import show_stats

stat_printer = show_stats.ShowStats()
plt.style.use('ggplot')

''' **********************************************************
GET DATA
********************************************************** '''
raw_results = pd.read_csv('../data/results.csv')
raw_races = pd.read_csv('../data/races.csv')
raw_drivers = pd.read_csv('../data/drivers.csv')
raw_circuits = pd.read_csv('../data/circuits.csv')
raw_constructor = pd.read_csv('../data/constructors.csv')
raw_status = pd.read_csv('../data/status.csv')
raw_constructor_standings = pd.read_csv('../data/constructor_standings.csv')
raw_qualify = pd.read_csv('../data/qualifying.csv')

''' **********************************************************
CLEAN DATA - INITIAL
********************************************************** '''
################ REMOVE UNWANTED COLS #####################
cleaned_results = raw_results.drop(columns=['milliseconds'])
cleaned_races = raw_races.drop(columns=['url'])
cleaned_drivers = raw_drivers.drop(columns=['url'])
cleaned_circuits = raw_circuits.drop(columns=['url'])
cleaned_constructor = raw_constructor.drop(columns=['url'])
cleaned_constructor_standings = raw_constructor_standings.drop(columns=['positionText'])
cleaned_status = raw_status#.drop()
cleaned_qualify = raw_qualify#.drop()

################ HANDLE NULLS #####################
# With this data '\N' values that were used to stand for null
data_list = [
    cleaned_results,
    cleaned_races,
    cleaned_drivers,
    cleaned_circuits,
    cleaned_constructor,
    cleaned_constructor_standings,
    cleaned_status,
    cleaned_qualify
    ]

num_replace_val=-1
cleaner = DataCleaner()
for df in data_list:
    #cleaner.remove_newline(df=df,num_replace_val=-1, obj_replace_val='-1' )
    for col_name in df.columns:
        if df[col_name].dtype in ['int32', 'int64','float32', 'float64']:
            df[col_name].replace(r'\\N',  num_replace_val, regex=True, inplace=True)
        else:
            df[col_name].replace(r'\\N',  str(num_replace_val), regex=True, inplace=True)

################ CONVERT DTYPES #####################
# convert cols that should be numbers
cleaned_results.astype({'number' : 'int32', 'position' : 'int32', 'fastestLapSpeed' : 'float32'}, copy=False)
#the above isn't maintining or working so forced coversion for position col
#cleaned_results[['position']].apply(pd.to_numeric, errors='coerce')
cleaned_results['position'] = cleaned_results['position'].astype('int32')

# convert cols that should be dates
d_format = '%Y-%m-%d'
cleaned_drivers['dob'] = cleaned_drivers['dob'].map(lambda x : dt.datetime.strptime(x, d_format))
cleaned_races['date'] = cleaned_races['date'].map(lambda x : dt.datetime.strptime(x, d_format))

#time convertions to datetime.time
#cleaned_races['time'] = cleaned_races['time'].map(lambda x : dt.datetime.strptime(x, '%H:%M:%S'))

#timings - timedelta objs

#cleaned_result['time'] = cleaned_result['time'].map(lambda x : pd.to_timedelta(x, unit=?))
#fastestLapTime


################ ADD COLS #####################
#Add country to drivers table based off thier nationality value
driver_countries_dict = {'British': 'UK', 'German': 'Germany', 'Spanish': 'Spain', 'Finnish': 'Finland', 'Japanese': 'Japan', 'French': 'France', 'Polish': 'Poland',
 'Brazilian': 'Brazil', 'Italian': 'Italy', 'Australian': 'Australia', 'Austrian': 'Austria', 'American': 'USA', 'Dutch': 'Netherlands',
 'Colombian': 'Columbia', 'Portuguese': 'Portugal', 'Canadian': 'Canada', 'Indian': 'India', 'Hungarian': 'Hungary', 'Irish': 'Ireland', 'Danish': 'Denmark',
 'Malaysian': 'Malaysia', 'Argentine': 'Argentina', 'Czech': 'Czech Republic', 'Belgian': 'Belgium', 'Swiss': 'Switzerland', 'Monegasque': 'Monaco', 'Swedish': 'Sweden',
 'Venezuelan': 'Venezuela', 'New Zealander': 'New Zealand', 'Chilean': 'Chile', 'Mexican': 'Mexico', 'South African': 'South Africa',
 'Liechtensteiner': 'Liechtenstein', 'Rhodesian': 'Rhodesia', 'American-Italian': 'USA', 'Uruguayan': 'Uruguay',
 'Argentine-Italian': 'Italy', 'Thai': 'Thailand', 'East German': 'Germany', 'Russian': 'Russia', 'Indonesian': 'Indonesia'
}

def map_country_from_nationality(nationality):
    return driver_countries_dict[nationality]

cleaned_drivers['country'] = cleaned_drivers['nationality'].apply(map_country_from_nationality)

################ RENAME COLS #####################
#rename some cols before merging since it gets confusing what some cols are referring to and merge.suffix is inadequate
# don't rename the Id column
cleaned_circuits.columns = cleaned_circuits.columns.map(lambda x: str(x) + '_cir' if str(x)[-2:]!='Id' else str(x))
cleaned_results.columns = cleaned_results.columns.map(lambda x: str(x) + '_result' if str(x)[-2:]!='Id' else str(x))
cleaned_drivers.columns = cleaned_drivers.columns.map(lambda x: str(x) + '_driver' if str(x)[-2:]!='Id' else str(x))
cleaned_races.columns = cleaned_races.columns.map(lambda x: str(x) + '_race' if str(x)[-2:]!='Id' else str(x))
cleaned_constructor.columns = cleaned_constructor.columns.map(lambda x: str(x) + '_constr' if str(x)[-2:]!='Id' else str(x))
#cleaned_status.columns = cleaned_status.columns.map(lambda x: str(x) + '_stat' if str(x)[-2:]!='Id' else str(x))
cleaned_qualify.columns = cleaned_qualify.columns.map(lambda x: str(x) + '_qual' if str(x)[-2:]!='Id' else str(x))

''' **********************************************************
MERGE DATA
********************************************************** '''
#LEFT JOIN Results on Drivers
mg_results_driver = pd.merge(cleaned_results, cleaned_drivers, on='driverId', how='left', suffixes=('', '_driver'))
#LEFT JOIN Races on Circuits
mg_race_circuit = pd.merge(cleaned_races, cleaned_circuits, on='circuitId', how='left', suffixes=('_race', '_circuit'))
#Bring the two DFs from above together with LEFT JOIN Results/Drivers on Races/Circuits
mg_res_dr_rac_cir = pd.merge(mg_results_driver, mg_race_circuit, on='raceId', how='left', suffixes=('', '_race'))
#LEFT JOIN Above on Constructors
mg_res_dr_rac_cir_const = pd.merge(mg_res_dr_rac_cir, cleaned_constructor, on='constructorId', how='left', suffixes=('', '_constr'))
#LEFT JOIN Above on Atatus
df_all = pd.merge(mg_res_dr_rac_cir_const, cleaned_status, on='statusId', how='left')

#Check shapes to see if they look right and numer of rows matches between cleaned_results and df_all
# print(f'mg_results_driver: {mg_results_driver.shape}')
# print(f'mg_race_circuit: {mg_race_circuit.shape}')
# print(f'mg_res_dr_rac_cir: {mg_res_dr_rac_cir.shape}')
# print(f'mg_res_dr_rac_cir_const: {mg_res_dr_rac_cir_const.shape}')
# print(f'df_all: {df_all.shape}')

# save to .csv
df_all.to_csv('../data/df_all.csv')



''' **********************************************************
ANALYSIS
********************************************************** '''
if __name__ == '__main__':
    #REMINDER : mask - grouby - agg - col selection - sort

    #***Number of wins per contructor
    # #create mask and groupby constructor name and specify colums to inlude in final dataframe
    # mask_wins = df_all['positionOrder_result'] == 1
    # wins_by_constructor = df_all[(mask_wins)].groupby(['name_constr']).sum()[['positionOrder_result', 'points_result']]
    # ## sort 
    # wins_by_constructor.sort_values(by=['positionOrder_result'], ascending=False, inplace=True)
    # print(wins_by_constructor.head(10))
    # # all in one line
    # wins_by_constructor = df_all[(mask_wins)].groupby(['name_constr']).sum()[['positionOrder_result', 'points_result']].sort_values(by=['points_result'], ascending=False)

    '''
    HYPOTH 1 - Comparing 'home' wins to 'away' wins
    How to organize this data? Have to exclude drivers who don't have a race in their home country.
    What will my axes be?  x: probability of winning?
    Plots wanted:
    1) bar chart? for all (current ?) drivers, regardless of year - binomial choice 0 = position/avg perf <= agv pos for all their races; 1 = position/avg perf > agv
        1A) for Bayesian Testing - Distribution A = 'home', Distribution B = away
    2) line plot - Average for all drivers across all seasons - single plot
    3) Per driver across all seasons participated in - 1 plot per driver
    4) Per driver per season - does the relationship change at all over time? 1 plot per driver per season

    Per seasons over time for all drivers combined - plot per season they competed
    --- Query : will need to groupby Year, then Driver
    3) All seasons driver particpated in - single plot
    '''

    #WHY DON'T YOU WORK??????!!!!!!!  - AH-HA!have to use numbers on the x axis
    # 
    # dr_country = cleaned_drivers['nationality_driver'].value_counts().to_dict()
    # print(type(dr_country))
    # print(dr_country)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.bar(dr_country.keys(), dr_country.items())
    # ax.set_title('''Driver's Home Countries''')
    
    # dr_country = cleaned_drivers['nationality_driver'].value_counts().to_frame()
    # dr_country.plot(kind='bar')
    # plt.tight_layout()
    # plt.savefig('..img/driver_country_count_bar.png')
    # plt.show()

    ################ HOME AND AWAY RACES #####################
    # query for all 'home' races across all drivers and seasons
    df_finishers = df_all[df_all['position_result'] != -1]
    mask_is_home_circuit = df_finishers['country_cir'].isin(cleaned_drivers['country_driver'])
    
    df_results_with_home_race = df_finishers[(mask_is_home_circuit)]

    # the tilde (\~) signifies "not" so ~mask_is_home_circuit reads 'not mask_is_home_circuit'
    df_results_with_away_race = df_finishers[~mask_is_home_circuit]

    df_home_races = df_results_with_home_race[df_results_with_home_race['country_driver'] == df_results_with_home_race['country_cir']]
    df_away_races = df_results_with_home_race[df_results_with_home_race['country_driver'] != df_results_with_home_race['country_cir']]

    home_means = df_home_races.groupby('driverId')['position_result'].mean().reset_index()
    away_means = df_away_races.groupby('driverId')['position_result'].mean().reset_index()
    
    #merge means
    all_means = pd.merge(home_means, away_means, on='driverId', how='left', suffixes=('_mean_home', '_mean_away'))
    
    #merge both means into drivers
    df_driver_means = pd.merge(all_means, cleaned_drivers, on='driverId', how='left')

    stat_printer.print_basic_stats(home_means['position_result'],'home_means')
    stat_printer.print_basic_stats(away_means['position_result'],'away_means')
    stat_printer.print_t_test_ind(home_means['position_result'], away_means['position_result'], 'home and away means')
    
    #ratio of home_mean to away _mean - so above 1 is better at home below 1 is better away
    df_driver_means['home_away_ratio'] = df_driver_means['position_result_mean_home']/df_driver_means['position_result_mean_away']

    '''**********************************************************
    VISUALIZATIONS
    **********************************************************'''
    #Data Description Visualizations

    ###pie chart of drivers with home vs no home  
    # labels = ['Has Home Race', 'No Home Race']
    # mask_has_home = cleaned_drivers['country_driver'].isin(cleaned_circuits['country_cir'])
    # has_home = cleaned_drivers[mask_has_home]
    # no_home = cleaned_drivers[~mask_has_home]
    # breakpoint()
    # sizes = [len(has_home), len(no_home)]
    # explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'no_home')

    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #plt.show()


    #Data Anaysis Visualizations
    
    
    #bar chart of avg pos(y ax) of home and away (x ax)
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    x = np.arange(2)
    values = [all_means['position_result_mean_home'].mean(), all_means['position_result_mean_away'].mean()]
    labels = ['Home', 'Away']
    ax1.bar(x, values, color=['chartreuse', 'black'])
    plt.xticks(x, labels)
    ax1.set_title('''Driver's Average Means''')
    ax1.set_ylabel('Average Finishing Position')
    plt.show()

    #bar chart of num of drivers (y) with home advantage and without home ad (x)
    fig = plt.figure(figsize=(10, 6))
    ax2 = fig.add_subplot(111)

    x = np.arange(2)
    values = [all_means['position_result_mean_home'].count(), all_means['position_result_mean_away'].count()]
    labels = ['Advantage', 'No Advantage']
    ax2.bar(x, values, color='tan')
    plt.xticks(x, labels)
    ax2.set_title('Drivers Advantage Counts')
    ax2.set_ylabel('Number of Drivers')
    plt.show()

    # histogram of home/away ratio
    fig = plt.figure(figsize=(10, 6))
    ax3 = fig.add_subplot(111)
    ax3.hist(df_driver_means['home_away_ratio'], bins=80, alpha=1)
    ax3.set_title('Ratio of Finishing Positions')
    ax3.set_xlabel('Home/Away Avgerage Ratio')
    ax3.set_ylabel('Number of Drivers')

    plt.tight_layout()
    plt.show()
