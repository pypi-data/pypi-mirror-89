# Links verification
Verify that all the external/absolute links within a web page work correctly.
 
# Install
``` bash
$ pip install links-verification
```

# How to use
``` bash
from links_verification import verify

my_verify = verify.Verify ("https://www.url_example.com")


# PRINT INFORMATION

# Print all links functional links, error links and the problem of the error links
my_verify.print_all_links()

# Print only the functional links
my_verify.print_functional_links()

# Print only the error links and their errors
my_verify.print_error_links()


# SAVE INFORMATION IN FILE

# External file absolute path
my_file = os.path.join (os.path.dirname(__file__), "ouput.txt")

# Save in external text file all links and the problem error links
my_verify.save_all_links(my_file)

# Save in external text file only the functional links
my_verify.save_functional_links (my_file)

# Save in external text file only the error links and their errors
my_verify.save_error_links (my_file)


# RETURN INFORMATION

# Return a dictionary with the keywords: "functional" and "erros", whitch contains the link list
links = my_verify.return_all_links()

# Retiurn only the functional links in a list
links = my_verify.return_functional_links()

# Return only the error links and their errors in a list
links = my_verify.return_error_links()
```
