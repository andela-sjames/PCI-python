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


# Returns a distance-based similarity score for person1 and person2
# euclidean distance
def sim_distance(prefs, person1, person2):
    """Get the list of shared_items."""
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
    """Get the list of mutually rated items."""
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # Find the number of elements
    n = len(si)
    # if they are no ratings in common, return 0
    if n == 0:
        return 0
    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Sum up the products
    psum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate Pearson score
    num = psum - (sum1 * sum2 / n)
    den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    """
    Return the best matches for person from the prefs dictionary.

    Number of results and similarity function are optional params.
    """
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]
