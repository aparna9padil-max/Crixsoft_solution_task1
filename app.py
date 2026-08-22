from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("movie_ratings_project.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Convert Rating to numeric
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Remove missing ratings
df = df.dropna(subset=["Rating"])


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/movies")
def movies():
    movies_data = df.to_dict(orient="records")
    return render_template("movies.html", movies=movies_data)


@app.route("/top-movies")
def top_movies():
    top_movies_data = df.sort_values(
        by="Rating", ascending=False
    ).head(10)

    return render_template(
        "top_movies.html",
        movies=top_movies_data.to_dict(orient="records")
    )


@app.route("/genres")
def genres():
    genre_data = (
        df.groupby("Genre")["Rating"]
        .mean()
        .sort_values(ascending=False)
    )

    genres_data = [
        {"Genre": genre, "Rating": round(rating, 2)}
        for genre, rating in genre_data.items()
    ]

    return render_template(
        "genres.html",
        genres=genres_data
    )
    
@app.route("/dashboard")
def dashboard():

    # Basic statistics
    mean_rating = round(df["Rating"].mean(), 2)
    median_rating = round(df["Rating"].median(), 2)
    mode_rating = round(df["Rating"].mode()[0], 2)

    # Highest-rated movie
    top_movie_row = df.loc[df["Rating"].idxmax()]

    top_movie = top_movie_row["Title"]
    highest_rating = top_movie_row["Rating"]

    # Total movies
    total_movies = len(df)

    # Rating distribution
    rating_counts = (
        df["Rating"]
        .round(1)
        .value_counts()
        .sort_index()
    )

    rating_labels = rating_counts.index.tolist()
    rating_values = rating_counts.values.tolist()

    # Top 10 movies
    top_movies_data = (
        df.sort_values("Rating", ascending=False)
        .head(10)
    )

    movie_titles = top_movies_data["Title"].tolist()
    movie_ratings = top_movies_data["Rating"].tolist()

    # Average rating by genre
    genre_data = (
        df.groupby("Genre")["Rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    genre_labels = genre_data.index.tolist()
    genre_values = genre_data.round(2).tolist()

    return render_template(
        "dashboard.html",

        total_movies=total_movies,

        mean_rating=mean_rating,

        median_rating=median_rating,

        mode_rating=mode_rating,

        highest_rating=highest_rating,

        top_movie=top_movie,

        rating_labels=rating_labels,

        rating_values=rating_values,

        movie_titles=movie_titles,

        movie_ratings=movie_ratings,

        genre_labels=genre_labels,

        genre_values=genre_values
    )   





if __name__ == "__main__":
    app.run(debug=True)