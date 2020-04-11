import numpy as np

class Visualization:

    def __init__(self):
        pass

    def show_driver_country_vertical(self, plt, f1):
        fig, ax = plt.subplots(figsize=(12, 15))
        country_names_dict = f1.cleaned_drivers['country_driver'].value_counts().to_dict()
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

    def show_driver_country_pretty(self, plt, f1):
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
            df = f1.cleaned_drivers['country_driver'].value_counts().to_frame()#pd.DataFrame({'percentage' : percentages})
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

    def show_drivers_with_home_race_pie(self, plt, f1):
        #pie chart of drivers with home vs no home  
        labels = ['Has Home Race', 'No Home Race']
        mask_has_home = f1.cleaned_drivers['country_driver'].isin(f1.cleaned_circuits['country_cir'])
        has_home = f1.cleaned_drivers[mask_has_home]
        no_home = f1.cleaned_drivers[~mask_has_home]
        sizes = [len(has_home), len(no_home)]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'no_home')

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('''Driver's With Home Race''')

        plt.savefig('../img/drivers_with_home_pie.png')
        #plt.show()
    
    def print_bar_chart(self, plt, y_data, title, y_label, x_data, x_label='', make_x_ticks=False, saveFigName='', color_list=[]):
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

    def show_drivers_average_means(self, plt, df_driver_means, years_for_title, color_list=[]):
        filename = years_for_title.replace(' ', '')
        #bar chart of avg pos(y ax) of home and away (x ax)
        values = [df_driver_means['position_result_mean_home'].mean(), df_driver_means['position_result_mean_away'].mean()]
        self.print_bar_chart(plt, y_data=values,title=f'Driver Average Means for {years_for_title}',y_label='Average Finishing Position',
            x_data=['Home', 'Away'], make_x_ticks=True, x_label='(Lower is better)', saveFigName=f'AvgDriverMeans{filename}.png', color_list=color_list)
    
    def show_home_away_comp(self, plt, df_driver_means, years_for_title, color_list=[]):
        filename = years_for_title.replace(' ', '')
        #bar chart of num of drivers (y) with home advantage and without home ad (x)
        values = [df_driver_means[df_driver_means['home_away_ratio'] > 1]['home_away_ratio'].count(), 
            df_driver_means[df_driver_means['home_away_ratio'] < 1]['home_away_ratio'].count()]
        self.print_bar_chart(plt, y_data=values,title=f'Frequency of Better Performance at Home vs Away for {years_for_title}',y_label='Number of Drivers',
            x_data=['Better At Home', 'Better Away'], x_label='', make_x_ticks=True, saveFigName=f'DriverAdvantageCounts{filename}.png', color_list=color_list)

    def show_home_away_ratio(self, plt, df_driver_means, years_for_title):
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

    def print_wins_per_construtor(self, plt, f1):
        #create mask and groupby constructor name and specify colums to inlude in final dataframe
        mask_wins = f1.df_all['position_result'] == 1
        wins_by_constructor = f1.df_all[(mask_wins)].groupby(['name_constr']).sum()[['position_result', 'points_result']]
        ## sort 
        wins_by_constructor.sort_values(by=['position_result'], ascending=False, inplace=True)
        print(wins_by_constructor.head(10))

        # all in one line
        #wins_by_constructor = self.df_all[(mask_wins)].groupby(['name_constr']).sum()[['position_result', 'points_result']].sort_values(by=['points_result'], ascending=False)