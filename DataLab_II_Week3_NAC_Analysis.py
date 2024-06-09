import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

file = '2022_2023_cleaned.csv'
df = pd.read_csv(file)

# Insert questions into variables because I am lazy and why bother when you can just copy/paste...
q1 = "What is the average age of players in the dataset?"
q2 = "Which team has the highest market value on average?"
q3 = "How does the market value of players correlate with their age?"
q4 = "What is the distribution of players' positions across different teams?"
q5 = "Which country has the highest representation in the dataset in terms of player birthplace?"
q6 = "Is there a correlation between a player's height and weight and the number of goals scored?"
q7 = "How does the number of goals per player vary across different positions?"
q8 = "What is the average number of matches played by players in different age groups?"
q9 = "Which players have the highest 'xG (Expected Goals)' value and how does it compare with actual goals scored?"
q10 = "What is the average contract duration left for players in each team?"
q11 = "How do 'Duels won %' and 'Aerial duels won %' vary by position?"
q12 = "Is there a significant difference in 'Successful defensive actions per 90' between players on loan and permanent players?"
q13 = "Which players have the highest 'Successful attacking actions per 90' and which position do they play?"
q14 = "What is the relationship between 'Goals per 90' and 'Assists per 90' for forwards?"
q15 = "Which players exceed in 'Shots on target %' and how does it relate to their overall 'Goal conversion %'?"
q16 = "How do 'Passes per 90' and 'Accurate passes %' correlate for midfielders?"
q17 = "Is there a trend in the 'Save rate %' for goalkeepers across different age groups?"
q18 = "What is the distribution of 'Yellow cards per 90' and 'Red cards per 90' across different positions?"
q19 = "How does 'Fouls suffered per 90' compare for attackers and defenders?"
q20 = "Which players have the highest 'Penalty conversion %' and what are their overall shooting statistics?"


st.title('NAC Data Analysis')
st.write('To get a sneak-peek into the different insights we can gather from the data set, we will need to visualize some of the data so it can be understood easily. We will ask some questions and answer these to make the process understandable.\n\n')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header(f'**{q1}**')

average_age = round(df['Age'].mean())
st.write(f'The average age for football players in the current dataset is: {average_age}')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 2
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q2}**')

market_value = df[df["Market value"] != 0]     # Remove players with no market value because they mess up the average
market_value = market_value.groupby('Team')['Market value'].mean()
id_max = market_value.idxmax()
max = market_value.max()
st.write(f"The team with the highest average market value is: {id_max}, with an average value of: {max:,.2f}")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 3
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q3}**')

age_by_marketvalue = df[df['Market value'] != 0]      # remove players with no market value because they mess up the average
st.write(f"The correlation coefficient for the two series is: {age_by_marketvalue['Age'].corr(age_by_marketvalue['Market value'])}. Indicating there is little to no correlation between the two. Though i would beg to differ, and I will show you why:")

grouped_by_age = age_by_marketvalue.groupby('Age')
plt.bar(grouped_by_age.groups.keys(), grouped_by_age['Market value'].mean(), color='r')
plt.title('Average market value of football players by age')
plt.xlabel('Age')
plt.ylabel('Average Market value')
st.pyplot(plt, clear_figure=True)

st.write("As can be seen in the chart above, it seems that beyond the age of 16, the younger the player, the higher the average price, but it's not a very strong correlation, so indeed a weak negative correlation.")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 4
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q4}**')

grouped_by_category = df.groupby('Position category')
plt.pie(grouped_by_category['Team'].count(), labels=grouped_by_category.groups.keys(), autopct='%1.0f%%')
plt.title("Distribution of players' positions")

st.pyplot(plt, clear_figure=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 5
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q5}**')

countrylist = df['Birth country'].value_counts()
countrylist.sort_values(ascending=False)
st.write(countrylist)
st.write(f"As can be seen in the table above, within the dataset, the country with the highest representation is {countrylist.index[0]}")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 6
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q6}**')

df_hw_del = df[(df['Height'] != 0) & (df['Weight'] != 0)]   # Exclude heights and weights that are not recorded.

fig, ax = plt.subplots(2,1, constrained_layout=True)

# plot 1 // height
ax[0].plot(df_hw_del.groupby('Height')['Goals'].mean())
ax[0].set_xlabel('Length in cm')

# plot 2 // weight
ax[1].plot(df_hw_del.groupby('Weight')['Goals'].mean())
ax[1].set_xlabel('Weight in Kg')

# Common label for the y axis
fig.supylabel('Average scored Goals')

st.pyplot(fig, clear_figure=True)

st.write(f"As can be seen above, there seems to be little relation between the number of goals scored and the height and weight of the player. this can also be evidenced by the correlation coefficient for both:")
st.write(f"The correlation coefficient for Height X Goals is: {round(df_hw_del['Height'].corr(df_hw_del['Goals']), 4)}")
st.write(f"The correlation coefficient for Weight X Goals is: {round(df_hw_del['Weight'].corr(df_hw_del['Goals']), 4)}")
st.write('Meaning there is a weak negative relation between the both of them and the number of goals scored')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 7
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q7}**')

grouped_by_position = df.groupby('Position')
plt.bar(grouped_by_position.groups.keys(), grouped_by_position['Goals'].mean(), color='purple')

plt.xticks(rotation='vertical')
plt.xlabel('Positions')
plt.ylabel('Average number of goals per player')

st.pyplot(plt, clear_figure=True)

st.write('As expected, the attacking positions have been shown to have the best averages overall.')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 8
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q8}**')

plt.bar(grouped_by_age.groups.keys(), grouped_by_age['Matches played'].mean())

plt.xlabel('Age')
plt.ylabel('Average number of played matches')

st.pyplot(plt, clear_figure=True)

st.write(f"As you can see in the graph above, there does seem to be a relationship between the average number of played matches and the age groups. Meaning players below 21 are far more likely to have played less matches than the rest, and players above 37 are more likely to have played more, but within that range, the average doesn't seem to vary a whole lot.")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 9
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q9}**')

st.write(df[['Player', 'Position', 'xG', 'Goals', 'Goals per 90', 'Matches played']].sort_values(by=['xG'], ascending=False).head(5))

plt.scatter(df['xG'], df['Goals'])
plt.xlabel('xG (Expected Goals)')
plt.ylabel('Actual amount of goals per player')

st.pyplot(plt, clear_figure=True)

st.write(f"As can be seen in both the table and  the scatterplot: The xG is nearly correlated to the amount of goals of a player with a correlation coefficient of: {round(df['xG'].corr(df['Goals']), 4)}")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 10
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q10}**')

only_contracted = df[df['Contract expires'] != None]
only_contracted['Contract expires'] = pd.to_datetime(only_contracted['Contract expires'])

mean_enddate = (only_contracted['Contract expires'] - only_contracted['Contract expires'].min()).mean() + only_contracted['Contract expires'].min()
today_date = datetime.today()

time_left = mean_enddate - today_date
mean_enddate = datetime.strftime(mean_enddate, "%d/%m/%Y")
                
st.write(f"Taken into account all contract enddates, the average enddate for contracts within the dataset is: {mean_enddate}. Meaning the average length is {str(time_left)[:8]} from today.")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 11
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q11}**')

if 'button' not in st.session_state:
    st.session_state.button = False
    buttonText = "Show Aerial Duels Graph"

def click_button():
    st.session_state.button = not st.session_state.button

if st.session_state.button:
    buttonText = "Show Duels Graph"
    plt.bar(grouped_by_position.groups.keys(), grouped_by_position['Aerial duels won, %'].mean(), color='purple')
    plt.xticks(rotation='vertical')
    plt.xlabel('Positions')
    plt.ylabel('Average percentage of aerial duels won per player')
    plt.title('Aerial Duels')
    st.pyplot(plt, clear_figure=True)
else:
    buttonText = "Show Aerial Duels Graph"
    plt.bar(grouped_by_position.groups.keys(), grouped_by_position['Duels won, %'].mean(), color='purple')
    plt.xticks(rotation='vertical')
    plt.xlabel('Positions')
    plt.ylabel('Average percentage of duels won per player')
    plt.title('Duels')
    st.pyplot(plt, clear_figure=True)

st.button(buttonText, on_click=click_button)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 12
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q12}**')

# Done like this because of the low speed when doing it otherwise...
grouped_by_loan = df.groupby('On loan')

plt.bar(grouped_by_loan.groups.keys(), grouped_by_loan['Successful defensive actions per 90'].mean(), color='r')
plt.title('Average succeccful defensive actions per 90 by Loan-status')
plt.ylabel('Average defensive actions per 90')
plt.xticks([0, 1], ['Players not on loan', 'Players on loan'])

st.pyplot(plt, clear_figure=True)

st.write('As can be seen above, there is little to no difference if the player is on a loan or not.')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 13
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q13}**')

st.write(df[['Player', 'Team', 'Position', 'Successful attacking actions per 90']].sort_values(by=['Successful attacking actions per 90'], ascending=False).head(5))


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 14
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q14}**')

filter_by_position = df[df['Position category'] == 'AT']
plt.scatter(filter_by_position['Goals per 90'], filter_by_position['Assists per 90'])

st.pyplot(plt, clear_figure=True)

st.write(f'As can be evidenced by the scatterplot above and athe correlation coefficient bteween the two variables: {round(filter_by_position["Assists per 90"].corr(filter_by_position["Goals per 90"]), 2)}. There is little to no relation between the two.')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 15
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q15}**')

no_0_goal = df[df['Goal conversion, %'] != 0]
st.write(df[['Player', 'Team', 'Position', 'Shots on target, %', 'Goal conversion, %']].sort_values(by=['Shots on target, %'], ascending=False).head(5))
st.write("As can be seen above, the players with the highest percentage of shots on target have a goal conversion of 0, meaning they haven't scored any, which incidentally gives them a 100 on shots on target. Below can be seen the updated table with no 0-values in the goal conversion.")
st.write(no_0_goal[['Player', 'Team', 'Position', 'Shots on target, %', 'Goal conversion, %']].sort_values(by=['Shots on target, %'], ascending=False).head(5))
st.write("Above can be seen that most players with a high shots on target percentage are either goal keepers or corner-backs, which on average don't make a lot of goals or shots, for that matter.")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 16
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q16}**')

only_midfield = df[df['Position category'] == 'MF']
only_midfield = only_midfield[(only_midfield['Passes per 90'] != 0) & (only_midfield['Accurate passes, %'] != 0)]
plt.scatter(only_midfield['Passes per 90'], only_midfield['Accurate passes, %'])
plt.xlabel('Passes per 90')
plt.ylabel('Accurate passes, %')

st.pyplot(plt, clear_figure=True)

st.write(f"As can be seen in the plot above, and as can be evidenced by the correlation coeffictient: {round(only_midfield['Accurate passes, %'].corr(only_midfield['Passes per 90']), 2)}. There seems to be a moderate positive relationship between the two variables.")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 17
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q17}**')

only_goalie = df[df['Position category'] == 'GK']
keeper_grouped_by_age = only_goalie.groupby('Age')
plt.plot(keeper_grouped_by_age.groups.keys(), keeper_grouped_by_age['Save rate, %'].mean())
plt.xlabel('Age')
plt.ylabel('Save rate, %')

st.pyplot(plt, clear_figure=True)
st.write('No, there does not seem to be much of a trend.')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 18
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q18}**')

mean_red_cards = grouped_by_position['Red cards per 90'].mean()
mean_yellow_cards = grouped_by_position['Yellow cards per 90'].mean()

plt.plot(grouped_by_position.groups.keys(), mean_red_cards, mean_yellow_cards)

plt.title('Mean Red and Yellow Cards per 90 by Position')
plt.xlabel('Position')
plt.ylabel('Mean Cards per 90')
plt.legend(['Red cards', 'Yellow cards'])

st.pyplot(plt, clear_figure=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 19
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q19}**')

only_att_df = df[(df['Position category'] == 'AT') | (df['Position category'] == 'DF')].groupby('Position category')

plt.bar(only_att_df.groups.keys(), only_att_df['Fouls per 90'].mean(), color='green')
plt.ylabel('Average Fouls suffered per 90')

st.pyplot(plt, clear_figure=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Question 20
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('---')
st.header(f'**{q20}**')

st.write(df[['Player', 'Team', 'Position', 'Penalty conversion, %', 'Penalties taken', 'Goal conversion, %', 'Shots on target, %']].sort_values(by=['Penalty conversion, %'], ascending=False).head(5))
