"""
6.101 Lab 3:
Bacon Number
"""

#!/usr/bin/env python3

import pickle



def transform_data(raw_data):
    """
    Turns raw data into a more usable form

    Args:
        raw_data (list): list of 3 element tuples in the
        form of (actor_id_1, actor_id_2, film_id)

    Returns:
        list: A list of two dicts one for actors and one for movies
        actor dict has keys of actor ids and values of a set of
        every actor they have acted with
        movies dict has movie id keys and values of a set of
        actor ids of actors in that movie

    """

    movie_dict = {}
    acted_with = {}

    # movie dict
    for actor_id_1, actor_id_2, movie in raw_data:
        if movie in movie_dict:
            movie_dict[movie].add(actor_id_1)
            movie_dict[movie].add(actor_id_2)
        else:
            # set
            movie_dict[movie] = {actor_id_1, actor_id_2}

    # actor dict
    for actor_id_1, actor_id_2, movie in raw_data:
        # check for actor 1
        if actor_id_1 in acted_with:
            acted_with[actor_id_1].add(actor_id_2)
        else:
            acted_with[actor_id_1] = {actor_id_2}

        # check for actor 2
        if actor_id_2 in acted_with:
            acted_with[actor_id_2].add(actor_id_1)
        else:
            acted_with[actor_id_2] = {actor_id_1}

    return [acted_with, movie_dict]


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Determines if two actors have acted together

    Args:
        transformed_data (list): A list of two dicts
        one for actors and one for movies
        actor dict has keys of actor ids and
        values of a set of every actor they have
        acted with. Movies dict has movie id
        keys and values of a set of actor ids of
        actors in that movie
        actor_id_1 (int): number id of an actor
        actor_id_2 (int): number id of an actor

    Returns:
        Boolean: True if actors have been in a
        movie together and false if they have not
    """
    # actor has acted with themself
    if actor_id_1 == actor_id_2:
        return True

    # get actors dict
    actors_info = transformed_data[0]
    actor_1_with = actors_info[actor_id_1]

    return actor_id_2 in actor_1_with


def actors_with_bacon_number(transformed_data, n):
    """
    Finds all of the actors in data witha given
    Bacon number

    Args:
        transformed_data (list): A list of two dicts
        one for actors and one for movies
        actor dict has keys of actor ids and
        values of a set of every actor they have
        acted with. Movies dict has movie id
        keys and values of a set of actor ids of
        actors in that movie
        n (int): Bacon number

    Returns:
        set: set of all actor ids with bacon
        number n
    """
    actors_info = transformed_data[0]

    if 4724 not in actors_info:
        return set()

    if n == 0:
        return {4724}

    # keep track of actor ids searched
    visited = {4724}
    visited.update(actors_info[4724])

    # keep track of current level
    actors_current_level = actors_info[4724]

    for _ in range(1, n):
        # create next level
        new_level = set()
        for actor in actors_current_level:
            # check all actors acted with
            acted_with = actors_info[actor]
            for act in acted_with:
                if act not in visited:
                    new_level.add(act)

        visited.update(new_level)
        actors_current_level = new_level
        # to avoid looping through empty sets
        if new_level == set():
            break

    return actors_current_level


def bacon_path(transformed_data, actor_id):
    """
    Finds shortest list of actors connecting
    to Keviin Bacon

    Args:
        transformed_data (list): A list of two dicts
        one for actors and one for movies
        actor dict has keys of actor ids and
        values of a set of every actor they have
        acted with. Movies dict has movie id
        keys and values of a set of actor ids of
        actors in that movie
        actor_id (int): id for a specific actor

    Returns:
        list: shortest list of actor path going
        to Kevin Bacon
    """

    return actor_path(transformed_data, 4724, lambda actor: actor == actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Finds shortest path between two actors

    Args:
        transformed_data (list): A list of two dicts
        one for actors and one for movies
        actor dict has keys of actor ids and
        values of a set of every actor they have
        acted with. Movies dict has movie id
        keys and values of a set of actor ids of
        actors in that movie
        actor_id_1 (int): actor id
        actor_id_2 (int): actor id

    Returns:
        list: shortest list of actor id's of
        path connecting actor_id_1 and
        actor_id_2
    """

    return actor_path(transformed_data, actor_id_1, lambda actor: actor == actor_id_2)


def movie_path(transformed_data, actors_path):
    """
    Using an actor path returns a path of
    movies that connects them

    Args:
        transformed_data (list): A list of two dicts
        one for actors and one for movies
        actor dict has keys of actor ids and
        values of a set of every actor they have
        acted with. Movies dict has movie id
        keys and values of a set of actor ids of
        actors in that movie
        actors_path (list): list of actor ids

    Returns:
        list: movie id list
    """
    movie_pathway = []

    movie_info = transformed_data[1]
    for i, current_actor in enumerate(actors_path):
        # check to see if already checked all
        if i + 1 == len(actors_path):
            break
        for movie in movie_info:
            if current_actor in movie_info[movie]:
                if actors_path[i + 1] in movie_info[movie]:
                    movie_pathway.append(movie)

    return movie_pathway


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Finds the shortest path between an actor and an
    actor in a specific group/with a constraint

    Args:
        transformed_data (list): A list of two dicts
        one for actors and one for movies
        actor dict has keys of actor ids and
        values of a set of every actor they have
        acted with. Movies dict has movie name
        keys and values of a set of actor ids of
        actors in that movie
        actor_id_1 (int): actor id
        goal_test_function (func): Any function that takes
        an actor id and returns true or false based if it
        applies to the group

    Returns:
        list: list of actor ids that form the shortest
        path between actor_id_1 and an actor that applies
        to the rule of goal_test_function
    """
    actor_db = transformed_data[0]
    # if path of 1
    if goal_test_function(actor_id_1):
        return [actor_id_1]

    # create agenda and visited list
    agenda = [(actor_id_1,)]
    visited = {actor_id_1}

    # while still things to check in agends
    while agenda:
        path = agenda.pop(0)
        current_actor = path[-1]
        # check actors related to current
        for actor in actor_db[current_actor]:
            new_path = path + (actor,)
            if goal_test_function(actor):
                return list(new_path)
            if actor not in visited:
                agenda.append(new_path)
                visited.add(actor)
    # if agenda empty and dont find valid actor
    return None


def actors_connecting_films(transformed_data, film1, film2):
    """
    Finds the shortest list of actor ids
    that connect the two films

    Args:
        transformed_data (list): A list of two dicts
        one for actors and one for movies
        actor dict has keys of actor ids and
        values of a set of every actor they have
        acted with. Movies dict has movie id
        keys and values of a set of actor ids of
        actors in that movie
        film1 (int): film id
        film2 (int): film id

    Returns:
        list: shortest list of actor id path that
        connects film1 and film2
    """
    movies = transformed_data[1]
    actors_1 = movies[film1]
    actors_2 = movies[film2]

    path_options = set()
    for a1 in actors_1:
        for a2 in actors_2:
            # find shortest path
            new_path = actor_to_actor_path(transformed_data, a1, a2)
            if new_path is not None:
                path_options.add(tuple(new_path))

    # if no paths exist
    if path_options == set():
        return None
    shortest_path = min(path_options, key=len)

    return list(shortest_path)


if __name__ == "__main__":
    # with open("resources/small.pickle", "rb") as f:
    #     smalldb = pickle.load(f)
    with open("resources/names.pickle", "rb") as f:
        names = pickle.load(f)
    with open("resources/movies.pickle", "rb") as h:
        movie_names = pickle.load(h)
    # #print(names)
    # print(names["Jon Davison"])
    # name_wanted = ""
    # actors = names.keys()
    # for a in actors:
    #     if names[a] == 121192:
    #         name_wanted = a
    # data = transform_data(smalldb)
    # id_1 = names["Theresa Russell"]
    # id_2 = names["Jennifer Taylor"]
    # print(acted_together(data, id_1, id_2))
    # id1 = names["Stanislas Crevillen"]
    # id2 = names["Stephen Blackehart"]
    # print(acted_together(data, id1, id2))

    # print("desired person: ", name_wanted)
    with open("resources/tiny.pickle", "rb") as a:
        tiny = pickle.load(a)
    # transformed_data = transform_data(tiny)
    # small_path = bacon_path(transformed_data, 1640)
    # print("path", small_path)
    # words = names.keys()
    # numbers = names.values()
    with open("resources/large.pickle", "rb") as b:
        large = pickle.load(b)
    desired_id = names["Helen Holmes"]
    # transformed_data = transform_data(large)
    # final_large_path = bacon_path(transformed_data, desired_id)
    # print("final_path", final_large_path)
    # print(names)

    # movie path code
    # id_1 = names["Ellen Barkin"]
    # id_2 = names["Vjeran Tin Turk"]
    # actor_path_1 = actor_to_actor_path(transformed_data, id_1, id_2)
    # movie_ans = movie_path(transformed_data, actor_path_1)
    # print('the movie id path is: ', movie_ans)
    # name_mov = []
    # for mov in movie_ans:
    #     for m in movie_names:
    #         if movie_names[m] == mov:
    #             name_mov.append(m)

    # print("the movie name path is: ", name_mov)

    # find actor to actor path:
    # id_1 = names["Helen Holmes"]
    # act_path = bacon_path(transformed_data, id_1)
    # act_names = []
    # for a in act_path:
    #     for ac in names:
    #         if names[ac] == a:
    #             act_names.append(ac)
    # print("actor name path is:", act_names)

    # arbitrary path finder:
    id__1 = names["Heinz Strunk"]
    id__2 = names["Barry Levinson"]
    # small_path = actor_to_actor_path(transformed_data, id__1, id__2)
    # print("arb numbs")
    snp = []
    # for s in small_path:
    #     for n in names:
    #         if names[n] == s:
    #             snp.append(n)

    # print("arb path names:", snp)

    # developing tiny pickle test case for acyor to actor path
    # print("this is tiny db:" ,tiny)

    # actor_info = transformed_data[0]
    # actors_one = []
    # # for one
    # for i in actor_info:
    #     if 4724 in actor_info[i]:
    #         if actor_info[i] != 4724:
    #             actors_one.append(i)
    # print("the count for 1 is: ", actors_one)
    # actors_two = set()
    # for i in actor_info:
    #     for h in actors_one:
    #         if h in actor_info[i] and actor_info[i] not in actors_one:
    #             actors_two.add(i)
    # print("the count for two is: ", actors_two)
    # actors_three = set()
    # actorstwo = {1640}
    # for i in actor_info:
    #     for h in actorstwo:
    #         if h in actor_info[i]:
    #             for v in actors_one:
    #                 if v not in actor_info[i]:
    #                     actors_three.add(i)
    # print("three :", actors_three)

    # check bacon number levels
    # ans = actors_with_bacon_number(transformed_data, 6)
    # print("bacon number set ids:", ans)
    # name_bac = []
    # for s in ans:
    #     for na in names:
    #         if names[na] == s:
    #             name_bac.append(na)

    # print("correct bac nam:", name_bac)
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
