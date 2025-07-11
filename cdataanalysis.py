import json
import numpy as np
import pandas as pd

class CricketStatsAnalyzer:
    def __init__(self, batting_filename=None, bowling_filename=None):
        self.batting_filename = batting_filename
        self.bowling_filename = bowling_filename

    def load_data_from_json(self, filename):
        try:
            # Open the JSON file and load the data
            with open(filename, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            # Handle file not found error
            print(f"File {filename} not found.")
            return None
        except Exception as e:
            # Handle other exceptions
            print(f"Error occurred while loading data from {filename}: {e}")
            return None

    def get_top_players(self, data, key, limit=5):
        all_players = {}
        # Iterate through the data
        for entry in data:
            if 'battingSummary' in entry:
                for player in entry['battingSummary']:
                    if player['batsmanName'] in all_players:
                        # If the player already exists in the dictionary, update their stats
                        if key in player:
                            all_players[player['batsmanName']][key] += float(player[key])
                        else:
                            all_players[player['batsmanName']][key] = 0
                    else:
                        # If the player is not in the dictionary, add them with their stats
                        if key in player:
                            all_players[player['batsmanName']] = {key: float(player[key])}
                        else:
                            all_players[player['batsmanName']] = {key: 0}
        
        # Sort the players based on the given key and limit the results
        sorted_players = sorted(all_players.items(), key=lambda x: x[1][key], reverse=True)[:limit]
        return sorted_players

    def get_top_bowlers(self, data, limit=5):
        all_bowlers = {}
        # Iterate through the data
        for entry in data:
            if 'bowlingSummary' in entry:
                for bowler in entry['bowlingSummary']:
                    if bowler['bowlerName'] in all_bowlers:
                        # If the bowler already exists in the dictionary, update their stats
                        if bowler['wickets'].isdigit():  # Check if wickets value is a digit
                            all_bowlers[bowler['bowlerName']]['wickets'] += int(bowler['wickets'])
                        overs = float(bowler['overs'])
                        runs = float(bowler['runs'])
                        economy_rate = runs / overs if overs != 0 else 0
                        all_bowlers[bowler['bowlerName']]['economy'] += economy_rate
                    else:
                        # If the bowler is not in the dictionary, add them with their stats
                        if bowler['wickets'].isdigit():  # Check if wickets value is a digit
                            all_bowlers[bowler['bowlerName']] = {'wickets': int(bowler['wickets']), 'economy': 0}
                        else:
                            all_bowlers[bowler['bowlerName']] = {'wickets': 0, 'economy': 0}  # If wickets not present
                        overs = float(bowler['overs'])
                        runs = float(bowler['runs'])
                        economy_rate = runs / overs if overs != 0 else 0
                        all_bowlers[bowler['bowlerName']]['economy'] += economy_rate
        
        # Sort the bowlers based on wickets and economy rate, and limit the results
        sorted_bowlers = sorted(all_bowlers.items(), key=lambda x: (x[1]['wickets'], x[1]['economy']), reverse=True)[:limit]
        return sorted_bowlers

    def display_top_players(self, players, key):
        # Display the top players with the specified key
        print(f"Top 5 players with the highest {key}:")
        for i, (player, stats) in enumerate(players, 1):
            print(f"{i}. {player}: {stats[key]:.2f} {key}")
        print()

    def main(self):
        if not self.batting_filename or not self.bowling_filename:
            # Check if filenames are provided
            print("File names not provided.")
            return
        
        # Load batting and bowling data from JSON files
        batting_data = self.load_data_from_json(self.batting_filename)
        if not batting_data:
            return
        bowling_data = self.load_data_from_json(self.bowling_filename)
        if not bowling_data:
            return
        
        while True:
            # Display menu options
            print("Menu:")
            print("1. Top 5 players with highest runs")
            print("2. Top 5 players with highest wickets")
            print("3. Top 5 most economical bowlers")
            print("4. Top 5 players with most 4s")
            print("5. Top 5 players with most 6s")
            print("6. Exit")    
            
            # Prompt user for choice
            choice = input("Enter your choice: ")
            
            if choice == '1':
                # Get and display top players with highest runs
                top_runs_players = self.get_top_players(batting_data, 'runs')
                self.display_top_players(top_runs_players, 'runs')
            elif choice == '2':
                # Get and display top bowlers with highest wickets
                top_wickets_players = self.get_top_bowlers(bowling_data)
                self.display_top_players(top_wickets_players, 'wickets')
            elif choice == '3':
                # Get and display top economical bowlers
                top_economical_bowlers = self.get_top_bowlers(bowling_data)
                self.display_top_players(top_economical_bowlers, 'economy')
            elif choice == '4':
                # Get and display top players with most 4s
                top_4s_players = self.get_top_players(batting_data, '4s')
                self.display_top_players(top_4s_players, '4s')
            elif choice == '5':
                # Get and display top players with most 6s
                top_6s_players = self.get_top_players(batting_data, '6s')
                self.display_top_players(top_6s_players, '6s')
            elif choice == '6':
                # Exit the program
                print("Exiting the program...")
                break
            else:
                # Handle invalid choice
                print("Invalid choice. Please enter a valid option.\n")

if __name__ == "__main__":
    # Create an instance of CricketStatsAnalyzer and run the main function
    analyzer = CricketStatsAnalyzer("batting_data.json", "bowling_data.json")
    analyzer.main()
