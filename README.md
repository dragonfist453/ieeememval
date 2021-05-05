# IEEE Vtools Membership Validator for Excel files

## Usage

- Run the following command on a linux shell
    
        pip install requirements.txt
    
- Download the chrome driver executable binaries and add to path as shown [here](https://www.selenium.dev/documentation/en/selenium_installation/installing_webdriver_binaries/).

- Rename the columns such that there are no spaces or newlines or tabs or slashes, in order for the program to work as expected

- Run the program using the following command

        python main.py
         --colname name of column in the input csv file
         --input <path/to/inputfile>
         --output <path/to/outputfile>
         --errors <path/to/errorfile>

- Done!