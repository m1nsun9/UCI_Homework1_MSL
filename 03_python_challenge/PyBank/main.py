import os
import csv

# create a path to a file called 'budget_data.csv'
csv_path = os.path.join('Resources', 'budget_data.csv')

# Read in the CSV file
with open(csv_path, 'r+') as csv_file:
    # Split the data on commas and save to variable
    csv_reader = csv.reader(csv_file, delimiter=',')

    # Skip the header, which has column labels
    csv_header = next(csv_file)

    total_months = 0
    net_total_pnl = 0
    average_change_pnl = 0
    greatest_increase = 0
    greatest_increase_date = ''
    greatest_decrease = 0
    greatest_decrease_date = ''

    # Record the following:
    for row in csv_reader:

        # The total number of months included in the dataset
        total_months += 1

        # The net total amount of 'Profits/Losses' over the entire period
        net_total_pnl += int(row[1])
        
        # The greatest increase in profits (date and amount) over the entire period
        if int(row[1]) > greatest_increase:
            greatest_increase = int(row[1])
            greatest_increase_date = row[0]

        # The greatest decrease in losses (date and amount) over the entire period
        if int(row[1]) < greatest_decrease:
            greatest_decrease = int(row[1])
            greatest_decrease_date = row[0]
    
    # The average of the changes in 'Profits/Losses' over the entire period
    average_change_pnl = "{:.2f}".format(net_total_pnl/total_months)

    # create a variable with the all the output information
    output = [
        f"Financial Analysis",
        f"----------------------------",
        f"Total Months: {total_months}",
        f"Total: ${net_total_pnl}",
        f"Average Change: ${average_change_pnl}",
        f"Greatest Increase in Profits: {greatest_increase_date} (${greatest_increase})",
        f"Greatest Decrease in Profits: {greatest_decrease_date} (${greatest_decrease})"
    ]

    # create a text file with the output 
    output_path = os.path.join('..', 'Analysis', 'output.txt')
    output_text = open(output_path, 'w')
    
    for i in range(len(output)):
        print(output[i])
        output_text.write(output[i] + '\n')
