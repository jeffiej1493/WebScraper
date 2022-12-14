import keyring
import requests
import smtplib
from email.message import EmailMessage
import pandas as pd
from bs4 import BeautifulSoup

"""
This script uses web scraping to search for items on eBay, specifically Raspberry Pi 4 kits.
It filters and parses the information it gets from the eBay search, calculates the average price per unit,
outputs the data to a CSV file, and sends the file to a specified Gmail account.

To use this script, modify the 'search_term' variable to specify the items you want to search for on eBay.
Change the email addresses and update the password manager keyring with your information.
Then, run the script using the following command:

python ebay_scraper.py
"""

# This saves my password into a password manager. ---> keyring.set_password('your_application_name', username, password)

# This stored the password from 'keyring' for future use.
password = keyring.get_password("gmail", "Jeffreyswebscraper@gmail.com")

# Search term can be modified to search items on ebay. The + symbol will replace empty spaces.
search_term = 'raspberry+pi+4+kit'

# saves the url for future use.
url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&LH_TitleDesc=0&_fsrp=1&LH_Auction=1&LH_PrefLoc=2&LH_Complete=1&LH_Sold=1&_ipg=240"


def get_data(url):
    """
      Saves the text from the web page at the specified URL to the 'request_variable' variable.

      Args:
          url (str): The URL of the web page to scrape.

      Returns:
          soup (BeautifulSoup object): The parsed HTML of the web page.
      """

    request_variable = requests.get(url)
    soup = BeautifulSoup(request_variable.text, "html.parser")
    return soup


# Creates a method to filter through the information of the url link.
def parse(soup):
    """
    Filters and parses the information from the eBay search results in the specified BeautifulSoup object.

    Args:
        soup (BeautifulSoup object): The parsed HTML of the eBay search results page.

    Returns:
        raspPIlist (list): A list of dictionaries, where each dictionary contains information about a single item from the search results.
    """
    # creates an empty list to store items into.
    raspPIlist = []

    # stores the div tags of all items into the soup variable from the url link.
    results = soup.find_all('div', {'class': 's-item__info clearfix'})

    # Creating a for loop to iterate over each item and store specific info about that item into a dict.
    for item in results:
        raspPiProducts = {
            'title': item.find('div', {'class': 's-item__title'}).text,
            'soldPrice': float(item.find('span', {'class': 's-item__price'}).text.replace('$', '').replace(',', '').strip()),
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        raspPIlist.append(raspPiProducts)

    return raspPIlist


# this function finds the average price per item.
def find_average_price(soup):
    """
     Calculates the average price per unit of the items in the specified BeautifulSoup object.

     Args:
         soup (BeautifulSoup object): The parsed HTML of the eBay search results page.

     Returns:
         average_price (float): The average price per unit of the items in the search results.
     """
    # creates an empty list to store prices into.
    average_list = []

    # stores the div tags of all items into the soup variable from the url link
    results = soup.find_all('div', {'class': 's-item__info clearfix'})

    # Creating a for loop to iterate over each item and store the price of that item into a dict.
    for item in results:
        item_list = {
            'soldPrice': float(
                item.find('span', {'class': 's-item__price'}).text.replace('$', '').replace(',', '').strip()),
        }
        average_list.append(item_list['soldPrice'])
    return sum(average_list)/(len(average_list))


# This function outputs the product list to a csv file.
def output(raspPIlist):
    """
     Outputs the list of Raspberry Pi 4 kit items to a CSV file.

     Args:
         raspPIlist (list): A list of dictionaries, where each dictionary contains information about a single item from the search results.

     Returns:
         None: The function does not return any value, but saves the data to a CSV file.
     """
    dataFrameForProducts = pd.DataFrame(raspPIlist)
    dataFrameForProducts.to_csv('raspPI4kitList.csv', index=False)
    print("successfully saved to CSV file.")
    return


# This function opens the csv file and sends it to my gmail account.
def send_csvfile_to_gmail(cvs_file_path, myGmail, gMailPassword, average_price):
    """
      Sends the specified CSV file to a specified email address using a Gmail account.

      Args:
          csv_file_path (str): The file path of the CSV file to send.
          myGmail (str): The email address to send the CSV file to.
          gMailPassword (str): The password of the Gmail account to use to send the CSV file.
          average_price(float): The average price per unit.

      Returns:
          None
      """
    # Checking to see if file exists then reading in binary mode.
    try:
        # Opening the csv file in read mode.
        with open(cvs_file_path, 'rb') as csv_file:
            csv_data = csv_file.read()
    except FileNotFoundError:
        error_message = "sorry the filename: " + cvs_file_path + ' does not exist.'
        print(f'This error occured: ******{error_message}*****')

    # Creates the message.
    msg = EmailMessage()
    msg.set_content(f'Here is the CSV file with rasp pi 4 kits. The average price per unit is: ${average_price:.2f}')
    msg['Subject'] = 'CSV File'
    msg['From'] = 'Jeffreyswebscraper@gmail.com'
    msg['To'] = 'jeffiej1493@gmail.com'
    msg.add_attachment(csv_data, maintype='application', subtype='octet-stream', filename='raspPI4kitlist.csv')

    # Connect to the Gmail SMTP server.
    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login(myGmail, gMailPassword)
    conn.send_message(msg)

    conn.quit()
    return

soup = get_data(url)
raspPIlist = parse(soup)
average_price = find_average_price(soup)

output(raspPIlist)
send_csvfile_to_gmail('raspPI4kitList.csv', 'Jeffreyswebscraper@gmail.com', password, average_price)



