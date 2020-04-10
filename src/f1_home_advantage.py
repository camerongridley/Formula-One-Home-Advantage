import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

from data_cleaner import DataCleaner
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
        #self.cleaned_constructor_standings = self.raw_constructor_standings[]
        #self.cleaned_qualify = self.raw_qualify[]
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

        #time convertions to datetime.time
        #cleaned_races['time'] = cleaned_races['time'].map(lambda x : dt.datetime.strptime(x, '%H:%M:%S'))

        #timings - timedelta objs

        #cleaned_result['time'] = cleaned_result['time'].map(lambda x : pd.to_timedelta(x, unit=?))
        #fastestLapTime
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
        #self.cleaned_status.columns = self.cleaned_status.columns.map(lambda x: str(x) + '_stat' if str(x)[-2:]!='Id' else str(x))
        #self.cleaned_qualify.columns = self.cleaned_qualify.columns.map(lambda x: str(x) + '_qual' if str(x)[-2:]!='Id' else str(x))

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

        #Check shapes to see if they look right and numer of rows matches between cleaned_results and df_all
        # print(f'mg_results_driver: {mg_results_driver.shape}')
        # print(f'mg_race_circuit: {mg_race_circuit.shape}')
        # print(f'mg_res_dr_rac_cir: {mg_res_dr_rac_cir.shape}')
        # print(f'mg_res_dr_rac_cir_const: {mg_res_dr_rac_cir_const.shape}')
        # print(f'df_all: {self.df_all.shape}')

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


        # for each season year, get home/away result means and ratio
        # since we add 1 to the year in the call to filter_results_by_year, don't add 1 when setting the range for the loop
        #for year in range(start_year, end_year):
        #    df_season = self.filter_results_by_year(year, year+1)

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


    def show_driver_country_vertical(self):
        dr_country = self.cleaned_drivers['nationality_driver'].value_counts().to_frame()
        dr_country.plot(kind='bar')
        plt.tight_layout()
        plt.savefig('../img/driver_country_count_bar.png')
        #plt.show()

    def show_driver_countries(self):
            fig, ax = plt.subplots(figsize=(12, 15))
            country_names_dict = self.cleaned_drivers['country_driver'].value_counts().to_dict()
            countries = list(country_names_dict.values())
            y_pos = np.arange(len(country_names_dict))

            ax.barh(y_pos, countries, height=.8, align='center')
            ax.set_yticks((y_pos))
            ax.set_yticklabels(country_names_dict.keys(), fontsize=16)
            #ax.set_xticklabels()
            ax.invert_yaxis() # labels read top-to-bottom
            ax.set_xlabel('Drivers', fontsize=18)
            ax.set_title('Number of Drivers Per Country',  fontsize=20)
            plt.tight_layout()
            plt.savefig('../img/driver_country_count_bar.png')
            #plt.show()

    def show_driver_country_pretty(self):
        # set font
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = 'Helvetica'

        # set the style of the axes and the text color
        plt.rcParams['axes.edgecolor']='#333F4B'
        plt.rcParams['axes.linewidth']=0.8
        plt.rcParams['xtick.color']='#333F4B'
        plt.rcParams['ytick.color']='#333F4B'
        plt.rcParams['text.color']='#333F4B'

        # create some fake data
        #percentages = pd.Series([20, 15, 18, 8, 6, 7, 10, 2, 10, 4], 
        #                        index=['Rent', 'Transportation', 'Bills', 'Food', 
        #                            'Travel', 'Entertainment', 'Health', 'Other', 'Clothes', 'Phone'])
        df = self.cleaned_drivers['country_driver'].value_counts().to_frame()#pd.DataFrame({'percentage' : percentages})
        df = df.sort_values(by='country_driver')

        # we first need a numeric placeholder for the y axis
        my_range=list(range(1,len(df.index)+1))

        fig, ax = plt.subplots(figsize=(5,7))

        # create for each expense type an horizontal line that starts at x = 0 with the length 
        # represented by the specific expense percentage value.
        plt.hlines(y=my_range, xmin=0, xmax=df['country_driver'], color='#007ACC', alpha=0.2, linewidth=5)

        # create for each expense type a dot at the level of the expense percentage value
        plt.plot(df['country_driver'], my_range, "o", markersize=5, color='#007ACC', alpha=0.6)

        # set labels
        ax.set_xlabel('Drivers', fontsize=15, fontweight='black', color = '#333F4B')
        ax.set_ylabel('')

        # set axis
        ax.tick_params(axis='both', which='major', labelsize=12)
        plt.yticks(my_range, df.index)

        # add an horizonal label for the y axis 
        fig.text(-0.23, 0.96, 'Number of Drivers Per Country', fontsize=15, fontweight='black', color = '#333F4B')

        # change the style of the axis spines
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)

        # set the spines position
        ax.spines['bottom'].set_position(('axes', -0.04))
        ax.spines['left'].set_position(('axes', 0.015))

        plt.savefig('../img/driver_country_count_bar_pretty.png', dpi=300, bbox_inches='tight')

    def show_drivers_with_home_race_pie(self):
        #pie chart of drivers with home vs no home  
        labels = ['Has Home Race', 'No Home Race']
        mask_has_home = self.cleaned_drivers['country_driver'].isin(self.cleaned_circuits['country_cir'])
        has_home = self.cleaned_drivers[mask_has_home]
        no_home = self.cleaned_drivers[~mask_has_home]
        sizes = [len(has_home), len(no_home)]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'no_home')

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('''Driver's With Home Race''')

        plt.savefig('../img/drivers_with_home_pie.png')
        #plt.show()
    
    def print_bar_chart(self, y_data, title, y_label, x_data, x_label='', make_x_ticks=False, saveFigName='', color_list=[]):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        x = x_data

        if make_x_ticks:
            x = np.arange(len(x_data))
            plt.xticks(x, x_data)
        if color_list:
            ax.bar(x=x, height=y_data, color=color_list)
        else:
            ax.bar(x=x, height=y_data)
        ax.set_title(title, fontsize=20)
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
        if saveFigName:
            plt.savefig(f'../img/{saveFigName}')
        plt.tight_layout()
        #plt.show()

    def show_drivers_average_means(self, df_driver_means, years_for_title, color_list=[]):
        filename = years_for_title.replace(' ', '')
        #bar chart of avg pos(y ax) of home and away (x ax)
        values = [df_driver_means['position_result_mean_home'].mean(), df_driver_means['position_result_mean_away'].mean()]
        self.print_bar_chart(y_data=values,title=f'Driver Average Means for {years_for_title}',y_label='Average Finishing Position',
            x_data=['Home', 'Away'], make_x_ticks=True, x_label='(Lower is better)', saveFigName=f'AvgDriverMeans{filename}.png', color_list=color_list)
    
    def show_home_away_comp(self, df_driver_means, years_for_title, color_list=[]):
        filename = years_for_title.replace(' ', '')
        #bar chart of num of drivers (y) with home advantage and without home ad (x)
        values = [df_driver_means[df_driver_means['home_away_ratio'] > 1]['home_away_ratio'].count(), 
            df_driver_means[df_driver_means['home_away_ratio'] < 1]['home_away_ratio'].count()]
        self.print_bar_chart(y_data=values,title=f'Frequency of Better Performance at Home vs Away for {years_for_title}',y_label='Number of Drivers',
            x_data=['Better At Home', 'Better Away'], x_label='', make_x_ticks=True, saveFigName=f'DriverAdvantageCounts{filename}.png', color_list=color_list)

    def show_home_away_ratio(self, df_driver_means, years_for_title):
        filename = years_for_title.replace(' ', '')
        # histogram of home/away ratio
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.hist(df_driver_means['home_away_ratio'], bins=80, alpha=1)
        ax.set_title(f'Ratio of Home/Away Finishing Positions for {years_for_title}')
        ax.set_xlabel('Home/Away Avgerage Ratio')
        ax.set_ylabel('Number of Drivers')
        plt.savefig(f'../img/all_results_home_away_ration{filename}.png')
        
        #plt.show()

    def print_wins_per_construtor(self):
        #create mask and groupby constructor name and specify colums to inlude in final dataframe
        mask_wins = self.df_all['position_result'] == 1
        wins_by_constructor = self.df_all[(mask_wins)].groupby(['name_constr']).sum()[['position_result', 'points_result']]
        ## sort 
        wins_by_constructor.sort_values(by=['position_result'], ascending=False, inplace=True)
        print(wins_by_constructor.head(10))

        # all in one line
        #wins_by_constructor = self.df_all[(mask_wins)].groupby(['name_constr']).sum()[['position_result', 'points_result']].sort_values(by=['points_result'], ascending=False)

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

    plt.style.use('seaborn-deep')

    #df_driver_means_years_combined, t_score, p_val, df_driver_means_by_year_by_driver = f_one.end_user_home_adv_for_all_data()

    # Visualizations
    color_list=['grey', 'green']
    # f_one.show_driver_countries()
    # f_one.show_drivers_with_home_race_pie()
    # f_one.show_drivers_average_means(df_driver_means_years_combined, 'All Years')
    # f_one.show_home_away_comp(df_driver_means_years_combined, 'All Years')
    # f_one.show_home_away_ratio(df_driver_means_years_combined, 'All Years')
    # f_one.show_driver_country_pretty()
    

    # By Season
    df_driver_means_years_combined, t_score_years_combined, p_val_years_combined, df_driver_means_by_year_by_driver = f_one.end_user_most_recent_grid()
    #f_one.print_driver_ratio_per_year(df_driver_means_by_year_by_driver)
    f_one.show_drivers_average_means(df_driver_means_years_combined, '2019 Grid')
    f_one.show_home_away_comp(df_driver_means_years_combined, '2019 Grid')
    #f_one.show_home_away_ratio(df_driver_means_years_combined, '2019 Grid')

    # Info printed to terminal
    #f_one.print_wins_per_construtor()
    #avgHAR = df_driver_means_years_combined['home_away_ratio'].mean()
    #print(f'Years Combined Average HAR: {avgHAR}')
    #print(f_one.df_all.corr())
   
    #f_one.ham_2019()

    plt.show()
