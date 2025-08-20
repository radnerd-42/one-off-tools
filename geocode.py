# Geocode script to get addresses from OpenStreetMap using the Nominatim. Information at https://nominatim.org/
# This was done for a project that included several hundred locations, so manual was not the way to go.
# This gets a street address from latitude and longitude provided in a CSV. 
# The columns must be labeled 'latitude' and 'longitude'.
# Other columns are ignored, so the output file can be used directly.
# I may play around with looking other aspects of the API, but this was a first go.

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

# Determine input and output files
input_csv = input("What file has the coordinates? ")
output_csv = input("Where do you want the addresses saved? ")

# Function to get provide the coordinates and geolocator user_agent string to Nominatim
def get_address_from_coords(lat, lon, geolocator):
  try:
    location = geolocator.reverse(f"{lat},{lon}", language = "en")
    if location:
      return location.address
    else:
      return "No address found"
  # Errors with the API not inputs
  except (GeocoderTimedOut, GeocoderServiceError) as e:
    print(f"Geocoder error for {lat}, {lon}: e")
    return "API error"
  # Check your coordinates, especially to make sure tyou didn't mix up the lat and lon
  except ValueError:
    return "Invalid coordinates"

# Function to run through the CSV and use the above function to get the addresses
def process_csv():
  try:
    df = pd.read_csv(input_csv, sep = "\t") # Replace "\t" with "," if using actual commas. My output had tabs.
  # Report typos or location issue
  except FileNotFoundError:
    print(f"Error: {input_csv} not found")
    return
  # Check for column names
  if "latitude" not in df.columns or "longitude" not in df.columns:
    print("Error: The CSV must contain 'latitude' and 'longitude' columns.")
    return
  # Nominatim takes a user_agent
  geolocator = Nominatim(user_agent = input("What are you running (name your app)? "))
  # Add the output column
  df["address"] = None
  # Work through all the rows to get addresses
  for index, row in df.iterrows():
    lat = row["latitude"]
    lon = row["longitude"]
    if pd.notna(lat) and pd.notna(lon):
      address = get_address_from_coords(lat, lon, geolocator)
      df.at[index, "address"] = address
      print(f"Processed {lat}, {lon}")
  # Nominatim required lookup rate
  time.sleep(1.01)
  # Output to the new CSV. Could change a bit to just add to the original. This was my initial approach.
  df.to_csv(output_csv, index = False)
  print(f"\nProcessing complete. Results saved to {output_csv}")

if __name__ == "__main__":
  process_csv()
