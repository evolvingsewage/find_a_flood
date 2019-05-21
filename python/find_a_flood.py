import argparse
import database
import distance
import parse

def main(args):
    """ Return the rivers of a category within a radius of a city
    Args:
        args
    Returns:
        None
    """
    database.init_river_db(args["refresh_data"])
    if args["category"]:
        rivers = distance.get_rivers_within_dist(args["city"], args["state"],
                                                 args["radius"], args["category"])
        category = args["category"].replace("_", " ")
    else:
        rivers = distance.get_rivers_within_dist(args["city"], args["state"],
                                                 args["radius"])
        category = "Major Stage"

    if rivers:
        for distance_float, river_info in sorted(rivers.items()):
            river_info_string = ("{0} is about {1} miles away from {2}, {3} and is in the "
                                 "{4} category of flooding."
                                 "\n{0}'s coordinates are {5}.").format(river_info[0],
                                                                     round(distance_float),
                                                                     args["city"], args["state"],
                                                                     category, river_info[2])

            print(river_info_string)
    else:
        river_info_string = ("No rivers are in the {0} category within {1} "
                             "miles of {2}, {3}").format(category, args["radius"],
                                                         args["city"], args["state"])
        print(river_info_string)


def parse_args():
    """ Returns arguments from the command line
    Args:
        None
    Returns:
        args - the argparser object with args from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="The name of a city.", type=str)
    parser.add_argument("state",
                        help="The two letter abbreviation of the state the city is in.",
                        type=str)
    parser.add_argument("radius", type=int, help="The search radius, in miles.")
    parser.add_argument("--category", type=str, choices=["Low_Water", "No_Flooding",
                                     "Action_Stage","Minor_Stage", "Moderate_Stage",
                                     "Minor_Stage", "Major_Stage", "Observations_are_not_current",
                                     "Not_Defined"],
                        help="The category of flooding to search for.")
    parser.add_argument("--refresh_data", action="store_true",
                        help="""Whether or not to re-sync the database of results.""")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    args = vars(args)
    main(args)
