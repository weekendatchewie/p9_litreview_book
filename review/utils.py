def stars_rating(reviews):

    for review in reviews:
        if review.rating == 5:
            review.rating = '★★★★★'
        elif review.rating == 4:
            review.rating = "★★★★☆"
        elif review.rating == 3:
            review.rating = "★★★☆☆"
        elif review.rating == 2:
            review.rating = "★★☆☆☆"
        elif review.rating == 1:
            review.rating = "★☆☆☆☆"
        else:
            review.rating = "☆☆☆☆☆"

    return reviews
