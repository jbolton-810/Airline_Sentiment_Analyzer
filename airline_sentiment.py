# Airline Sentiment
# 5/4/20
# @author Jonathan Bolton

# The Airline Sentiment Analayzer program is designed to analyze an airline review dataset, and give text analysis as requested. Can be used to see review polarity of an airline over time, or polarity of airline againest other major US airlines.

import sys
import json
import textblob
import matplotlib.pyplot as plt

print("Welcome to the Airline Sentiment Analyzer\n")


#Main function asks user for an airline and checks to make sure it exsists. If so, calls analysis tree function.
def main():
    flag = False

    with open (sys.argv[1]) as input_file:
        data = json.load(input_file)
        
    user_airline = str(input("What airline would you like to analyze?\n"))

    for line in data:
        if line["airline_name"] == user_airline:
            flag = True
    if flag == True:
        analysis_tree(user_airline)
    else:            
        error_help = str(input("Error, no airline found with that name. Type 'help' to see format list of major US airlines. Type anything else to continue.\n"))
        if error_help == "help":
            airline_list = ["alaska-airlines", "allegiant-air", "american-airlines", "delta-air-lines", "frontier-airlines", "hawaiian-airlines", "jetblue-airways", "southwest-airlines", "spirit-airlines", "united-airlines"]
            for airline in airline_list:
                print(airline)
            main()
        else:
            main()


# Function for deciding what analysis type to use.
def analysis_tree(airline):
    analysis_type = str(input("What type of analysis would you like to perform? (airline info/sentiment over time/sentiment in comparison)\n"))

    if analysis_type.lower() == "airline info":
        airline_info(airline)
    elif analysis_type.lower() == "sentiment over time":
        sentiment_time(airline)
    elif analysis_type.lower() == "sentiment in comparison":
        sentiment_compare(airline)
    else:
        again = str(input("You gave an incorrect type, do you still want to choose an analysis? (yes/no)\n"))
        if again.lower() == "yes":
            analysis_tree(airline)
        else:
            continue_analysis(airline)


# Function that asks user if they want to continue. If no, exits program.
def continue_analysis(airline):
    again = str(input("Do you want to analyze " + airline + " again? (yes/no)\n"))
    
    if again.lower() == "yes":
        analysis_tree(airline)
    else:
        new = str(input("Do you want to analzye a different airline? (yes/no)\n"))
        
        if new.lower() == "yes":
            main()
        else:
            raise SystemExit


# Function that shows average sentiment and other ratings of the choosen airline.
def airline_info(airline):
    counter = 0
    rating_counter = 0
    seat_counter = 0
    staff_counter = 0
    food_counter = 0
    entertainment_counter = 0
    value_counter = 0
    polarity = 0.0
    subjectivity = 0.0
    rating = 0.0
    seat = 0.0
    staff = 0.0
    food = 0.0
    entertainment = 0.0
    value = 0.0   
 
    with open (sys.argv[1]) as input_file:
        data = json.load(input_file)
        
    for line in data:
        if line["airline_name"] == airline:
            if line["overall_rating"] is not None:
                rating = rating + line["overall_rating"]
                rating_counter = rating_counter + 1
            if line["seat_comfort_rating"] is not None:
                seat = seat + line["seat_comfort_rating"]
                seat_counter = seat_counter + 1
            if line["cabin_staff_rating"] is not None:
                staff = staff + line["cabin_staff_rating"]
                staff_counter = staff_counter + 1
            if line["food_beverages_rating"] is not None:
                food = food + line["food_beverages_rating"]
                food_counter = food_counter + 1
            if line["inflight_entertainment_rating"] is not None:
                entertainment = entertainment + line["inflight_entertainment_rating"]
                entertainment_counter = entertainment_counter + 1
            if line["value_money_rating"] is not None:
                value = value + line["value_money_rating"]
                value_counter = value_counter + 1
            counter = counter + 1
            blob = textblob.TextBlob(line["content"])
            polarity = polarity + blob.polarity
            subjectivity = subjectivity + blob.subjectivity
    
    polarity = polarity / counter
    subjectivity = subjectivity / counter
    rating = rating / rating_counter
    seat = seat / seat_counter
    staff = staff / staff_counter
    food = food / food_counter
    entertainment = entertainment / entertainment_counter
    value = value / value_counter    

    print("\nNumber of reviews found for " + airline + ": " + str(counter))
    print("Average polarity: " + str(polarity))
    print("Average subjectivity: " + str(subjectivity))
    print("Average overall rating: " + str(rating))
    print("Average seat comfort rating: " + str(seat))
    print("Average cabin staff rating: " + str(staff))
    print("Average food and beverages rating: " + str(food))
    print("Average inflight entertainment rating: " + str(entertainment))
    print("Average value money rating: " + str(value) + "\n")

    continue_analysis(airline)
    

# Function that shows polarity levels of choosen airline over a selected period of time.
def sentiment_time(airline):
    polarity = 0.0    
    review_date = 0
    polarity_list = []
    date_list = []

    boolean_start_date = input("Would you like to add a start date? (yes/no)\n")
    if boolean_start_date.lower() == "yes":
        start_date = str(input("Which start date would you like to use? (YYYYMMDD)\n"))
    else:
        start_date = "19800101"

    boolean_end_date = input("Would you like to add an end date? (yes/no)\n")
    if boolean_end_date.lower() == "yes":
        end_date = str(input("Which end date would you like to use? (YYYYMMDD)\n"))
    else:
        end_date = "20500101"

    with open (sys.argv[1]) as input_file:
        data = json.load(input_file)
        
    for line in data:
        if line["airline_name"] == airline:
            if line["date"] >= start_date and line["date"] <= end_date:
                review_date = line["date"]
                blob = textblob.TextBlob(line["content"])
                polarity = blob.polarity
                
                date_list.append(review_date)
                polarity_list.append(polarity)

                print("Polarity on " + str(review_date) + ": " + str(polarity))

    intro_title = "Polarity of " + airline + " reviews between " + str(date_list[len(date_list)-1]) + " and " + str(date_list[0])

    #Create Graph
    plt.title(intro_title)
    plt.ylabel("Polarity")
    plt.xlabel("Date")
    plt.bar(date_list, polarity_list)
    plt.xticks(rotation = 45, ha = "right")
    plt.show()

    continue_analysis(airline)


# Function that compaires polarity of choosen airline against all major US airlines.
def sentiment_compare(airline):
    airline_list = ["alaska-airlines", "allegiant-air", "american-airlines", "delta-air-lines", "frontier-airlines", "hawaiian-airlines", "jetblue-airways", "southwest-airlines", "spirit-airlines", "united-airlines"]
    polarity_list = []

    airline_list.append(airline)
    
    for line in airline_list:
        polarity = get_polarity(line)
        polarity_list.append(polarity)
        
        print(line + " polarity: " + str(polarity))    
    
    #Create Graph
    plt.title("Polarity Comparison Against Major US Airlines")
    plt.ylabel("Polarity")
    plt.xlabel("Date")
    plt.bar(airline_list, polarity_list)
    plt.xticks(rotation = 45, ha = "right")
    plt.show()

    continue_analysis(airline)


# Function that returns average polarity of given airline.
def get_polarity(airline):
    counter = 0
    polarity = 0.0

    with open (sys.argv[1]) as input_file:
        data = json.load(input_file)
        
    for line in data:
        if line["airline_name"] == airline:
            blob = textblob.TextBlob(line["content"])
            polarity = polarity + blob.polarity
            counter = counter + 1
        
    polarity = polarity / counter

    return polarity


if __name__ == '__main__':
    main()
