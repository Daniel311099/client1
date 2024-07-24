
from flask import Flask, jsonify, request
from sqlalchemy.orm import Session
from service import Post, SessionLocal
from flask_cors import CORS
# from dashboard import dashboard
import dash
from dash import dcc, html
import plotly.express as px

app = Flask(__name__)
CORS(app, resources={r"/user/*": {"origins": "*"}})
@app.after_request
def add_header(response):
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response
def get_user_post_count(user_id: str) -> int:
    """
    Fetches all posts made by a user and counts them.

    Args:
        user_id (int): The ID of the user.

    Returns:
        int: The count of posts made by the user.
    """
    # Create a new database session
    session: Session = SessionLocal()
    
    try:
        # Query the posts table to get the count of posts made by the user
        post_count = session.query(Post).filter(Post.createdById == user_id).count()
        return post_count
    finally:
        # Close the session
        session.close()

@app.route('/user/<string:user_id>/post_count', methods=['GET'])
def user_post_count(user_id):
    print(user_id)
    try:
        post_count = get_user_post_count(user_id)
        return jsonify({'user_id': user_id, 'post_count': post_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/dashboard', methods=['GET'])
# def get_dashboard():
#     return dashboard

dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dashboard/'
)

# Generate a sample plot
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')

dash_app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
if __name__ == "__main__":
    app.run(debug=True)
