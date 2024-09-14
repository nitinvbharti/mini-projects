import csv
import os
from typing import List

def append_to_csv_file(
    filepath: str,
    row: dict,
    fieldnames: List[str]):
    """
    Append data to csv file.
    
    Keyword arguments:
    filepath -- Csv file path to append data to.
    row -- Data to insert.
    fieldnames -- List of field names.
    """
    if already_searched_movie(row, filepath):
        return
    
    with open(filepath, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(row)
        
def read_csv_File(filepath: str):
    """
    Read a csv file.
    
    Keyword arguments:
    filepath -- File path.
    Return: Contents of file path as list of row items.
    """
    if not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
        return []
    
    # TODO: Avoid duplicate writes.
    with open(filepath, 'r') as csvfile:
        data = csv.reader(csvfile)
        return list(data)
    
def already_searched_movie(
    row: dict,
    filepath: str):
    """
    Checks if movie entry already exists in the search history.
    
    Keyword arguments:
    row -- Dictionary item to be searched.
    filepath -- Path of stored history file. 
    Return: Movie already searched in past.
    """
    entries = read_csv_File(filepath)
    
    for e in entries:
        e = [x.lower() for x in e]
        if str.lower(row['Movie']) in e:
            return True
    
    return False