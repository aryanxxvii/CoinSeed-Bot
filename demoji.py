import emoji

string = ":fishing_pole:"
demoji = emoji.demojize("🍑 ")   # This takes the emoji and gives--> :fishing_pole:
emoji = emoji.emojize(string)    # This takes :fishing_pole: and gives--> :fishing_pole_and_fish:    
print(demoji)
print(emoji)
