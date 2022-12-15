# WebScraper

    ****eBay Scraper****
    
This script is a web scraper that searches for items on eBay, specifically Raspberry Pi 4 kits. 
It filters and parses the information it gets from the eBay search, calculates the average price per unit, outputs the data to a CSV file, and 
sends the file to a specified Gmail account.

*Usage
To use this script, you'll need to modify the search_term variable to specify the items you want to search for on eBay. 
You'll also need to update the email addresses and password in the keyring module with your own information. 
Then, you can run the script using the python ebay_scraper.py command.

*Requirements
This script uses the following Python modules:

-requests
-BeautifulSoup
-keyring
-pandas
-smtplib
Make sure these modules are installed before running the script.

*Output
The script will output a CSV file containing the parsed information from the eBay search results. 
The file will be saved in the same directory as the script, and it will be named ebay_search_results.csv.

The script will also send the CSV file to the specified email address via Gmail.

License
This script is provided under the MIT license. See the LICENSE file for details.
