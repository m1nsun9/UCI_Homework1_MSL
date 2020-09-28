import os
import csv

# create a path to the election_data.csv file
election_csv_path = os.path.join('Resources', 'election_data.csv')

total_votes = 0
candidates = []
votes_won = {}
highest_votes = 0
winner = ''
 
with open(election_csv_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    # skip header
    csv_header = next(csv_file)

    # iterate through dataset 
    for row in csv_reader:

        # count total number of votes
        total_votes += 1

        # a complete list of candidates who received votes
        if row[2] not in candidates:
            # if candidate isn't in list of candidates, add to list of candidates 
            candidates.append(row[2])

            # add candidate to dictionary and add one vote 
            votes_won[row[2]] = 1
        
        # if candidate is already in list of candidates, add one vote
        else:
            votes_won[row[2]] += 1

    final_output = [
        f"Election Results",
        f"-----------------------",
        f"Total Votes: {total_votes}",
        f"-----------------------"
    ]
    
    # append a string showing each candidate's percentage of votes won and total number of votes
    for candidate in votes_won:
        percentage_votes_won = "{:.3f}".format(100 * votes_won[candidate]/total_votes)
        final_output.append(f"{candidate}: {percentage_votes_won}% ({votes_won[candidate]})")

        # if the candidate has the highest number of votes, set as winner
        if votes_won[candidate] > highest_votes:
            highest_votes = votes_won[candidate]
            winner = candidate

    # add the winner text to the final output list
    final_output.append(f"-----------------------")
    final_output.append(f"Winner: {winner}")
    final_output.append(f"-----------------------")

    # create a path to the analysis folder
    analysis_path = os.path.join('Analysis', 'output.txt')
    analysis_text = open(analysis_path, 'w')

    # print analysis of report and export a text file to 'Analysis' folder
    for i in range(len(final_output)):
        print(final_output[i])
        analysis_text.write(final_output[i] + '\n')
    
    analysis_text.close()

