
import os
from math import sqrt
# A dictionary of movie critics and their ratings of a small
# set of movies

critics = {'Lisa Rose': {'Lady in the Water': 2.5,
                         'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0,
                         'Superman Returns': 3.5,
                         'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0
                         },

           'Gene Seymour': {'Lady in the Water': 3.0,
                            'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5,
                            'Superman Returns': 5.0,
                            'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5
                            },

           'Michael Phillips': {'Lady in the Water': 2.5,
                                'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5,
                                'The Night Listener': 4.0
                                },

           'Claudia Puig': {'Snakes on a Plane': 3.5,
                            'Just My Luck': 3.0,
                            'The Night Listener': 4.5,
                            'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5
                            },

           'Mick LaSalle': {'Lady in the Water': 3.0,
                            'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0,
                            'Superman Returns': 3.0,
                            'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0
                            },

           'Jack Matthews': {'Lady in the Water': 3.0,
                             'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0,
                             'Superman Returns': 5.0,
                             'You, Me and Dupree': 3.5
                             },

           'Toby': {'Snakes on a Plane': 4.5,
                    'You, Me and Dupree': 1.0,
                    'Superman Returns': 4.0
                    }
           }








# user based collaborative filtering...
# Returns a distance-based similarity score for person1 and person2
# euclidean distance
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                         for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)


# Returns the Pearson correlation coefficient for p1 and p2
# pearson correlation score
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1_sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2_sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    p_sum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = p_sum - (sum1 * sum2 / n)
    den = sqrt((sum1_sq - pow(sum1, 2) / n) * (sum2_sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den

    return r


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def get_recommendations(prefs,person,similarity=sim_pearson):
    totals = {}
    sim_sums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
        # Sum of similarities
        sim_sums.setdefault(item, 0)
        sim_sums[item] += sim

    # Create the normalized list
    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


# import pprint
# pprint.pprint(transform_prefs(critics))
# Item based filtering.


def calculate_similarItems(prefs,n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be item-centric
    item_prefs = transform_prefs(prefs)
    c = 0
    for item in item_prefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print "%d / %d" % (c, len(item_prefs))
            # Find the most similar items to this one
        scores = top_matches(item_prefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def get_recommended_items(prefs, item_match, user):
    user_ratings = prefs[user]
    scores = {}
    total_sim = {}
    # Loop over items rated by this user
    for (item, rating) in user_ratings.items():
        # Loop over items similar to this one
        for (similarity, item2) in item_match[item]:
            # Ignore if this user has already rated this item
            if item2 in user_ratings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


# should be built first and stored somewhere.
# value = calculate_similarItems(critics)
# print get_recommended_items(critics, value, 'Toby')
def load_movie_lens(path=os.getcwd()):
    # Get movie titles
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    # Load data
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs
