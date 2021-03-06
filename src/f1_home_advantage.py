import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import visualization as visualize
import show_stats

stat_printer = show_stats.ShowStats()

class F1Home:
    
    def __init__(self, results_data_path, races_data_path, drivers_data_path, 
                circuit_data_path, constructors_data_path, status_data_path):
        #load data
        self.raw_results = pd.read_csv(results_data_path)
        self.raw_races = pd.read_csv(races_data_path)
        self.raw_drivers = pd.read_csv(drivers_data_path)
        self.raw_circuits = pd.read_csv(circuit_data_path)
        self.raw_constructor = pd.read_csv(constructors_data_path)
        self.raw_status = pd.read_csv(status_data_path)

        self.cleaned_results = pd.DataFrame()
        self.cleaned_races = pd.DataFrame()
        self.cleaned_drivers = pd.DataFrame()
        self.cleaned_circuits = pd.DataFrame()
        self.cleaned_constructor = pd.DataFrame()
        self.cleaned_status = pd.DataFrame()

        self.cleaned_data_frames = [
            self.cleaned_results,
            self.cleaned_races,
            self.cleaned_drivers,
            self.cleaned_circuits,
            self.cleaned_constructor,
            self.cleaned_status
            ]

    def update_cleaned_df_list(self):
        self.cleaned_data_frames = [
            self.cleaned_results,
            self.cleaned_races,
            self.cleaned_drivers,
            self.cleaned_circuits,
            self.cleaned_constructor,
            self.cleaned_status
            ]

    def apply_data_cleaning(self):
        self.handle_nulls()
        self.convert_col_dtypes()
        self.create_calculated_cols()
        self.rename_cols()
        self.create_master_table()

    def select_desired_cols(self, results_cols, races_cols, drivers_cols, circuits_cols, constructor_cols, status_cols):
        self.cleaned_results = self.raw_results.copy()[results_cols]
        
        self.cleaned_races = self.raw_races.copy()[races_cols]
        self.cleaned_drivers = self.raw_drivers.copy()[drivers_cols]
        self.cleaned_circuits = self.raw_circuits.copy()[circuits_cols]
        self.cleaned_constructor = self.raw_constructor.copy()[constructor_cols]
        self.cleaned_status = self.raw_status.copy()[status_cols]
        self.update_cleaned_df_list()

    def handle_nulls(self):
            # With this data '\N' values were used to stand for null
            replace_val=-1
            
            for df in self.cleaned_data_frames:
                self.remove_newline(df=df,num_replace_val=replace_val, obj_replace_val=str(replace_val))

    def remove_newline(self, df, num_replace_val=-1, obj_replace_val='None'):
        """
        Replaces, INPLACE, \\N and \\n characters in a dataframe with the specified replacement values.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to search for \\N
        num_replace_val : int
            Number to replace newline with. Defaults to -1. 
        obj_replace_val : string
            String to replace newline with in oject dtype col
        """
        
        for col_name in df.columns:
            if df[col_name].dtype in ['int32', 'int64','float32', 'float64']:
                df[col_name].replace(r'\\N',  num_replace_val, regex=True, inplace=True)
            else:
                df[col_name].replace(r'\\N',  obj_replace_val, regex=True, inplace=True)

    def convert_col_dtypes(self):
        # convert cols that should be numbers
        self.cleaned_results['position'] = self.cleaned_results['position'].astype('int32')
        
        # convert cols that should be dates
        d_format = '%Y-%m-%d'
        self.cleaned_drivers['dob'] = self.cleaned_drivers['dob'].map(lambda x : dt.datetime.strptime(x, d_format))
        self.cleaned_races['date'] = self.cleaned_races['date'].map(lambda x : dt.datetime.strptime(x, d_format))

        self.update_cleaned_df_list()

    def create_calculated_cols(self):
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

        self.cleaned_drivers['country'] = self.cleaned_drivers['nationality'].apply(map_country_from_nationality)
        self.update_cleaned_df_list()
        
    def rename_cols(self):
        #rename some cols before merging since it gets confusing what some cols are referring to and merge.suffix is inadequate
        # don't rename the Id column
        self.cleaned_circuits.columns = self.cleaned_circuits.columns.map(lambda x: str(x) + '_cir' if str(x)[-2:]!='Id' else str(x))
        self.cleaned_results.columns = self.cleaned_results.columns.map(lambda x: str(x) + '_result' if str(x)[-2:]!='Id' else str(x))
        self.cleaned_drivers.columns = self.cleaned_drivers.columns.map(lambda x: str(x) + '_driver' if str(x)[-2:]!='Id' else str(x))
        self.cleaned_races.columns = self.cleaned_races.columns.map(lambda x: str(x) + '_race' if str(x)[-2:]!='Id' else str(x))
        self.cleaned_constructor.columns = self.cleaned_constructor.columns.map(lambda x: str(x) + '_constr' if str(x)[-2:]!='Id' else str(x))

        self.update_cleaned_df_list()

    def create_master_table(self):
        #LEFT JOIN Results on Drivers
        mg_results_driver = pd.merge(self.cleaned_results, self.cleaned_drivers, on='driverId', how='left', suffixes=('', '_driver'))
        #LEFT JOIN Races on Circuits
        mg_race_circuit = pd.merge(self.cleaned_races, self.cleaned_circuits, on='circuitId', how='left', suffixes=('_race', '_circuit'))
        #Bring the two DFs from above together with LEFT JOIN Results/Drivers on Races/Circuits
        mg_res_dr_rac_cir = pd.merge(mg_results_driver, mg_race_circuit, on='raceId', how='left', suffixes=('', '_race'))
        #LEFT JOIN Above on Constructors
        mg_res_dr_rac_cir_const = pd.merge(mg_res_dr_rac_cir, self.cleaned_constructor, on='constructorId', how='left', suffixes=('', '_constr'))
        #LEFT JOIN Above on Atatus
        self.df_all = pd.merge(mg_res_dr_rac_cir_const, self.cleaned_status, on='statusId', how='left')

    def save_csvs(self, save):
        if save:
            self.cleaned_results.to_csv('../output/cleaned_results.csv')
            self.cleaned_races.to_csv('../output/cleaned_races.csv')
            self.cleaned_drivers.to_csv('../output/cleaned_drivers.csv')
            self.cleaned_circuits.to_csv('../output/cleaned_circuits.csv')
            self.cleaned_constructor.to_csv('../output/cleaned_constructor.csv')
            self.cleaned_status.to_csv('../output/cleaned_status.csv')
            self.df_all.to_csv('../output/all.csv')

    def calculate_home_advantage(self, df):
        '''
        Parameters:
        -------
        df - Pandas DataFrame
            All race results driver on which to calculate the home advantage
            REQUIRED COLS: driverId, position_result, country_cir, country_driver
        Returns:
        -------
        df_driver_means_years_combined : Pandas DataFrame
            For combined years in the dataframe provided lists driver's basic info as well as average_home_means, average_away_means and home_to_away_ratio
        t_score_years_combined : float
            t-score of t-test comparing home_results and away_results for combined years
        p_val_years_combined : float
            p value for the t-test for combined years
        df_driver_means_by_year_by_driver : Pandas DataFrame
            average_home_means, average_away_means and home_to_away_ratio results by year by driver
        '''

        # select results for only those who finished the race
        df_valid_results = df[df['position_result'] != -1]
        
        #if a driver doesn't have a 'home race' then we can't use their results
        mask_driver_has_home_circuit = df_valid_results['country_cir'].isin(self.cleaned_drivers['country_driver'])
        df_results_of_drivers_who_have_home_race = df_valid_results[mask_driver_has_home_circuit]

        year_min = df_results_of_drivers_who_have_home_race['year_race'].min()
        year_max = df_results_of_drivers_who_have_home_race['year_race'].max()
        num_res = df_results_of_drivers_who_have_home_race['year_race'].count()
        #f'{num_res:,}
        print(f'Showing Home Advantage Results for Years {year_min} to {year_max} having {num_res:,} rows')

        # the tilde (\~) signifies "not" so ~mask_driver_has_home_circuit reads 'not mask_driver_has_home_circuit'
        df_results_driver_no_home_race = df_valid_results[~mask_driver_has_home_circuit]

        df_home_races = df_results_of_drivers_who_have_home_race[df_results_of_drivers_who_have_home_race['country_driver'] == df_results_of_drivers_who_have_home_race['country_cir']]
        df_away_races = df_results_of_drivers_who_have_home_race[df_results_of_drivers_who_have_home_race['country_driver'] != df_results_of_drivers_who_have_home_race['country_cir']]

        # calculate means for the entire group across all years/seasons in the df
        ########################################################################
        df_home_means_years_combined = df_home_races.groupby('driverId')['position_result'].mean().reset_index()
        df_away_means_years_combined = df_away_races.groupby('driverId')['position_result'].mean().reset_index()
        
        #merge means for combined years
        df_all_means_for_years_combined = pd.merge(df_home_means_years_combined, df_away_means_years_combined, on='driverId', how='left', suffixes=('_mean_home', '_mean_away'))
        
        #merge both means for combined years into drivers
        df_driver_means_years_combined = pd.merge(df_all_means_for_years_combined, self.cleaned_drivers, on='driverId', how='left')

        stat_printer.print_basic_stats(df_home_means_years_combined['position_result'],'home_means for ALL YEARS combined')
        stat_printer.print_basic_stats(df_away_means_years_combined['position_result'],'away_means for ALL YEARS combined')
        
        t_score_years_combined, p_val_years_combined = stat_printer.print_t_test_ind(df_home_means_years_combined['position_result'], 
                df_away_means_years_combined['position_result'], 'home and away means for ALL YEARS combined')
        
        #ratio of home_mean to away _mean for combined years - so above 1 is better at home below 1 is better away
        df_driver_means_years_combined['home_away_ratio'] = df_driver_means_years_combined['position_result_mean_home']/df_driver_means_years_combined['position_result_mean_away']

        
        #calculate means per season
        ########################################################################
        df_home_means_by_year_by_driver = df_home_races.groupby(['driverId', 'year_race'])['position_result'].mean().reset_index()
        df_away_means_by_year_by_driver = df_away_races.groupby(['driverId', 'year_race'])['position_result'].mean().reset_index()

        #merge means for season years
        df_all_means_by_year_by_driver = pd.merge(df_home_means_by_year_by_driver, df_away_means_by_year_by_driver, on='driverId', how='left', suffixes=('_mean_home', '_mean_away'))
        
        #merge both means for season years into drivers
        df_driver_means_by_year_by_driver = pd.merge(df_all_means_by_year_by_driver, self.cleaned_drivers, on='driverId', how='left')

        #ratio of home_mean to away _mean for season years
        df_driver_means_by_year_by_driver['home_away_ratio'] = df_driver_means_by_year_by_driver['position_result_mean_home']/df_driver_means_by_year_by_driver['position_result_mean_away']
        ##################################################################

        df_driver_means_years_combined.to_csv('../output/df_driver_means_years_combined.csv')
        df_driver_means_by_year_by_driver.to_csv('../output/df_driver_means_by_year_by_driver.csv')

        return df_driver_means_years_combined, t_score_years_combined, p_val_years_combined, df_driver_means_by_year_by_driver

    # TODO - implement include_all_driver_years so it does something different for False, right now the function
    # runs as if it were always true
    def filter_results_by_year(self, start_year, end_year, include_all_driver_years=True):
        '''
        Create DataFrame that has ALL results for drivers who competed in the years supplied in the parameters
        If include_all_driver_years is True include results that are in years outside supplied range.
        So if the start_year is 2015, the results for Lewis Hamilton would include all of his races since he started in 2007.
        Even though there are now some results that were before 2015,
        Jules Bianchi, who raced in 2014 but tragically died in a race that year, would not be included in the results.
        '''
        #find all driverIds for races in the year interval
        mask_time_interval = (self.df_all['year_race'] >= start_year) & (self.df_all['year_race'] <= end_year)
        driver_id_list = self.df_all[mask_time_interval]['driverId'].tolist()

        #with that list of driverIds, do a isin(driverIDList) to get all results to be used for calculation
        mask_driver_ids = self.df_all['driverId'].isin(driver_id_list)
        df_filtered_results = self.df_all[mask_driver_ids]
        
        return df_filtered_results

    def end_user_home_adv_for_all_data(self):
        start_year = self.cleaned_races['year_race'].min()
        end_year = self.cleaned_races['year_race'].max()

        df = self.filter_results_by_year(start_year, end_year)
        return self.calculate_home_advantage(df)

    def end_user_driver_ratios_by_season(self, start_year, end_year):
        '''
        Attributes
        ----------
        
        start_year : int
            Minimum year in which a driver competed
        end_year : int
            Maximum year in which a driver competed
        driver_id_list : list of ints
                    Driver ids to include in search
                    defaults to only Lewis Hamilton, driverId=1

        Returns
        -------
        df_driver_means_years_combined : Pandas DataFrame

        t_score_years_combined : float

        p_val_years_combined : float

        df_driver_means_by_year_by_driver : Pandas DataFrame
        '''
        
        if start_year < self.cleaned_races['year_race'].min():
            raise Exception("The starting year chosen is before the earliest data that exists.")

        if end_year > self.cleaned_races['year_race'].max():
            raise Exception("The ending year chosen is before the latest data that exists.")
        
        
        
        # filter for for specified time interval
        df_filtered_seasons_results = self.filter_results_by_year(start_year, end_year, include_all_driver_years=True)
        # now we have a df of all driver results in the time interval

        # get results for the time and driver conditions
        df_driver_means_years_combined, t_score_years_combined, p_val_years_combined, df_driver_means_by_year_by_driver = self.calculate_home_advantage(df_filtered_seasons_results)

        return df_driver_means_years_combined, t_score_years_combined, p_val_years_combined, df_driver_means_by_year_by_driver

    def end_user_all_most_wins(self):
        # mask_wins = self.df_all['position_result'] == 1
        # df_most_wins = self.df_all[mask_wins].groupby('driverId').sum()['position_result'].sort_values(ascending=False).head(10)
        pass

    def end_user_most_recent_grid(self):
        #get most recent year
        #need to update so dynamically gets year. right now it has race dates for future races that have no results data
        #need to join dataframes for this and I am running out of time!
        most_recent_year = 2019#self.cleaned_races['year_race'].max()

        #get all results for most recent year DELETE ME?
        #df_recent_year_results = self.df_all[self.df_all['year_race'] == most_recent_year]

        return self.end_user_driver_ratios_by_season(most_recent_year,most_recent_year)


    def print_driver_ratio_per_year(self, df):
        grp = df.groupby(['driverId', 'year_race_mean_home'])
        ham_ratio = grp[grp['driverId'] == 1]
        for name, g in grp.groups:
            print(f'name: {name}')
            print(f'group {g}')

    def ham_2019(self):
        mask_ham = self.df_all['driverId'].isin([1])
        mask_year = self.df_all['year_race'] == 2019
        df_ham = self.df_all[mask_ham & mask_year][['surname_driver', 'date_race', 'position_result']].sort_values('date_race')
        
        fig, axes = plt.subplots()
        axes.plot(df_ham['date_race'], df_ham['position_result'])

        
    
if __name__ == '__main__':

    raw_results_path = '../data/results.csv'
    raw_races_path = '../data/races.csv'
    raw_drivers_path = '../data/drivers.csv'
    raw_circuits_path = '../data/circuits.csv'
    raw_constructor_path = '../data/constructors.csv'
    raw_status_path = '../data/status.csv'

    results_cols = ['resultId','raceId','driverId', 'constructorId','position','statusId', 'points']
    races_cols = ['raceId','year','round','circuitId','name','date','time']
    drivers_cols = ['driverId','driverRef','number','code','forename','surname','dob','nationality']
    circuits_cols = ['circuitId','name','location','country','lat','lng','alt']
    constructor_cols = ['constructorId','constructorRef','name','nationality']
    status_cols = ['statusId', 'status']

    f_one = F1Home(raw_results_path, raw_races_path, raw_drivers_path, raw_circuits_path, raw_constructor_path, raw_status_path)
    f_one.select_desired_cols(results_cols, races_cols, drivers_cols, circuits_cols, constructor_cols, status_cols)
    f_one.apply_data_cleaning()
    f_one.save_csvs(False)


    vis = visualize.Visualization()
    
    plt.style.use('seaborn-deep')
    color_list=['grey', 'green']
    #df_driver_means_years_combined, t_score, p_val, df_driver_means_by_year_by_driver = f_one.end_user_home_adv_for_all_data()
    # vis.show_driver_country_vertical(plt, f_one)
    # vis.show_drivers_with_home_race_pie(plt, f_one)
    # vis.show_driver_country_pretty(plt, f_one)
    # vis.show_drivers_average_means(plt,df_driver_means_years_combined, 'All Years')
    # vis.show_home_away_comp(plt, df_driver_means_years_combined, 'All Years')
    # vis.show_home_away_ratio(plt, df_driver_means_years_combined, 'All Years')

    
    # By Season
    df_driver_means_years_combined, t_score_years_combined, p_val_years_combined, df_driver_means_by_year_by_driver = f_one.end_user_most_recent_grid()
    vis.show_drivers_average_means(plt,df_driver_means_years_combined, '2019 Grid')
    vis.show_home_away_comp(plt, df_driver_means_years_combined, '2019 Grid')
    #f_one.print_driver_ratio_per_year(df_driver_means_by_year_by_driver)
    #f_one.show_home_away_ratio(df_driver_means_years_combined, '2019 Grid')

    # Info printed to terminal
    #f_one.print_wins_per_construtor()
    #avgHAR = df_driver_means_years_combined['home_away_ratio'].mean()
    #print(f'Years Combined Average HAR: {avgHAR}')
    #print(f_one.df_all.corr())
   
    #f_one.ham_2019()

    plt.show()
