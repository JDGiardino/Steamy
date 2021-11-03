from dataclasses import dataclass


@dataclass(frozen=True)
class Achievement:
    name: str
    percent: float




"""

# myAchievement = Achievement(foo=100, bar=hi)X

some_dict_I_got_from_an_api = {
    foo: 100
    bar: hi
    baz: xyz
}

myAchievement = Achievement(**some_dict_I_got_from_an_api)

myAchievement = Achievemewnt(foo=some_dict["foo"], bar=some_dict["bar"]


"""

""""# TODO can be filter this a bit more simply?
    rarest_achievement = min(x["percent"] for x in json_achievement_list)
    for x in json_achievement_list:
        if x["percent"] == rarest_achievement:
            return Achievement(**x)

    # best thing is to use a filter function
        # TO DO research filter"""






    # two ways
    # since our Achievement matches the expected json exactly, I think we can do this:
    #result = Achievement(**x)
    # which is basically doing this under the hood
    # result = Achievement(name=x["name"], percent=x["percent"])
