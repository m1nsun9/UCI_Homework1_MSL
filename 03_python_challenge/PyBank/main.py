import os
import csv

# create a path to a file called 'budget_data.csv'
csv_path = os.path.join('Resources', 'budget_data.csv')

# Read and write in the CSV file
with open(csv_path, 'r+') as csv_file:
    # Split the data on commas and save to variable
    csv_reader = csv.reader(csv_file, delimiter=',')

    # Skip the header, which has column labels
    csv_header = next(csv_file)

    months = []
    net_total_pnl = 0
    average_change_pnl = 0
    greatest_increase = 0
    greatest_increase_date = ''
    greatest_decrease = 0
    greatest_decrease_date = ''

    last_profit = 0
    current_profit = 0
    net_changes = []

    # Record the following:
    for row in csv_reader:

        # The total number of months included in the dataset
        months.append(row[0])

        # The net total amount of 'Profits/Losses' over the entire period
        net_total_pnl += int(row[1])

        # calculate the average changes in Profits/Losses for each month and append to net_changes list
        current_profit = int(row[1])
        net_changes.append(int(current_profit - last_profit))

        last_profit = int(row[1])
    
    # get rid of the first item, which is not a difference of profits/losses between two months
    net_changes.pop(0)

    # The greatest increase in profits (date and amount) over the entire period
    greatest_increase = max(net_changes)
    greatest_increase_date = months[net_changes.index(greatest_increase)]

    # The greatest decrease in losses (date and amount) over the entire period
    greatest_decrease = min(net_changes)
    greatest_decrease_date = months[net_changes.index(greatest_decrease)]
    
    # The average of the changes in 'Profits/Losses' over the entire period
    average_change_pnl = "{:.2f}".format(sum(net_changes)/len(net_changes))

    # create a variable with the all the output information
    output = [
        f"Financial Analysis",
        f"----------------------------",
        f"Total Months: {len(months)}",
        f"Total: ${net_total_pnl}",
        f"Average Change: ${average_change_pnl}",
        f"Greatest Increase in Profits: {greatest_increase_date} (${greatest_increase})",
        f"Greatest Decrease in Profits: {greatest_decrease_date} (${greatest_decrease})"
    ]

    # create a text file with the output 
    analysis_path = os.path.join('Analysis', 'output.txt')
    analysis_text = open(analysis_path, 'w')
    
    # write and print final information in the output text file 
    for i in range(len(output)):
        print(output[i])
        analysis_text.write(output[i] + '\n')

    analysis_text.close()
