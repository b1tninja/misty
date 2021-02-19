import random

from yelpapi import YelpAPI

from misty.utils import print_and_say

YELP_API_KEY = 'h81ylaT0alwtJCUUyI7RazCCHNHleVGnhD9ZONPT1s4kL9v5qhCXPZrcI20H4LYisDEjJZu_j4ibEsSTpM2ISDpWBeraK3t42rwV_PhxtYvmatDn2xquIUKdueYtYHYx'  # plz no steal my api keyz!
client = YelpAPI(YELP_API_KEY)

biz_ids = ['pierce-j-r-plumbing-co-inc-of-sacramento-rocklin',
           'ncm-roseville',
           ]

random.shuffle(biz_ids)

for biz_id in biz_ids:
    result = client.business_query(id=biz_id)

    print_and_say(
        f"{result['name']}. Phone number: {result['display_phone']}. Address: {''.join(result['location']['display_address'])}",
        next_voice=True)

    reviews = client.reviews_query(id=result['id'])

    print_and_say(f"Retrieved {len(reviews['reviews'])} of {reviews['total']} reviews.", next_voice=True)
    for review in reviews['reviews']:
        print_and_say(
            f"On {review['time_created']} {review['user']['name']} gave a rating of {review['rating']} stars, stating: {review['text']}.",
            next_voice=True)
