#! python3
# Auto play 2048 game

import logging, time, requests, sys, bs4

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable()

class Verify (): 
    """
    Verify that all the external/absolute links within a web page work correctly.
    """

    def __init__ (self, page_url):
        """
        Constructor of the class
        Save as class variable the url of the page to verify
        """

        self.page_url = page_url
        self.__links_elements = []
        self.functional_links = []
        self.error_links = []


        self.__get_links()
        self.__verify_links()

    def __get_links (self):
        """
        Get and save all links of the page
        """ 
        
        print ('Searching links...')

        # get page
        res = requests.get (self.page_url)
        res.raise_for_status()

        # extract links
        selector = 'a[href]'
        soup = bs4.BeautifulSoup (res.text, "html.parser")
        self.__links_elements += soup.select (selector) 

    def __verify_links (self): 
        """ 
        Verify all link of the page and save each one 
        """

        for elemLink in self.__links_elements:  
            link = elemLink.attrs["href"]
            if link.strip() != "":

                # rename relative links
                if str(link).startswith("/") or str(link).startswith(".."): 
                    link = self.page_url + link
                
                # ignore js functions
                if not str(link).startswith("http"):
                    continue


                try: 
                    res = requests.get(link)
                    res.raise_for_status()
                    self.functional_links.append (link)
                except Exception as error:
                    self.error_links.append (str(link +  'The problem was: ' + str(error)))
    
    def print_all_links (self): 
        """
        Print all links functional links, error links and the problem of the error links
        """

        self.print_functional_links()
        self.print_error_links()

    def print_functional_links (self): 
        """
        Print only the functional links
        """

        if self.functional_links: 
            print ("\nFunctional links:\n")

            for link in self.functional_links: 
                print (link)
        else: 
            print ("\nNo functional links found\n")

    def print_error_links (self): 
        """
        Print only the error links and their errors
        """

        if self.error_links: 
            print ("\nError links:\n")

            for link in self.error_links: 
                print (link)
        else: 
            print ("\nNo error links found\n")
    
    def save_all_links (self, file): 
        """
        Save in external text file all links and the problem error links
        """

        self.save_functional_links(file)
        self.save_error_links(file)

    def save_functional_links (self, file): 
        """
        Save in external text file only the functional links
        """

        file_obj = open (file, 'a')

        if self.functional_links: 
            print ("\nSaved functional links.\n")

            for link in self.functional_links: 
                file_obj.write("\n"+link)
        else: 
            print ("\nNo functional links found\n")


    def save_error_links (self, file): 
        """
        Save in external text file only the error links and their errors
        """

        file_obj = open (file, 'a')

        if self.error_links: 
            print ("Saved errror links:\n")

            for link in self.error_links: 
                file_obj.write("\n"+link)
        else: 
            print ("\nNo error links found\n")
    
    def return_all_links (self): 
        """
        Return a dictionary with the keywords: "functional" and "erros", 
        whitch contains the link list
        """

        functional = self.return_functional_links()
        error = self.return_error_links()

        return {"functional": functional, "error":error}

    def return_functional_links (self): 
        """
        Retiurn only the functional links in a list
        """

        links = []

        for link in self.functional_links: 
            links.append(link)
        return links


    def return_error_links (self): 
        """
        Return only the error links and their errors in a list
        """

        links = []

        for link in self.error_links: 
            links.append(link)
        return links
    
    
    