import random
from numpy.random import normal

class TastingNote:

    AROMA_POOL_WHITE = ("Smoke", "Petrol", "Toast", "Ginger", "Fresh Bread", "Almond", "Honey")
    AROMA_POOL_RED = ("Smoke", "Barnyard", "Toast", "Cola", "Game")

    def __init__(self, wine, accuracy):
        self.wine = wine

        self.accuracy = accuracy

        self.label_color = wine.label_color
        self.clarity = wine.clarity
        self.appearance_other = wine.appearance_other
        self.condition = wine.condition
        self.nose_intensity = self.randomize_ordinal(accuracy, wine.nose_intensity) 
        self.development = self.randomize_ordinal(accuracy, wine.development)
        self.petillance = self.randomize_ratio(accuracy, wine.petillance) 
        self.sweetness = self.randomize_ratio(accuracy, wine.sweetness) 
        self.acidity = self.randomize_ratio(accuracy, wine.acidity) 
        self.alcohol = self.randomize_ratio(accuracy, wine.alcohol) 
        self.body = self.randomize_ordinal(accuracy, wine.body)
        self.tannin_or_bitterness = self.randomize_ordinal(accuracy, wine.tannin_or_bitterness)
        self.finish = self.randomize_ordinal(accuracy, wine.finish)
        self.fruit_color = self.randomize_ordinal(accuracy, wine.fruit_color)
        self.fruit_family = self.randomize_ordinal(accuracy, wine.fruit_family)
        self.fruit_ripeness = self.randomize_ordinal(accuracy, wine.fruit_ripeness)
        self.fruit_subcondition = self.randomize_ordinal(accuracy, wine.fruit_subcondition)
        self.floral = self.randomize_ordinal(accuracy, wine.floral)
        self.herbaceous = self.randomize_ordinal(accuracy, wine.herbaceous)
        self.herbal = self.randomize_ordinal(accuracy, wine.herbal)
        self.earth_organic = self.randomize_ordinal(accuracy, wine.earth_organic)
        self.earth_inorganic = self.randomize_ordinal(accuracy, wine.earth_inorganic)
        self.grape_spice = self.randomize_ordinal(accuracy, wine.grape_spice)
        self.oak_aroma = self.randomize_ordinal(accuracy, wine.oak_aroma)
        self.oak_intensity = self.randomize_ratio(accuracy, wine.oak_intensity)
        self.aroma_other = self.randomize_other(accuracy, wine.aroma_other)

        # will be implemented once display is graphical
        self.appearance_red = wine.appearance_red
        self.appearance_green = wine.appearance_green
        self.appearance_blue = wine.appearance_blue


    def generate_description(self):
        output = []

        output.append(
            f"This is a {self.get_petillance()}, "
            f"{self.get_clarity()} "
            f"{self.get_label_color()} wine.\n"
            f"The nose is of {self.get_nose_intensity()} "
            f"intensity and it is {self.get_development()}.\n"
            f"The wine is {self.get_sweetness()}, "
            f"Acidity is {self.get_acidity()}, "
            f"Alcohol is {self.get_alcohol()}, "
            f"Body is {self.get_body()}, "
        )
        if self.label_color == "Red":
            output.append(f"Tannin is {self.get_tannin_or_bitterness()}, ")
        elif self.check_for_bitterness():
            output.append(f"Bitterness is {self.get_tannin_or_bitterness()}, ")
        
        output.append(
            f"and the finish is {self.get_finish()}.\n"
            f"The wine shows {self.get_fruit_ripeness()} "
            f"{self.get_fruit_color()} {self.get_fruit_family()} fruit"
        )

        if self.check_for_fruit_subcondition():
            output.append(
                f", with a {self.get_fruit_subcondition()} character.\n"
            )
        else:
            output.append(".\n")

        if self.check_for_floral() and self.check_for_herbaceous():    
            output.append(
                f"The wine shows a {self.get_floral()} florality, "
                f"and {self.get_herbaceous()} herbaceousness.\n"
            )
        elif self.check_for_floral():
            output.append(f"The wine shows a {self.get_floral()} florality.\n")
        elif self.check_for_herbaceous():
            output.append(
                f"The wine shows a {self.get_herbaceous()} herbaceousness.\n"
            )
        
        if self.check_for_earth_organic() and self.check_for_earth_inorganic():
            output.append(
                f"It has a {self.get_earth_organic()} earthiness, "
                f"and a {self.get_earth_inorganic()} minerality.\n"
            )
        elif self.check_for_earth_organic():
            output.append(f"It has a {self.get_earth_organic()} earthiness.\n")
        elif self.check_for_earth_inorganic():
            output.append(f"It has a {self.get_earth_inorganic()} minerality.\n")
        
        misc_list = self.generate_misc_list()
        misc_length = len(misc_list)

        if misc_length > 0:
            output.append(f"Finally, there are notes of ")
            if misc_length == 1:
                output.append(f"{misc_list[0]}.\n")
            elif misc_length == 2:
                output.append(f"{misc_list[0]} and {misc_list[1]}.")
            else:
                for i in range(misc_length):
                    output.append(f"{misc_list[i]}")
                    if i == misc_length - 2:
                        output.append(f" and ")
                    elif i == misc_length - 1:
                        output.append(".")
                    else:
                        output.append(", ")
        
        output.append('\n')

        output_string = ''.join(output)
        return output_string
    
    def get_petillance(self):
        if self.petillance >= 94:
            return "Sparkling"
        elif self.petillance >= 39:
            return "Semi-Sparkling"
        elif self.petillance >= 20:
            return "Spritzy"
        elif self.petillance < 20:
            return "Still"
        else:
            return "Error outputting get_petillance"
    
    def get_clarity(self):
        return self.clarity
    
    def get_label_color(self):
        return self.label_color
    
    def get_nose_intensity(self):
        if self.nose_intensity >= 204:
            return "High"
        elif self.nose_intensity >= 153:
            return "Medium-Plus"
        elif self.nose_intensity >= 102:
            return "Medium"
        elif self.nose_intensity >= 51:
            return "Medium-Minus"
        elif self.nose_intensity < 51:
            return "Low"
        else:
            return "Error outputting nose_intensity"
    
    def get_development(self):
        if self.development >= 170:
            return "Mature"
        elif self.development >= 85:
            return "Developing"
        elif self.development < 85:
            return "Youthful" 
        else:
            return "Error outputting get_development"
    
    def get_sweetness(self):
        if self.sweetness >= 115:
            return "Very Sweet"
        elif self.sweetness >= 45:
            return "Sweet"
        elif self.sweetness >= 12:
            return "Medium-Sweet"
        elif self.sweetness >= 5:
            return "Medium-Dry"
        elif self.sweetness < 5:
            return "Dry"
        else:
            return "Error outputting get_sweetness"
    
    def get_acidity(self):
        if self.acidity >= 204:
            return "High"
        elif self.acidity >= 153:
            return "Medium-Plus"
        elif self.acidity >= 102:
            return "Medium"
        elif self.acidity >= 51:
            return "Medium-Minus"
        elif self.acidity < 51:
            return "Low"
        else:
            return "Error outputting get_acidity"
    
    def get_alcohol(self):
        return f"{self.alcohol / 10}%"
    
    def get_body(self):
        if self.body >= 204:
            return "Full"
        elif self.body >= 153:
            return "Medium-Plus"
        elif self.body >= 102:
            return "Medium"
        elif self.body >= 51:
            return "Medium-Minus"
        elif self.body < 51:
            return "Light"
        else:
            return "Error outputting get_body"
        
    def get_tannin_or_bitterness(self):
        if self.tannin_or_bitterness >= 204:
            return "High"
        elif self.tannin_or_bitterness >= 153:
            return "Medium-Plus"
        elif self.tannin_or_bitterness >= 102:
            return "Medium"
        elif self.tannin_or_bitterness >= 51:
            return "Medium-Minus"
        elif self.tannin_or_bitterness >= 30:
            return "Low"
        elif self.tannin_or_bitterness < 30:
            return "None"
        else:
            return "Error outputting get_tannin_or_bitterness"
    
    def get_finish(self):
        if self.finish >= 204:
            return "Long"
        elif self.finish >= 153:
            return "Medium-Plus"
        elif self.finish >= 102:
            return "Medium"
        elif self.finish >= 51:
            return "Medium-Minus"
        elif self.finish < 51:
            return "Short"
        else:
            return "Error outputting get_finish"
    
    def get_fruit_ripeness(self):
        if self.fruit_ripeness >= 204:
            return "Jammy"
        elif self.fruit_ripeness >= 153:
            return "Overripe"
        elif self.fruit_ripeness >= 102:
            return "Ripe"
        elif self.fruit_ripeness >= 51:
            return "Just-ripe"
        elif self.fruit_ripeness < 51:
            return "Unripe"
        else:
            return "Error outputting get_fruit_ripeness"
        
    def get_fruit_color(self):
        if self.label_color == "White":
            return self.get_white_color()
        elif self.label_color == "Red":
            return self.get_red_color()
        else:
            return "Fruit color error. (Only white/red currently implemented)"
    
    def get_white_color(self):
        if self.fruit_color >= 215:
            return "Deep Orange"
        elif self.fruit_color >= 172:
            return "Orange"
        elif self.fruit_color >= 129:
            return "Yellow-Orange"
        elif self.fruit_color >= 86:
            return "Yellow"
        elif self.fruit_color >= 43:
            return "Greenish"
        elif self.fruit_color < 43:
            return "Green"
        else:
            return "Error outputting get_white_color"
    
    def get_red_color(self):
        if self.fruit_color >= 215:
            return "Black"
        elif self.fruit_color >= 172:
            return "Blue"
        elif self.fruit_color >= 129:
            return "Purple"
        elif self.fruit_color >= 86:
            return "Deep Red"
        elif self.fruit_color >= 43:
            return "Red"
        elif self.fruit_color < 43:
            return "Orange"
        else:
            return "Error outputting get_red_color"

    def get_fruit_family(self):
        if self.label_color == "White":
            return self.get_white_family()
        elif self.label_color == "Red":
            return self.get_red_family()
        else:
            return "Fruit family error. (Only white/red currently implemented)"
    
    def get_white_family(self):
        if self.fruit_family >= 224:
            return "Sweet Melon"
        elif self.fruit_family >= 196:
            return "Sweet Tropical"
        elif self.fruit_family >= 168:
            return "Sweet Stone"
        elif self.fruit_family >= 140:
            return "Sweet Pome"
        elif self.fruit_family >= 112:
            return "Tart Tropical"
        elif self.fruit_family >= 84:
            return "Tart Stone"
        elif self.fruit_family >= 56:
            return "Sweet Citrus"
        elif self.fruit_family >= 28:
            return "Tart Pome"
        elif self.fruit_family < 28:
            return "Tart Citrus"
        else:
            return "White fruit error"
    
    def get_red_family(self):
        if self.fruit_family >= 200:
            return "Sweet Stone"
        elif self.fruit_family >= 143:
            return "Sweet Berry"
        elif self.fruit_family >= 86:
            return "Tart Stone"
        elif self.fruit_family >= 29:
            return "Tart Berry"
        elif self.fruit_family < 29:
            return "Vegetal"
        else:
            return "Red fruit error"

    def get_fruit_subcondition(self):
        if self.fruit_subcondition >= 217:
            return "Baked"
        elif self.fruit_subcondition >= 178:
            return "Cooked"
        elif self.fruit_subcondition >= 139:
            return "Dried"
        elif self.fruit_subcondition >= 39:
            return "None"
        elif self.fruit_subcondition < 39:
            return "Candied"
        else:
            return "Error outputting get_fruit_subcondition"

    def get_floral(self):
        if self.label_color == "White":
            if self.floral >= 238:
                return "Soap"
            elif self.floral >= 210:
                return "Perfume"
            elif self.floral >= 182:
                return "Geranium"
            elif self.floral >= 154:
                return "Rose"
            elif self.floral >= 126:
                return "Jasmine"
            elif self.floral >= 98:
                return "Honeysuckle"
            elif self.floral >= 70:
                return "Faint White Flowers"
            elif self.floral < 70:
                return "None"
            else:
                return "White floral error"
        elif self.label_color == "Red":
            if self.floral >= 225:
                return "Soap"
            elif self.floral >= 194:
                return "Perfume"
            elif self.floral >= 163:
                return "Lilac"
            elif self.floral >= 132:
                return "Rose"
            elif self.floral >= 101:
                return "Violets"
            elif self.floral >= 70:
                return "Faint Purple Flowers"
            elif self.floral < 70:
                return "None"
            else:
                return "Red floral error"
        else:
            return "Floral error. (Only white/red are implemented yet)"

    def get_herbaceous(self):
        if self.herbaceous >= 212:
            return "Green Bell Pepper"
        elif self.herbaceous >= 168:
            return "Grassy"
        elif self.herbaceous >= 124:
            return "Asparagus"
        elif self.herbaceous >= 80:
            return "Faint Green"
        elif self.herbaceous < 80:
            return "None"
        else:
            return "Error outputting get_herbaceous"

    def get_earth_organic(self):
        if self.earth_organic >= 216:
            return "Compost"
        elif self.earth_organic >= 174:
            return "Forest Floor"
        elif self.earth_organic >= 132:
            return "Potting Soil"
        elif self.earth_organic >= 90:
            return "White Mushroom"
        elif self.earth_organic < 90:
            return "None"
        else:
            return "Error outputting get_earth_organic"

    def get_earth_inorganic(self):
        if self.earth_inorganic >= 230:
            return "Scraped Steel"
        elif self.earth_inorganic >= 202:
            return "Flinty"
        elif self.earth_inorganic >= 174:
            return "Chalky"
        elif self.earth_inorganic >= 146:
            return "Slatey"
        elif self.earth_inorganic >= 118:
            return "Wet Pavement"
        elif self.earth_inorganic >= 90:
            return "Wet Stone"
        elif self.earth_inorganic < 90:
            return "None"
        else:
            return "Error outputting get_earth_inorganic"

    def get_herbal(self):
        if self.herbal >= 210:
            return "Medicinal Herbs"
        elif self.herbal >= 165:
            return "Garrigue"
        elif self.herbal >= 120:
            return "Faint Dried Herbs"
        elif self.herbal < 120:
            return "None"
        else:
            return "Error outputting get_herbal"
    
    def get_grape_spice(self):
        if self.grape_spice >= 226:
            return "White Pepper"
        elif self.grape_spice >= 198:
            return "Black Pepper"
        elif self.grape_spice >= 169:
            return "Black Licorice"
        elif self.grape_spice >= 140:
            return "Fennel"
        elif self.grape_spice < 140:
            return "None"
        else:
            return "Error outputting get_grape_spice"
    
    def get_oak(self):
        if self.get_oak_intensity() == "None":
            return "None"
        else:
            return f"{self.get_oak_intensity()} aromas of {self.get_oak_aroma()}"
    
    def get_oak_aroma(self):
        if self.oak_aroma >= 222:
            return "Coffee"
        elif self.oak_aroma >= 185:
            return "Mocha"
        elif self.oak_aroma >= 148:
            return "Caramel"
        elif self.oak_aroma >= 111:
            return "Vanilla"
        elif self.oak_aroma >= 74:
            return "Baking Spice"
        elif self.oak_aroma >= 37:
            return "Sandalwood"
        elif self.oak_aroma < 37:
            return "Sawdust"
        else:
            return "Error outputting oak_aroma"
    
    def get_oak_intensity(self):
        if self.oak_intensity >= 216:
            return "Intense"
        elif self.oak_intensity >= 174:
            return "Strong"
        elif self.oak_intensity >= 132:
            return "Moderate"
        elif self.oak_intensity >= 90:
            return "Faint"
        elif self.oak_intensity < 90:
            return "None"
        else:
            return "Error oak_intensity"
    
    def get_aroma_other(self):
        return self.aroma_other
    
    def check_for_bitterness(self):
        if self.get_tannin_or_bitterness() != "None":
            return True
        else:
            return False
    
    def check_for_fruit_subcondition(self):
        if self.get_fruit_subcondition() != "None":
            return True
        else:
            return False
    
    def check_for_floral(self):
        if self.get_floral() != "None":
            return True
        else:
            return False
    
    def check_for_herbaceous(self):
        if self.get_herbaceous() != "None":
            return True
        else:
            return False
    
    def check_for_herbal(self):
        if self.get_herbal() != "None":
            return True
        else:
            return False
    
    def check_for_earth_organic(self):
        if self.get_earth_organic() != "None":
            return True
        else:
            return False
    
    def check_for_earth_inorganic(self):
        if self.get_earth_inorganic() != "None":
            return True
        else:
            return False
    
    def check_for_grape_spice(self):
        if self.get_grape_spice() != "None":
            return True
        else:
            return False
    
    def check_for_oak(self):
        if self.get_oak() != "None":
            return True
        else:
            return False
    

    # these characteristics are all output together for user, so check how many
    # need to be displayed to determine formatting

    # we can't just use len() here because these return "None"
    # instead of None. should this change?
    def check_quantity_others(self):
        count = 0

        if self.check_for_oak():
            count += 1
        if self.check_for_grape_spice():
            count += 1
        if self.check_for_herbal():
            count += 1
        count += self.check_quantity_aroma_other()

        return count
    
    def check_quantity_aroma_other(self):
        if self.aroma_other == "None":
            return 0
        else:
            return len(self.aroma_other.split(','))
    
    def generate_aroma_other_list(self):
        output_list = self.aroma_other.split(',')
        return output_list
    
    # oak, grape_spice, herbal, and 0-9 aroma_other used in
    # final text output section
    def generate_misc_list(self):
        output_list = []

        if self.check_for_grape_spice():
            output_list.append(self.get_grape_spice())
        if self.check_for_herbal():
            output_list.append(self.get_herbal())
        if self.check_quantity_aroma_other():
            for item in self.generate_aroma_other_list():
                output_list.append(item)
        if self.check_for_oak():
            output_list.append(self.get_oak())
        
        return output_list
    
    # randomization functions used to introduce inaccuracy
    # in the tasting note

    # only to be used on attributes that are ordinal scales (ie. aromas)
    # not on ratio scales (ie. alcohol, sweetness)
    def randomize_ordinal(self, accuracy, value):
        RANDOMNESS = 15
        if accuracy == 5:
            return int(value)
        else:
            return int(normal(loc = value, scale = (RANDOMNESS * (5 - accuracy)), size = 1)[0])
    
    # only for ratio scales, see note on randomize_ordinal()
    def randomize_ratio(self, accuracy, value):
        RANDOMNESS = 0.045
        if accuracy == 5:
            return int(value)
        else:
            return int(normal(loc = value, scale = (int((value * RANDOMNESS)) * (5 - accuracy)), size = 1)[0])
    
    # randomly remove or insert "other" aromas
    def randomize_other(self, accuracy, comma_separated_string):
        
        # chance of change = 1 in X
        DELETE_CHANCE = 10
        INSERT_CHANCE = 20
        
        delete_count = 0
        insert_count = 0

        if accuracy == 5:
            return comma_separated_string
        
        aroma_pool = self.get_aroma_pool()


        for i in range(5 - accuracy):
            if random.randint(1, DELETE_CHANCE) == DELETE_CHANCE:
                delete_count += 1
            if random.randint(1, INSERT_CHANCE) == INSERT_CHANCE:
                insert_count += 1
        
        if comma_separated_string == "None":
            comma_separated_string = ""

        if comma_separated_string:
            aromas_list = comma_separated_string.split(",")
        else:
            aromas_list = []

        while len(aromas_list) > 0 and delete_count > 0:
            random.shuffle(aromas_list)
            del aromas_list[0]
            delete_count -= 1
        
        for i in range(insert_count):
            random_aroma = random.choice(aroma_pool)
            if random_aroma not in aromas_list:
                aromas_list.append(random_aroma)
        
        if not aromas_list:
            aromas_list.append("None")

        random.shuffle(aromas_list)
        aromas_string = ",".join(aromas_list)
        return aromas_string
    
    def get_aroma_pool(self):
        try:
            if self.label_color == "White":
                return self.AROMA_POOL_WHITE
            elif self.label_color == "Red":
                return self.AROMA_POOL_RED
        except:
            return ()

    def __repr__(self):
        return self.generate_description()