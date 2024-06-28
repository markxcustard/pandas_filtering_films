import pandas as pd
import os

def filter_films(input_file_path):
    # Read the CSV file
    films_df = pd.read_csv(input_file_path)

    # 1. Filter films that are <=2010 and have a rating between 8.4 and 8.7
    filtered_films_1 = films_df[(films_df['year'] <= 2010) & (films_df['rating'] >= 8.4) & (films_df['rating'] <= 8.7)]
    output_file_path_1 = os.path.join(os.path.dirname(input_file_path), 'filtered_films_1.csv')
    filtered_films_1.to_csv(output_file_path_1, index=False)

    # 2. Filter films that have the word "Gotham" in the description
    filtered_films_2 = films_df[films_df['description'].str.contains('Gotham', case=False)]
    output_file_path_2 = os.path.join(os.path.dirname(input_file_path), 'filtered_films_2.csv')
    filtered_films_2.to_csv(output_file_path_2, index=False)

    # 3. Filter actors name like "Leo" and characters called "Cobb"
    filtered_films_3 = films_df[(films_df['actors'].str.contains('Leo', case=False)) & 
                                (films_df['characters'].str.contains('Cobb', case=False))]
    
    print("Filtered by 'Leo' and 'Cobb':")
    print(filtered_films_3)
    
    output_file_path_3 = os.path.join(os.path.dirname(input_file_path), 'filtered_films_3.csv')
    filtered_films_3.to_csv(output_file_path_3, index=False)

    # 4. Filter films by multiple actors
    actors_list = ['Leonardo DiCaprio', 'Christian Bale']
    filtered_films_4 = films_df[films_df['actors'].apply(lambda actors: any(actor in actors.split(', ') for actor in actors_list))]
    output_file_path_4 = os.path.join(os.path.dirname(input_file_path), 'filtered_films_4.csv')
    filtered_films_4.to_csv(output_file_path_4, index=False)

    # 5. Filter films based on word count in the description
    filtered_films_5 = films_df[films_df['description'].apply(lambda desc: len(desc.split()) > 15)]
    output_file_path_5 = os.path.join(os.path.dirname(input_file_path), 'filtered_films_5.csv')
    filtered_films_5.to_csv(output_file_path_5, index=False)

    # 6. Filter films with the highest rating per decade
    films_df['decade'] = (films_df['year'] // 10) * 10
    filtered_films_6 = films_df.loc[films_df.groupby('decade')['rating'].idxmax()]
    output_file_path_6 = os.path.join(os.path.dirname(input_file_path), 'filtered_films_6.csv')
    filtered_films_6.to_csv(output_file_path_6, index=False)

    # 7. Filter films by common keywords in titles
    filtered_films_7 = films_df[films_df['title'].str.contains('The', case=False)]
    output_file_path_7 = os.path.join(os.path.dirname(input_file_path), 'filtered_films_7.csv')
    filtered_films_7.to_csv(output_file_path_7, index=False)

    return {
        "filtered_films_1": filtered_films_1,
        "filtered_films_2": filtered_films_2,
        "filtered_films_3": filtered_films_3,
        "filtered_films_4": filtered_films_4,
        "filtered_films_5": filtered_films_5,
        "filtered_films_6": filtered_films_6,
        "filtered_films_7": filtered_films_7
    }

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_folder, 'films.csv')
    filter_films(input_file_path)
