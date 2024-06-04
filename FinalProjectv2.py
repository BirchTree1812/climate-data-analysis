import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys


# this function is useful for all the other tasks, as it loads the data for weather and for the city names
def load_data(file_path, temp_cols, city_col):
    weather_array = np.loadtxt(file_path, delimiter = ',', usecols = temp_cols, skiprows = 1, dtype = 'float')
    city_array = np.loadtxt("data_temperature.txt", delimiter = ',', usecols = city_col, skiprows = 1, dtype = 'str')
    day_array = np.loadtxt("data_temperature.txt", delimiter = ',', usecols = 0, skiprows = 1, dtype = 'str')
    return weather_array, city_array, day_array

# Uses the load_data function to create arrays for weather variables and for the city names
def city_data_preparation():
    temp_cols=[2,3,4,5, 6, 7]
    city_col=[1]
    weather_array, city_array, day_array = load_data("data_temperature.txt", temp_cols, city_col)
    # creates an empty list that contains the names of all cities in the document
    citylist=[]
    # initializes cityname before the loop. This is to make sure that the first city
    # in the document will always be added
    cityname=""
    # these lines create arrays out of columns for max temperature, minimum temperature, precipitation and wind speed
    maxtemp = weather_array[:, 0]
    mintemp = weather_array[:, 1]
    precipitation=weather_array[:, 2]
    windspeed=weather_array[:, 3]
    humidity=weather_array[:,4]
    cloudcover=weather_array[:,5]
    # loop that combs through the column with city names
    # and outputs the names of all the mentioned cities into a list citylist
    for city in city_array:
        if city!=cityname:
            citylist.append(city)
            cityname=city
    datalist=[citylist, maxtemp, mintemp, precipitation, windspeed, humidity, cloudcover]
    return datalist

# This function solves exercises 2 and 3, because both these exercises are similar
def city_wise_analysis():
    # declares the list of data from the previous function
    datalist=city_data_preparation()
    # initializes lists for monthly average temperatures
    monthlyavgmaxlist=[]
    monthlyavgminlist=[]
    totalpreciplist=[]
    maxwindlist=[]
    minwindlist=[]
    humidlist=[]
    cloudcovlist=[]
    monthavglists=[monthlyavgmaxlist,monthlyavgminlist, totalpreciplist, maxwindlist, minwindlist,
                   humidlist, cloudcovlist]
    # this loop returns the total precipitation, average max and min temperatures
    # and the maximum wind speed for each city
    for city in range(0,10):
        # the two lines that return total precipitation.
        # For each city, cuts the column with precipitation into slices of 31 days,
        # with each iteration moving to the next city
        cityprecip=datalist[3][(city)*31:(city+1)*31]
        totalprecip=cityprecip.sum()
        totalpreciplist.append(totalprecip)
        # the 4 lines that return averages of maximum and minimum temperatures
        monthmax=datalist[1][(city)*31:(city+1)*31]
        monthmin = datalist[2][(city) * 31:(city + 1) * 31]
        monthlyavgmax=monthmax.mean()
        monthlyavgmaxlist.append(monthlyavgmax)
        monthlyavgmin = monthmin.mean()
        monthlyavgminlist.append(monthlyavgmin)
        # returns maximum and minimum wind speed
        citywindspeed=datalist[4][(city)*31:(city+1)*31]
        maxwind=citywindspeed.max()
        maxwindlist.append(maxwind)
        minwind=citywindspeed.min()
        minwindlist.append(minwind)
        humid=datalist[5][(city)*31:(city+1)*31]
        humidavg=humid.mean()
        humidlist.append(humidavg)
        cloudcov=datalist[6][(city)*31:(city+1)*31]
        cloudcovavg = cloudcov.mean()
        cloudcovlist.append(cloudcovavg)
    return monthavglists

# actual solution to exercise 2
def weather_data_print():
    monthavglists = city_wise_analysis()
    datalist = city_data_preparation()
    # these lines print the results for each city
    for city in range(0, 10):
        print("Average maximum and average minimum temperatures of",datalist[0][city],
              "in January are", "%.2f" % monthavglists[0][city],"and", "%.2f" % monthavglists[1][city],"degrees",sep=" ")
        print("Total precipitation in",datalist[0][city],"in January is", "%.2f" % monthavglists[2][city], "mm",sep=" ")
        print("Maximum and minimum wind speeds in",datalist[0][city],"in January are", "%.2f" % monthavglists[3][city],
              "and", monthavglists[4][city],"km/s",sep=" ")

# function for exercise 3
def weather_graph():
    monthavglists = city_wise_analysis()
    datalist = city_data_preparation()
    x_axis_data=list(range(1,32))
    # these lines of code allow to create a bar chart and a line chart each for maximum and minimum temperature.
    templist=[datalist[1],datalist[2]]
    tempnames=["Maximum temperature(C)","Minimum temperature(C)"]
    # sets window size, applies it to all the graphs
    mpl.rcParams['figure.figsize'] = (12, 6)
    # loop that generates the 2 charts for 10 cities.
    for temptype in range(0,2):
        # initializes the line charts for maximum and minimum temperature
        fig, ax = plt.subplots()
        ax.grid()
        # plots 10 plots, one for each city
        for city in range(0,10):
            # applies y-axis data for each city, cutting out the right chunk of data
            # from the respective temperature array using the slicer
            y_axis_data=templist[temptype][(city)*31:(city+1)*31]
            # sets up data labels and legend
            ax.plot(x_axis_data, y_axis_data, label=datalist[0][city])
            ax.legend()
        # more labels, but these apply to the whole graph, rather than each city
        title = tempnames[temptype]+" in January for each city"
        ax.set(xlabel="Days in January", ylabel=tempnames[temptype],
               title=title)
        savename = "test"+str(temptype)+".png"
        fig.savefig(savename)
    # sets 10 bar colors, one for each bar
    bar_colors = [(1, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0), (0, 0, 0)]
    # loop that creates one bar chart for max temperature and one bar chart for minimum temperature
    for i in range(0,2):
        # initialize graph
        fig, ax = plt.subplots()
        # make bars. citylist represents all the cities that are in the chart,
        # monthavglists represents whether to use the maximum or minimum temperature
        ax.bar(datalist[0], monthavglists[i], label=datalist[0], color=bar_colors)
        # sets up more labels, depending on whether it's max or min temperature
        ax.set_ylabel(tempnames[i])
        axtitle = tempnames[i]+" over January"
        ax.set_title(axtitle)
        ax.grid()
        ax.legend(title='City')
        savename = "bartest" + str(i) + ".png"
        fig.savefig(savename)
    plt.show()


# exercise 4
temp_cols = [2, 3]
city_col = [1]
days = ["2023-01-{:02d}".format(day) for day in range(1, 32)]
cities = ["New York", "Los Angeles", "London", "Tokyo", "Beijing", "Sydney", "Paris", "Berlin", "Cairo", "New Delhi"]

def load_data2(file_path, temp_cols, city_col):
    temp_array = np.loadtxt("data_temperature.txt", delimiter = ',', usecols = temp_cols, skiprows = 1, dtype = 'int')
    city_array = np.loadtxt("data_temperature.txt", delimiter = ',', usecols = city_col, skiprows = 1, dtype = 'str')
    return temp_array, city_array

def segregate_data(temp_array):
    city_temps = {}
    for i, city in enumerate(cities):
        start_index = i * 31
        end_index = (i + 1) * 31
        city_temps[city] = temp_array[start_index:end_index]
    return city_temps

def compute_averages(city_temps):
    city_day_averages = {city : np.mean(city_temps[city], axis=1) for city in cities}
    city_month_averages = {city : np.mean(city_day_averages[city]) for city in cities}
    return city_day_averages, city_month_averages

def daily_temperature_analysis(city, days_temp_average, month_temp_average):
    print(f"Daily temperature analysis of {city} in January 2023:")
    for i, day_temp in enumerate(days_temp_average):
        if day_temp < month_temp_average:
            print(days[i], ": Cold")
        elif day_temp > month_temp_average:
            print(days[i], ": Warm")
        else:
            print(days[i], ": Moderate")

# initializes data after the functions for task 4, necessary to run those functions
temp_array, city_array = load_data2("data_temperature.txt", temp_cols, city_col)
city_temps = segregate_data(temp_array)
city_day_averages, city_month_averages = compute_averages(city_temps)

# this function solves task 5.
def paris_global_warming():
    # columns of the text file that will become part of the array
    colread=[2,3,4,5,6,7,8,9]
    # turns the text file into the array, ignoring the first row and the first two columns
    # due to them not being decimal numbers
    data_array = np.loadtxt("Paris_data_climate.txt", delimiter=',', usecols=colread, skiprows=1, dtype='float')
    # defined each column as its own 1D array, so that I can more easily make graphs with it.
    maxtemp=data_array[:,0]
    mintemp=data_array[:,1]
    precip=data_array[:,2]
    co2level=data_array[:, 6]
    searise=data_array[:, 7]
    # put all the columns in a list, also made a list with proper names to display for each of those columns' values
    # both for weather values(y-axis) and the global warming values(x-axis)
    y_columns=[maxtemp, mintemp, precip, co2level, searise]
    y_column_names=["Max temperature(C)","Min temperature(C)","Precipitation(mm)", "CO2 Levels(ppm)","Sea Level Rise(mm)"]
    x_columns=list(range(1,32))
    # nested loop that creates a line graph of weather values against CO2 Levels and Sea Level Rise
    fig, ax = plt.subplots()
    ax.grid()
    for ycolumn in range(0,4):
        ax.plot(x_columns, y_columns[ycolumn],label= y_column_names[ycolumn])
        ax.legend()
    ax.set(xlabel="Time", ylabel="Values",
           title="Graph of weather values over January")

    fig, ax = plt.subplots()
    ax.grid()
    for ycolumn in range(0,5):
        if ycolumn == 3:
            continue
        ax.plot(x_columns, y_columns[ycolumn], label=y_column_names[ycolumn])
        ax.legend()
    # part of the first loop, creates a title and labels for each graph
    ax.set(xlabel="Days in January", ylabel="Values",
           title="Graph of weather values over January")
    fig.savefig("seatest.png")
    plt.show()
    # The weather values' relation to the global warming variables is weak positive linear
    # But how to find the correlation?


# this function solves problem 6, letting a user type the name
def user_interface(cityname):
    datalist = city_data_preparation()
    monthavglists = city_wise_analysis()
    statlist = ["Max Temperature (C)", "Min Temperature (C)", "Total Precipitation (mm)", "Max Wind Speed (km/h)",
                "Min Wind Speed (km/h)", "Humidity(%)", "Cloud Cover(%)"]
    # sets the 'found' bool as false in the beginning. If the city is found, the bool is set to true.
    # Otherwise, prints the error message
    found = False
    # loops across the entire list of cities to see if the city written by the user belongs there
    for city in datalist[0]:
        # if the list belongs there, then print its statistics
        if cityname == city:
            citynum = datalist[0].index(city)
            for statistic in range(0,7):
                value = monthavglists[statistic][citynum]
                print(statlist[statistic], "%.2f" % value)
            print(cityname)
            found = True
    # if the name is not in the city list, prints the error message, along with the list of correct names for the cities
    if found is False:
        print("This city is not available. Here's the list of cities that we do have", datalist[0])


# The code that makes sure the user can choose whichever function they want to run from the console.
# If the function is user_interface, then the user has also type in the name of the city.
# for example, to run user_interface for the data of New Delhi, type in:
# python3 FinalProject.py 6 "New Delhi"
print("Select a function from this file:\n"
      "2 - print average max/min temperature, total precipitation, max/min windspeed for each of the 10 cities\n"
      "3 - plot graphs for max/min of 10 cities in January\n"
      "4 - execute different data functions\n"
      "5 - plot graphs that compare weather variables and climate change data in Paris over January\n"
      "6 - select a city and print its weather data")

function_name = input("Choose a number between 2 and 6\n")
if function_name == "2":
    weather_data_print()
elif function_name == "3":
    weather_graph()
elif function_name == "4":
    for city in cities:
        daily_temperature_analysis(city, city_day_averages[city], city_month_averages[city])
elif function_name == "5":
    paris_global_warming()
elif function_name == "6":
    cityname = input("Select the city name\n")
    user_interface(cityname)
else:
    print("Invalid function name. Please choose from a number between 2 and 6")
    sys.exit(1)



#for city in cities:
#    daily_temperature_analysis(city, city_day_averages[city], city_month_averages[city])


#user_interface(sys.argv[1])
#if len(sys.argv) != 2:
#    print("Perhaps you inserted too many or too few arguments. "
#          "Make sure you write your city's name and enclose it in quotation marks.")