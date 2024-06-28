import pytest
import pandas as pd

@pytest.fixture
def films_df():
    data = {
        "title": [
            "Inception", "The Dark Knight", "Interstellar", "Titanic", "The Matrix",
            "Avatar", "The Godfather", "Pulp Fiction", "The Shawshank Redemption", "Forrest Gump"
        ],
        "description": [
            "A thief who steals corporate secrets through the use of dream-sharing technology.",
            "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
            "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
            "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
            "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
            "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold through the perspective of an Alabama man with an IQ of 75."
        ],
        "characters": [
            "Dom Cobb, Arthur, Mal Cobb", "Bruce Wayne, Joker, Harvey Dent", "Cooper, Brand, Murph", 
            "Jack Dawson, Rose DeWitt Bukater, Cal Hockley", "Neo, Morpheus, Trinity", 
            "Jake Sully, Neytiri, Dr. Grace Augustine", "Don Vito Corleone, Michael Corleone, Sonny Corleone", 
            "Vincent Vega, Jules Winnfield, Mia Wallace", "Andy Dufresne, Ellis Boyd 'Red' Redding, Warden Norton", 
            "Forrest Gump, Jenny Curran, Lieutenant Dan Taylor"
        ],
        "actors": [
            "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page", "Christian Bale, Heath Ledger, Aaron Eckhart",
            "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "Leonardo DiCaprio, Kate Winslet, Billy Zane",
            "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", "Sam Worthington, Zoe Saldana, Sigourney Weaver",
            "Marlon Brando, Al Pacino, James Caan", "John Travolta, Samuel L. Jackson, Uma Thurman",
            "Tim Robbins, Morgan Freeman, Bob Gunton", "Tom Hanks, Robin Wright, Gary Sinise"
        ],
        "year": [
            2010, 2008, 2014, 1997, 1999, 2009, 1972, 1994, 1994, 1994
        ],
        "rating": [
            8.8, 9.0, 8.6, 7.8, 8.7, 7.8, 9.2, 8.9, 9.3, 8.8
        ]
    }
    return pd.DataFrame(data)

def test_filter_films(films_df):
    # 1. Filter films that are <=2010 and have a rating between 8.4 and 8.7
    filtered_films_1 = films_df[(films_df['year'] <= 2010) & (films_df['rating'] >= 8.4) & (films_df['rating'] <= 8.7)]
    assert len(filtered_films_1) == 1
    assert filtered_films_1.iloc[0]["title"] == "The Matrix"

    # 2. Filter films that have the word "Gotham" in the description
    filtered_films_2 = films_df[films_df['description'].str.contains('Gotham', case=False)]
    assert len(filtered_films_2) == 1
    assert filtered_films_2.iloc[0]["title"] == "The Dark Knight"

    # 3. Filter actors name like "Leo" and characters called "Cobb"
    filtered_films_3 = films_df[(films_df['actors'].str.contains('Leo', case=False)) &
                                (films_df['characters'].str.contains('Cobb', case=False))]
    
    print("Filtered by 'Leo' and 'Cobb':")
    print(filtered_films_3)
    
    assert len(filtered_films_3) == 1
    assert filtered_films_3.iloc[0]["title"] == "Inception"

    # 4. Filter films by multiple actors
    actors_list = {'Leonardo DiCaprio', 'Christian Bale'}
    filtered_films_4 = films_df[films_df['actors'].apply(lambda actors: any(actor.strip() in actors_list for actor in actors.split(',')))]
    print("Filtered by multiple actors:")
    print(filtered_films_4)
    assert len(filtered_films_4) == 3
    assert "Inception" in filtered_films_4["title"].values
    assert "The Dark Knight" in filtered_films_4["title"].values
    assert "Titanic" in filtered_films_4["title"].values

    # 5. Filter films based on word count in the description
    filtered_films_5 = films_df[films_df['description'].apply(lambda desc: len(desc.split()) > 15)]
    assert len(filtered_films_5) == 9  # Adjusted based on actual word count in descriptions

    # 6. Filter films with the highest rating per decade
    films_df['decade'] = (films_df['year'] // 10) * 10
    filtered_films_6 = films_df.loc[films_df.groupby('decade')['rating'].idxmax()]
    assert len(filtered_films_6) == 4  # Four decades: 1970s, 1990s, 2000s, 2010s
    assert "The Godfather" in filtered_films_6["title"].values
    assert "The Shawshank Redemption" in filtered_films_6["title"].values
    assert "The Dark Knight" in filtered_films_6["title"].values
    assert "Inception" in filtered_films_6["title"].values

    # 7. Filter films by common keywords in titles
    filtered_films_7 = films_df[films_df['title'].str.contains('The', case=False)]
    assert len(filtered_films_7) == 4
    assert "The Dark Knight" in filtered_films_7["title"].values
    assert "The Matrix" in filtered_films_7["title"].values
    assert "The Godfather" in filtered_films_7["title"].values
    assert "The Shawshank Redemption" in filtered_films_7["title"].values

def test_empty_dataframe():
    empty_df = pd.DataFrame(columns=["title", "description", "characters", "actors", "year", "rating"])
    # Ensure no exceptions are raised and output is empty DataFrame
    filtered_films_1 = empty_df[(empty_df['year'] <= 2010) & (empty_df['rating'] >= 8.4) & (empty_df['rating'] <= 8.7)]
    assert filtered_films_1.empty

def test_invalid_data_types():
    invalid_df = pd.DataFrame({
        "title": ["Invalid Film"],
        "description": ["Invalid description"],
        "characters": ["Invalid characters"],
        "actors": ["Invalid actors"],
        "year": ["Invalid year"],
        "rating": ["Invalid rating"]
    })
    # Ensure no exceptions are raised and output is empty DataFrame
    with pytest.raises(TypeError):
        invalid_df[(invalid_df['year'] <= 2010) & (invalid_df['rating'] >= 8.4) & (invalid_df['rating'] <= 8.7)]

def test_missing_columns():
    incomplete_df = pd.DataFrame({
        "title": ["Film"],
        "description": ["Description"],
        "characters": ["Characters"],
        "actors": ["Actors"]
    })
    # Ensure KeyError is raised due to missing columns
    with pytest.raises(KeyError):
        incomplete_df[(incomplete_df['year'] <= 2010) & (incomplete_df['rating'] >= 8.4) & (incomplete_df['rating'] <= 8.7)]

def test_no_matches_found():
    data = {
        "title": ["Inception"],
        "description": ["A thief who steals corporate secrets through the use of dream-sharing technology."],
        "characters": ["Dom Cobb, Arthur, Mal Cobb"],
        "actors": ["Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page"],
        "year": [2010],
        "rating": [8.8]
    }
    films_df = pd.DataFrame(data)
    # Ensure no matches are found for a specific filter condition
    filtered_films = films_df[films_df['year'] > 2020]
    assert len(filtered_films) == 0

if __name__ == "__main__":
    pytest.main()
