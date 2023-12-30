# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from flask import render_template, request

from app import app

from .query_data import get_product_list
from .serpapi import get_product


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gifts', methods=['POST'])
def get_gifts():
    # Get the user's answers from the form
    relationship = request.form.get('relationship')
    age = request.form.get('age')
    occasion = request.form.get('occasion')
    interests = request.form.get('interests')
    budget = request.form.get('budget')

    # Execute the logic to generate gift ideas based on the keywords
    keywords = get_product_list(relationship, age, occasion, interests, budget)                                
    # Query SERPAPI for each keyword and compile the results
    gifts = []
    for keyword in keywords:
        serpapi_results = get_product(keyword)
        for result in serpapi_results:
            gift = {
                "idea": keyword, 
                "title": result.get('title', 'N/A'), 
                "link": result.get('link', 'N/A'), 
                "price": result.get('price', 'N/A'), 
                "old_price": result.get('old_price', 'N/A'), 
                "second_hand_condition": result.get('second_hand_condition', 'N/A'), 
                "rating": result.get('rating', 'N/A'), 
                "reviews": result.get('reviews', 'N/A'), 
                "store_rating": result.get('store_rating', 'N/A'), 
                "store_reviews": result.get('store_reviews', 'N/A'), 
                "number_of_comparisons": result.get('number_of_comparisons', 'N/A'), 
                "snippet": result.get('snippet', 'N/A'), 
                "thumbnail": result.get('thumbnail', 'N/A')
            }
            gifts.append(gift)

    # Render the template with the results
    return render_template('gifts.html', gifts=gifts)
