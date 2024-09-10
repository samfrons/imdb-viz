import csv
import imdb
from tqdm import tqdm
import time

# Initialize the IMDb object
ia = imdb.IMDb()

# Function to get movie details
def get_movie_details(movie_title, year):
    try:
        # Search for the movie
        results = ia.search_movie(f"{movie_title} ({year})")
        if results:
            # Get the first result
            movie = ia.get_movie(results[0].movieID)
            
            # Get number of votes (ratings)
            votes = movie.get('votes')
            
            # Get country
            countries = movie.get('countries', [])
            country = countries[0] if countries else 'Unknown'
            
            return votes, country
        else:
            return None, None
    except Exception as e:
        print(f"Error processing {movie_title} ({year}): {str(e)}")
        return None, None

# Input and output file names
input_file = 'apocalyptic_movies_details.csv'
output_file = 'apocalyptic_movies_details_updated.csv'

# Read the input CSV file
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Number of Ratings', 'Country']
    
    # Prepare the output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process each movie
        for row in tqdm(list(reader), desc="Processing movies"):
            votes, country = get_movie_details(row['Title'], row['Year'])
            
            # Add new information to the row
            row['Number of Ratings'] = votes if votes is not None else 'N/A'
            row['Country'] = country if country is not None else 'Unknown'
            
            # Write the updated row to the output file
            writer.writerow(row)
            
            # Add a small delay to avoid overwhelming the IMDb server
            time.sleep(1)

print(f"Updated data has been written to {output_file}")