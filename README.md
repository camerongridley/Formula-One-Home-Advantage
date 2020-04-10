![banner1-elip](img/readme/banner1-elip.png)

Formula-One-Home-Advantage


# Do F1 Drivers Benefit from a Home Field Advantage?

What does it take to win? While there are many factors, it would be tough to argue with the benefits of practice and repetition. These are key factors at the heart of "the home field advantage". The more an individual or team practices and competes on their home turf, the more they learn about the nuances and subtleties of their field and how to take advantage of these qualities. 

Furthermore, as athletes practice and compete over and over again in the same place their minds are unconsciously boosting performance at home due to the psychological phenomena of state dependent learning in which states that performance on a task is most effective when an individual is in the same situation, or state, as it  when the skills was learned. 

The confidence boost received from fan support during competition that can inspire and energize the athletes to better performance is another core element of the home field advantage. This project explores the question of whether the idea of a "home-field advantage" occurs in Formula One racing. Uses Python, Pandas, Numpy and MatPlotLib.

Most major sports have ample opportunity to cultivate the home field advantage.![other_sports_games](img/readme/other_sports_games.png)

Formula One is a global phenomenon and one of the most popular sports in the world (we can debate whether auto-racing is a sport in another project...). It is unique in how a season of races spans the world unlike any other major sporting competition. The F1 calendar consists of 20 races in 20 different countries, leaving driver's little opportunity to spend time on any one track. Additionally, there are strict regulations that govern how much time a driver can practice on a track as well as how much total time they are allowed to drive in the car.

![f1-2019-sched-black-blue](img/readme/f1-2019-sched-black-blue.png)

So if core repetition and familiarity components of the home field advantage are stripped away, does it still benefit F1 drivers? Is the fan support enough to keep the advantage alive?



## The Data

### Source

The data was obtained from the Kaggle Dataset <a href='https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020#constructor_results.csv'>Formula 1 World Championship (1950 - 2020)</a> and contains detailed information about every Formula 1 race since it's inaugural 1950 season up to the end of the 2019 season. During this time there were:

- 1040 Races
- 847 Drivers
- 24,600 Race results

### Data Decisions and Definitions

#### valid

valid = driver finished the race

#### 'home field'

home = driver's designated home country matched the country the race circuit was in

## Hypothesis

Remember, **a lower finishing position is better**

​	Ho: Average Finishing Position at Home = Average Finishing Position Away

​	Ha: Average Finishing Position at Home < Average Finishing Position Away	



## Analysis and Results

### Drivers' Home Country

<img src="img/driver_country_count_bar.png" alt="driver_country_count_bar" style="zoom:60%;" />



![drivers_with_home_pie](img/drivers_with_home_pie.png)



### For All Drivers Across All Seasons

![AvgDriverMeans](img/AvgDriverMeans.png)

Looking at all drivers across all 1040 races in Formula 1 history, we see that average of the finishing position at a home race is worse at 9.88 as compared to away races which had an average of 9.368. Furthermore, greater variance and standard within the home results highlights it's likelihood of greater fluctuation.

**Variance** of the average finishing result at **home**  - 21.143
**Standard Deviation** of the average finishing result at **home** -  9.881
**Variance** of the average finishing result **away** - 11.118
**Standard Deviation** of the average finishing result **away** - 9.368

![DriverAdvantageCounts](img/DriverAdvantageCounts.png)

Here we see that the number of drivers, on average, did better at home or better away. This doesn't reflect the magnitude of the difference between the two so we still don't know if there is a significant difference between the groups.

#### t-test

And finally, when we compare the average home results with the average aways results we see that at an significance level of .05 there is not a significant difference between the two groups. If anything, the difference is going in the direction of an advantage at away races.

t-test (ind) for home and away means: 

- p=0.052
- t_score=1.942

#### Home/Away Ratio (HAR)

Comparison of the ratio of drivers' finishing position at 'home' vs their finishing position 'away' produces the Home/Away Ratio (home race finishing position average / away race finishing position average)

The HAR will be smaller than 1 if the average finishing position at home is better than the away average and larger than 1 if the away average is better

![all_results_home_away_ration](img/all_results_home_away_ration.png)



##### Average HAR: 1.042

## Study Limitations

Definition of "home" refers to an entire country! For small countries this might be accurate, for large countries might be a poor definition.

Valid results could include drivers who have only competed in 2 races (1 home and 1 away), which could skew the data.

There are far more 'away' than 'home races' (### home vs ### away)

## New Directions

Each week Formula One polls fans for their favorite drivers. It would be interesting to see if there is any relationship with the fan ratings and the HAR.

























