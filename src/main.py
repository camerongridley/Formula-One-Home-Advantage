import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import driver
import data_cleaner as cleaner

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

replace_val = -1

#cleaner.remove_newline(df=df_all)
for df in data_list:
    #cleaner.DataCleaner.remove_newline(data=df,num_replace_val=replace_val, obj_replace_val=str(replace_val) )
    for col_name in df.columns:
        if df[col_name].dtype in ['int32', 'int64','float32', 'float64']:
            df[col_name].replace(r'\\N',  replace_val, regex=True, inplace=True)
        else:
            df[col_name].replace(r'\\N',  str(replace_val), regex=True, inplace=True)

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

    #WHY DON'T YOU WORK??????!!!!!!!
    # dr_country = cleaned_drivers['nationality_driver'].value_counts().to_dict()
    # print(type(dr_country))
    # print(dr_country)
    # #histogram of driver countries
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
    mask_remove_neg_one = df_all['position_result'] != -1
    mask_is_home_circuit = df_all['country_cir'].isin(cleaned_drivers['country_driver'])
    df_results_with_home_race = df_all[(mask_remove_neg_one & mask_is_home_circuit)]
    
    df_home_races = df_results_with_home_race[df_results_with_home_race['country_driver'] == df_results_with_home_race['country_cir']]
    
    means = df_home_races.groupby('driverId')['position_result'].mean()#.rename(columns={'position_result':'position_home_mean'})
    #cleaned_drivers['position_home_mean'] = means
    df_driver_home_mean = pd.merge(means, cleaned_drivers, on='driverId', how='left')
    breakpoint()




    
    # # Get drivers who have a "home" race - meaning their home country is also a country which a race takes place
    # mask_have_home_race = cleaned_drivers['country_driver'].isin(cleaned_circuits['country_cir'])
    # df_drivers_with_home_race = cleaned_drivers.loc[mask_have_home_race, :]

    # #get all the results for these drivers only
    # mask_results_have_home = df_all['driverId'].isin(df_drivers_with_home_race['driverId'])
    # mask_negative_one = df_all['positionOrder_result'] != -1
    # df_results_drivers_with_home_race = df_all[(mask_results_have_home & mask_negative_one)]
    # df_results_drivers_with_home_race.to_csv('../data/df_results_drivers_with_home_race.csv')
  
    # #Of the drivers who have home races, split their race result into HOME and AWAY groups
    # mask_home_results = df_results_drivers_with_home_race['country_cir'] == df_results_drivers_with_home_race['country_driver']
    # mask_away_races = df_results_drivers_with_home_race['country_cir'] != df_results_drivers_with_home_race['country_driver']
    
    # # 
    # df_drivers_with_home_race['position_home_mean'] = df_results_drivers_with_home_race.loc[mask_home_results, :].groupby('driverId')['positionOrder_result'].mean()
    # df_drivers_with_home_race.to_csv('../data/df_drivers_with_home_race.csv')
    # #df_drivers_with_home_race['position_mean'] = df_drivers_with_home_race[mask_home_races].groupby('driverId')[['surname_driver', 'positionOrder_result']].agg('mean')
    
    # df_results_drivers_with_home_race[df_results_drivers_with_home_race['driverId']==1]['positionOrder_result'].mean()

    # breakpoint()
    
 
    '''
    Create Classes
    '''
    # #print(cleaned_drivers['nationality_driver'].hist())
    # drivers_ls = []
    # for i, driver in enumerate(cleaned_drivers.iterrows()):
    #     #drivers_ls.append(Driver())
    #     #print(driver['driverId'])
    #     pass

