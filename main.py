
from scraper import Scraper
import logging
import timeit

url = "https://hprera.nic.in/PublicDashboard"
num_projects = 6  # Number of projects to scrape

scraper = Scraper(url, num_projects)

def scrape_projects():
    return scraper.scrape()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Measurng the time taken to scrape the details of the projects
    start_time = timeit.default_timer()
    registered_project_details = scrape_projects()
    elapsed_time = round(timeit.default_timer() - start_time, 2)
    
    print(f"\nTime elapsed: {elapsed_time} seconds")
    for key in registered_project_details:
        print("\nProject ", key+1)
        for (field, val) in registered_project_details[key].items():
            print(f"{field}: {val}")
    

    scraper.destroy()
