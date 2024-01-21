# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:45:56 2024

@author: Bhaskar Teja Ulichi

Before running this script, make sure to install the required packages:
- pandas: pip install pandas
- requests: pip install requests
- beautifulsoup4: pip install beautifulsoup4
- validators: pip install validators
"""
#Load the required Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import os
import validators

#Defining each function forming part of the main program
def create_wishlist():
    print("\nWelcome to the WishList Creator. \nThis wizard will assist you in creating your personalized WishLists.")
    print("\nAre a book worm? You like to buy tons of books but not right away?\nYou have come to the right place.")
    print("\nAll we need is the Book Name, its link and the price you wish to buy it for.")
    print("Wondering if you have to give the exact name? \nNo worries, just type how you like to remember.")
    print("\nNOTE: Currently this tool supports only the following website(s)\nhttps://books.toscrape.com/")

    # Initialize an empty list to store book names, URLs, and Desired Prices
    wishlist_data = []

    book_count = 0  # Track the number of books added

    while True:
        book_name = input(
            "Please type the book's name (Press 'ENTER' key to finish): ")

        if not book_name:
            # If the user pressed Enter, ask for Local Path and File Name
            print("\nGreat! What do you want to call this WishList? \nPlease enter a file name (without any extension)")
            file_name = input(
                "Please set the WishList name: ") or 'DefaultWishList'
            local_path = input(
                "\nYou are almost set. \nPlease enter the Storage Path for your WishList : ")

            # Set the default path if the user input is empty or invalid
            if not local_path or not os.path.exists(local_path):
                local_path = "C:\\Users\\Public\\Documents"
                print(
                    f"Invalid path or empty input. Setting default path to: {local_path}")

            # Create a CSV file with book names, URLs, and Desired Prices
            csv_file_path = f"{local_path}/{file_name}.csv"
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Book Name', 'URL', 'Desired Price'])
                csv_writer.writerows(wishlist_data)

            print(f"{book_count} book(s) have been successfully added to {file_name}.csv. "
                  f"\nYour Wishlist {file_name}.csv has been successfully saved in the path {local_path}")

            while True:
                print("\nHow else can I assist you?")
                print(
                    "Options:\n1. Create another WishList\n2. Track a WishList?\n3. Exit")
                track_option = input("Enter your choice (1 or 2 or 3): ")
                if track_option == '1':
                    create_wishlist()
                elif track_option == '2':
                    track_wishlist()
                elif track_option == '3':
                    print("Thanks for using WishList Creator. \nCheers!")
                    return
                else:
                    print("I am sorry. Please select either 1 or 2 or 3.")

        else:
            url = input(f"Please enter the URL of the book '{book_name}': ")

            # Validate the URL
            if not validators.url(url):
                print(
                    "This book will not be added to your wishlist because you entered an invalid URL.")
                continue

            desired_price = input(
                f"Please enter the Desired Price for the book '{book_name}': ")

            # Validate the Desired Price
            try:
                desired_price = float(desired_price)
                if desired_price < 0:
                    raise ValueError
            except ValueError:
                print("This book will not be added to your wishlist because you entered an invalid input."
                      "\nDesired Price can only be a positive numeric value.")
                continue

            wishlist_data.append([book_name, url, desired_price])
            book_count += 1  # Increment book count for each valid entry


def add_books_to_wishlist(csv_file_path):
    print("\nLet's add more books to your WishList! \nAll we need is the Book Name, its link and the price you wish to buy it for.")
    print("Wondering if you have to give the exact name? \nNo worries, just type how you like to remember.")

    wishlist_data = []
    books_added = 0  # Track the number of books added

    while True:
        book_name = input(
            "Please type the book's name (Press ENTER to finish): ")

        if not book_name:
            break

        url = input(f"Please enter the URL of the book '{book_name}': ")

        # Validate the URL
        if not validators.url(url):
            print(
                "This book will not be added to your wishlist because you entered an invalid URL.")
            continue

        while True:
            desired_price = input(
                f"Please enter the Desired Price for the book '{book_name}': ")

            # Validate the Desired Price
            try:
                desired_price = float(desired_price)
                if desired_price < 0:
                    raise ValueError
                break  # Break out of the loop if validation is successful
            except ValueError:
                print(
                    "Please enter a valid positive numeric value for the Desired Price.")

        wishlist_data.append([book_name, url, desired_price])
        books_added += 1  # Increment book count for each valid entry

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(wishlist_data)

    print(
        f"\n{books_added} new book(s) have been successfully added to your WishList.")


def delete_books_from_wishlist(csv_file_path):
    # Extract the file name from the csv_file_path
    file_name = os.path.basename(csv_file_path).split('.')[0]

    wishlist_data = pd.read_csv(csv_file_path)

    print("\nHere are the books that are currently in your WishList:")
    print(wishlist_data['Book Name'].to_string(index=False))

    books_to_delete = input(
        "Please type the book(s) you want to delete (comma-separated): ").split(',')

    # Get the number of books before deletion
    num_books_before = len(wishlist_data)

    wishlist_data = wishlist_data[~wishlist_data['Book Name'].isin(
        books_to_delete)]
    wishlist_data.to_csv(csv_file_path, index=False)

    # Get the number of books after deletion
    num_books_after = len(wishlist_data)

    # Calculate the number of books deleted
    num_books_deleted = num_books_before - num_books_after

    print(f"\n{num_books_deleted} book(s) have been successfully removed from '{file_name}'.csv")


def edit_wishlist():
    print("\nWelcome to the WishList Editor. \nModify your existing WishLists with ease.")

    # Prompt the user for the local path and CSV file name
    local_path = input(
        "Please enter the Local Path of the wishlist you want to modify: ")
    file_name = input("Please enter the WishList name (without extension): ")
    csv_file_path = f"{local_path}/{file_name}.csv"

    # Check if the CSV file exists
    if not os.path.isfile(csv_file_path):
        print(
            f"\nSorry. The file {file_name}.csv cannot be found in {local_path}. \nNote: WishList Editor can only modify CSV files. \nPlease check the file path and file name.")
        return

    while True:
        # Display options to the user
        print(
            f"\nPlease select the changes you would like to make to {file_name}.csv")
        print("1. Add books")
        print("2. Delete books")
        print("\nPress ANY OTHER KEY to exit the program.")
        user_choice = input("\nEnter your choice: ")

        if user_choice == '1':
            # Add books to the wishlist
            add_books_to_wishlist(csv_file_path)

            # Ask if the user wants to delete any books
            delete_option = input(
                "\nDo you want to delete any books? \nPlease type 1 to delete book(s). \nPress ANY OTHER KEY to exit. \nYour Choice: ")

            if delete_option == '1':
                # Delete books from the wishlist
                delete_books_from_wishlist(csv_file_path)
                print("\nThanks for using WishList Editor. \nCheers!")
                break
            else:
                print("\nThanks for using Wishlist Editor. \nCheers!")
                break

        elif user_choice == '2':
            # Delete books from the wishlist
            delete_books_from_wishlist(csv_file_path)

            # Ask if the user wants to add any books
            add_option = input(
                "\nDo you want to add any books? \nPlease type 1 to add book(s). \nPress ANY OTHER KEY to exit. \nYour Choice: ")

            if add_option == '1':
                # Add books to the wishlist
                add_books_to_wishlist(csv_file_path)
                print("\nThanks for using WishList Editor. \nCheers!")
                break
            else:
                print("\nThanks for using WishList Editor. \nCheers!")
                break

        else:
            print("\nThanks for using WishList Editor. \nCheers!")
            break


def track_wishlist():
    print("\nWelcome to the WishList Tracker. \nTrack and receive updates for your WishLists effortlessly with this tool.")

    while True:
        # Prompt the user for the path and CSV file name
        local_path = input(
            "Please enter the path of the wishlist you want to track: ")
        file_name = input("Please enter the file name of the WishList: ")

        try:
            # Read the CSV file
            csv_file_path = f"{local_path}/{file_name}.csv"
            wishlist_df = pd.read_csv(csv_file_path)

            # Create a DataFrame to store the tracked wishlist
            tracked_wishlist = pd.DataFrame(columns=[
                                            'SNo', 'Book', 'Currency', 'Current Price', 'Desired Price', 'Notes', 'URL', 'Availability'])

            # Scrape information from each URL in the input CSV file
            for index, row in wishlist_df.iterrows():
                url = row['URL']
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Scrape book details
                    book_name_tag = soup.find('h1')
                    book_name = book_name_tag.text.strip() if book_name_tag else None

                    price_tag = soup.find('p', class_='price_color')
                    current_price_raw = price_tag.text.strip() if price_tag else None

                    availability_tag = soup.find(
                        'p', class_='instock availability')
                    availability = availability_tag.text.strip() if availability_tag else None

                    # Extract currency symbol
                    currency_symbol = '£'

                    # Handle currency conversion
                    current_price = float(current_price_raw.replace(
                        currency_symbol, '').strip())
                    desired_price = float(row['Desired Price'])

                    # Populate the DataFrame with scraped information
                    notes = ''
                    if current_price <= desired_price:
                        if 'available' in availability.lower():
                            notes = "Great! You can buy the book"
                        else:
                            notes = "Oops. The Book is not available at the moment"
                    elif current_price > desired_price:
                        notes = ''

                    tracked_wishlist = tracked_wishlist.append({
                        'SNo': index + 1,
                        'Book': book_name,
                        'Currency': currency_symbol,
                        'Current Price': current_price,
                        'Desired Price': desired_price,
                        'Notes': notes,
                        'URL': url,
                        'Availability': availability
                    }, ignore_index=True)

            # Ask for Local Path and File Name to save the Excel file
            excel_file_name = input(
                "\nGreat! Your WishList items have updated information. \nPlease create a file name to save your WishList updates: ") or'Default_WishList_Update'

            # Save the DataFrame as an Excel file
            excel_file_path = f"{local_path}/{excel_file_name}.xlsx"
            
            # Check if the Excel file already exists
            suffix = 1
            while os.path.exists(excel_file_path):
                excel_file_name = f"{excel_file_name} {suffix}"
                excel_file_path = f"{local_path}/{excel_file_name}.xlsx"
                suffix += 1
                
            tracked_wishlist.to_excel(excel_file_path, index=False)

            print(
                f"\nUpdates to your WishList have been successfully saved as {excel_file_name}.xlsx in the path {local_path}")

            while True:
                track_option = input(
                    "\nHow else can I assist you? \nPress '1' to track another WishList.\nPress 'ANY OTHER KEY' to exit. \nYour Choice: ")
                if track_option == '1':
                    # Start tracking another wishlist
                    break
                else:
                    print("\nThanks for using WishList Tracker.\nHappy shopping!")
                    return

        except Exception as e:
            print(
                f"\nI am sorry. WishList Tracker could not read your file.\nError: {e}")
            retry_option = input(
                "Would you like to retry? \nPress '1' to track a WishList.\nPress 'ANY OTHER KEY' to exit.\nYour Choice: ")
            if retry_option != '1':
                print("\nOops. That's a bummer. \nExiting the program. \nCheers!")
                return

#Defining the Main Program
def wishlist_manager():
    while True:
        print("\nWelcome to the WishList Manager!")
        print("\nChoose an option to get started:")
        print("1. Create a WishList")
        print("2. Edit a Wishlist")
        print("3. Track a WishList")
        print("\nPress 'ANY OTHER KEY' to Exit the program")

        user_choice = input("Please enter your option: ")

        if user_choice == '1':
            create_wishlist()
            print("\nPress 1 for 'WishList Manager' main menu.\nPress ANY OTHER KEY to exit.")
            main_option = input('\nPlease type your choice here: ')

            if main_option == '1':
                continue
            else:
                print("\nThank you for using WishList Manager! \nCheers!")
                return

        elif user_choice == '2':
            edit_wishlist()
            print("\nPress 1 for 'WishList Manager' main menu.\nPress ANY OTHER KEY to exit.")
            main_option = input('\nPlease type your choice here: ')

            if main_option == '1':
                continue
            else:
                print("\nThank you for using WishList Manager! \nCheers!")
                return

        elif user_choice == '3':
            track_wishlist()
            print("\nPress 1 for 'WishList Manager' main menu.\nPress ANY OTHER KEY to exit.")
            main_option = input('\nPlease type your choice here: ')

            if main_option == '1':
                continue
            else:
                print("\nThank you for using WishList Manager! \nCheers!")
                return

        else:
            print("\nExiting the program.\nCheers!")
            return

#Executing the main program
if __name__ == "__main__":
    wishlist_manager()