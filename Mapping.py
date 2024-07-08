import pandas as pd

class Mapping:

    Relevance_levels = {
        5: 'Navigational',
        4: 'Excellent',
        3: 'Good',
        2: 'Acceptable',
        1: 'Bad'
    }

    Accuracy_levels = {
        3: 'Correct',
        2: 'Partially Correct',
        1: 'Incorrect',
        0: 'Cant verify',
        -1: 'n/a',
        -2: 'Correct with formating'
    }

    Pin_levels = {
        4: 'Perfect',
        3: 'Approximate',
        2: 'Next Door',
        1: 'Wrong',
        0: 'Cant verify'
    }

    demoted_scores = []
    demotion_reason = []
    resulting_scores = []

    def __init__(self) -> None:
        '''These values represent the best rating
        for each category, which might be demoted later on'''

        self.relevance_score = 5
        self.name_score = 3
        self.category_score = 3
        self.address_score = 3
        self.pin_score = 4


    ####################################################################

    def infinite_blank_check(self, loc_intents:list[str], self_iter) -> str:
        rep = len(loc_intents)
        lap = 1

        while lap != rep:
            if self_iter == lap:
                self_comment = loc_intents[lap-1]
            lap =+ 1
        
        return self_comment

    def fresh_viewport(self) -> None:
        str_list = ['User Location','Viewport > User Location','Viewport']
        self.comment_location_intent = self.infinite_blank_check(str_list, self.user_location)


    def stale_viewport(self) -> None:
        if self.user_location == 1:
            self.comment_location_intent = 'User Location'
        elif self.user_location == 2:
            self.comment_location_intent = 'User Location'
        elif self.user_location == 3:
            self.comment_location_intent = 'Stale Viewport'

    def missing_viewport(self) -> None:
        if self.user_location == 1:
            self.comment_location_intent = 'User Location'
        elif self.user_location == 2:
            self.comment_location_intent = 'Test Locale'

    def explicit_location(self) -> None:
        self.explicit_intent = int(input('----Select Explicit Intent \n\n1. Specific Location, \n2. Near me'))

        if self.explicit_intent == 1:
            self.comment_location_intent = 'Ignore User and Viewpoint Location'
        elif self.explicit_intent == 2:
            self.comment_location_intent = 'User Location'

    def implicit_location(self) -> None:
        self.viewport_type = int(input('----Select Viewport type \n\n1. Fresh, \n2. Stale, \n3. Age Missing, \n4. Missing'))

        if self.viewport_type < 3:
            self.user_location = int(input('----Select User Location \n\n1. Inside Viewport, \n2. Outside Viewport, \n3. Missing'))

            if self.viewport_type == 1:
                self.fresh_viewport()
            elif self.viewport_type == 2:
                self.stale_viewport()

        elif self.viewport_type > 3:
            self.user_location = int(input('----Select User Location \n\n1. Present, \n2. Missing'))

            if self.viewport_type == 3:
                self.fresh_viewport()
            elif self.viewport_type == 4:
                self.missing_viewport()

    def get_query_type(self) -> None:
        self.query_type = int(input('----Select Queary Type \n\n1. Address(street number, street name, locality, state, country, and postal code), \n2. Point of Interest(POI), \n3. Business, \n4. Category, \n5. Products and Service, \n6. Coordinates or My location, \n7. Emoji, \n8. No map Intent'))
        
        dict_query_types = {
            1: 'Address',
            2: 'Point of Interest',
            3: 'Business',
            4: 'Category',
            5: 'Products and Service',
            6: 'Coordinates or My location',
            7: 'Emoji',
            8: 'No map Intent',
        }

        self.comment_query_type = dict_query_types[self.query_type]
        print(f'***QUERY TYPE = {self.comment_query_type}')

    def get_location_intent(self) -> None:
        self.location_type = int(input('----Select Location Intent \n\n1. Explicit (Specific), \n2. Implicit (Not Specific)'))
        
        if self.location_type == 2:
            self.implicit_location()

        elif self.location_type == 1:
            self.explicit_location()

        print(f'***LOCATION INTENT = {self.comment_location_intent}')
    
    def user_intent(self) -> None:
        self.get_query_type()
        self.get_location_intent()

    def navigational(self) -> None:
        nav_test = int(input('----Is this a Navigational Intent? \nThe intent is unique and clear enough that there is only a single result in the world \n\n1. Yes \n2. No'))
        if nav_test == 1:
            self.comment_navigation = True
        else:
            self.comment_navigation = False
            self.relevance_score = 4
        
        print(f'***NAVIGATIONAL? = {self.comment_navigation}')

    def language_test(self) -> None:
        result_language_test = int(input('----Is the language matching for test_locale, query, and result region? \n\n1. Yes \n2. No'))
        if result_language_test == 1:
            self.comment_language = True
        else:
            self.comment_language = False

        print(f'***LANGUAGE MATCH = {self.comment_language}')

    def closure_test(self) -> None:
        result_closure_test = int(input('----Is the status PERMANENT_CLOSURE? \n\n1. Yes \n2. No'))
        if result_closure_test == 1:
            self.comment_closure = True
            exp = int(input('Is this result Expected? \nIt completely satisfies user intent or there are no other options? \n\n1. Yes \n2. No '))
            if exp == 2:
                self.relevance_score = 2
        else:
            self.comment_closure = False
        
        print(f'***PERMANENT_CLOSURE = {self.comment_closure}')

    def result_level_issues(self) -> None:
        self.language_test()
        self.closure_test()

    def demotion(self, score, demoted, demotion_comment, demotion = 1) -> int:
        self.demotion_reason.append(demotion_comment)
        self.demoted_scores.append(demoted)
        
        if score == 1:
            pass
        else:
            score -= demotion
            if score < 1:
                score = 1

        self.resulting_scores.append(score)
        
        return score
    
    def no_other_options(self) -> None:
        result_option_test = int(input('----Are there any better results not shown? \n\n1. Yes \n2. No '))
        if result_option_test == 1:
            self.comment_options = True
            demotion_req = int(input('----Does it require demotion? \n\n1. Yes \n2. No '))
            if demotion_req == 1:
                amount = input('----How many points?')
                demotion_comment = 'Due to missing options that fit the query better'
                self.relevance_score = self.demotion(self.relevance_score, 'Relevance', demotion_comment, demotion = amount)
        else:
            self.comment_options = False

        print(f'***Other options available = {self.comment_options}')

    def is_legal(self) -> None:
        result_ilegal_test = int(input('----Is it unexpectedly inappropriate? \n\n1. Yes \n2. No '))
        if result_ilegal_test == 1:
            self.comment_legal = True
            self.relevance_score = 1
        else:
            self.comment_legal = False

        print(f'***Unexpected inappropriate results = {self.comment_legal}')

    def query_result_connection(self) -> None:
        result_connection_test_p1 = int(input('----Does the connection satisfy intent? \nGeneral, Abbreviation/Alternate, Category, Spell Correction \nTransit, Special Character, Address? \n\n1. Yes \n2. No '))
        if result_connection_test_p1 == 1:
            result_connection_test_p2 = int(input('----Is it address? \n\n1. Yes \n2. No '))
            if result_connection_test_p2 == 1:
                result_connection_test_p3 = int(input('----What is missing? \n\n1. Unit Number \n2. Incomplete \n3. Wrong \n4. None'))
                if result_connection_test_p3 == 1:
                    self.comment_connection = 'Address wth no Unit #'
                    self.relevance_score = 3
                elif result_connection_test_p3 == 2:
                    self.comment_connection = 'Incomplete Address'
                    self.relevance_score = 2
                elif result_connection_test_p3 == 3:
                    self.comment_connection = 'Wrong Address'
                    self.relevance_score = 1
                else:
                    self.comment_connection = 'Good Address'
            else:
                self.comment_connection = 'Not Address'
        else:
            self.comment_connection = 'None'
            self.relevance_score = 1

        print(f'***Query connection type = {self.comment_connection}')

    def prominence(self) -> None:
        result_prominence_test = int(input('----Should there be a promotion due to interantional prominence? \n\n1. Yes \n2. No '))
        if result_prominence_test == 1:
            self.comment_prominence = 'International'
            self.relevance_score = 3
        else:
            self.comment_prominence = 'No Promotion'

        print(f'***Prominence Promotion = {self.comment_prominence}')
    
    def distance(self) -> None:
        result_many_test3 = int(input('----How far is the location from viewport? \n\n1. Near \n2. Near-ish \n3. Far-ish \n4. Far'))
        if result_many_test3 == 1:
            self.comment_relevance = min(self.relevance_score,4)
        elif result_many_test3 == 2:
            self.comment_relevance = min(self.relevance_score,3)
        elif result_many_test3 == 3:
            self.comment_relevance = min(self.relevance_score,2)
        elif result_many_test3 == 5:
            self.comment_relevance = min(self.relevance_score,1)
        
        print(f'***{self.relevance_type} Relevance  = {self.comment_relevance}')

    def many_possible_results(self) -> None:
        '''Many results that could satisfy the user'''

        self.relevance_type = 'Many possible options'
        print(f'***Relevance Type  = {self.relevance_type}')
        if self.user_location == 1:
            result_many_test = int(input('----How far is the location from user? \n\n1. Near/In \n2. Near-ish/In \n3. Far/In \n4. Near/Out \n5. Far/Out'))
            if result_many_test == 1 | result_many_test == 4:
                self.comment_relevance = min(self.relevance_score,4)
            elif result_many_test == 2:
                self.comment_relevance = min(self.relevance_score,3)
            elif result_many_test == 3:
                self.comment_relevance = min(self.relevance_score,2)
            elif result_many_test == 5:
                self.comment_relevance = min(self.relevance_score,1)

            print(f'***Inside of Viewport Relevance  = {self.comment_relevance}')
        elif self.user_location == 2:
            result_many_test2 = int(input('----Is the location in or out of the viewport? \n\n1. In \n2. Out '))
            if result_many_test2 == 1:
                self.comment_relevance = min(self.relevance_score,4)
            else:
                self.comment_relevance = min(self.relevance_score,1)
            
            print(f'***Outside of Viewport Relevance  = {self.comment_relevance}')
        else:
            self.distance()

    
    def few_possible_results(self) -> None:
        '''Fewer number of locations'''
        self.relevance_type = 'Few possible options'
        print(f'***Relevance Type  = {self.relevance_type}')
        self.distance()

    def lenient_distance(self) -> None:
        print(f'***Relevance Type  = {self.relevance_type}')
        self.distance()

        if self.comment_relevance == 1:
            self.comment_relevance = 2

        print(f'***{self.relevance_type} Relevance  = {self.comment_relevance}')
    
    def FPR_great_distances(self) -> None:
        '''Fewer number of locations at great distances'''
        self.relevance_type = 'FPO at Great distances'
        self.lenient_distance()

    def rural(self) -> None:

        self.relevance_type = 'Rural'
        self.lenient_distance()

    def location_user_deviations(self) -> None:
        '''Results where the locations are all over the place'''
        self.relevance_type = 'Deviations'
        print(f'***Relevance Type  = {self.relevance_type}')

        if self.navigational:
            pass
        else:
            result_deviation_test = int(input('----Is the location in the viewport, and near the user? \n\n1. Yes \n2. No '))
            if result_deviation_test == 1:
                self.comment_relevance = 4
            else:
                self.comment_relevance = 1
        
        print(f'***Deviation Relevance  = {self.comment_relevance}')

    def other_types(self) -> None:
        self.relevance_type = 'String Relevance'
        print(f'***Relevance Type  = {self.relevance_type}')
        self.comment_relevance = int(input('----Write score based on relationship between query and result'))

        print(f'***String Relevance  = {self.comment_relevance}')

    def relevance_tests(self) -> None:
        self.prominence()
        
        relevance_method = int(input('----Choose Method \n\n1. Many Resuslts \n2. Few Results(FPR) \n3. FPR and Further \n4. Rural \n5. Deviations in Location \n6. String Issues '))

        if relevance_method == 1:
            self.many_possible_results()
        elif relevance_method == 2:
            self.few_possible_results()
        elif relevance_method == 3:
            self.FPR_great_distances()
        elif relevance_method == 4:
            self.rural()
        elif relevance_method == 5:
            self.location_user_deviations()
        elif relevance_method == 6:
            self.other_types()

    def evaluate_relevance(self) -> None:
        self.no_other_options()
        self.is_legal()
        self.query_result_connection()

        self.relevance_tests

    def check_name(self) -> None:
        name_result = int(input('----Rate the name \n\n1. Correct \n2. Partially Correct (Mispell, Service Mismatches, Missing/Unnecesary additions) \n3. Incorrect (Unrecognizable) \n4. Cant Verify'))
        if name_result==1:
            self.comment_name = 'Correct'
            self.name_score = 3
        elif name_result==2:
            self.comment_name = 'Partially Correct'
            self.name_score = 2
        elif name_result==2:
            self.comment_name = 'Incorrect'
            self.name_score = 1
        else:
            self.comment_name = 'Cant verify'
            self.name_score = 0

    def check_category(self) -> None:
        category_result = int(input('----Is the category wrong, misleading, misspelled, incomplete or different language? \n\n1. Yes \n2. No \n3. n/a'))
        if category_result==1:
            self.comment_category = 'Incorrect'
            self.category_score = 1
        elif category_result==2:
            self.comment_category = 'Correct'
            self.category_score = 3
        else:
            self.comment_category = 'n/a'
            self.category_score = -1
        
        print(f'***Category Ranking  = {self.category_score}')

    def check_combined(self) -> None:
        cs = self.category_score
        ns = self.name_score
        
        if cs == 1 | ns == 1:
            self.name_category_score = 1
        elif (ns == 3 & cs == 3) | (ns == 3 & cs == -1):
            self.name_category_score = 3
        elif (ns == 2 & cs == 3) | (ns == 2 & cs == -1):
            self.name_category_score = 2
        else:
            self.name_category_score = int(input(f'----Name = {ns}, Category = {cs}. What is the score then?'))

        self.comment_name_category = self.Accuracy_levels[self.name_category_score]

        print(f'***Name and Category Ranking  = {self.comment_name_category}')

    def evaluate_name(self) -> None:
        if self.comment_query_type == 'Address':
            self.name_score = -1
        else:
            self.check_name
        
        print(f'***Name Ranking  = {self.name_score}')

        self.check_category()
        self.check_combined()

    def address_components(self) -> None:
        self.comment_components = []
        selection = int(input('----Check for the following address components \n\n1. Street #/Extensions/Ranges \n2. Unit/Apt \n3. St. Name/Alternate/Directions/Type \n4. Sub-locality \n5. Reggion/State \n6. Postal Code \n7. Country \n8. Exit'))
        while selection != 8:
            self.comment_components.append(selection)
            selection = int(input('----Check for the following address components \n\n1. Street #/Extensions/Ranges \n2. Unit/Apt \n3. St. Name/Alternate/Directions/Type \n4. Sub-locality \n5. Reggion/State \n6. Postal Code \n7. Country \n8. Exit'))
        
        if not selection:
            self.address_score = 3
        else:
            self.address_score = 1

        print(f'***Address Score  = {self.address_score} since there are issues with {self.comment_components}')

    def address_exists(self) -> None:
        if self.comment_query_type == 'Address':
            exists_test = int(input('----Does the address exist? \n\n1. Yes \n2. No'))
            if exists_test == 2:
                self.comment_adress_exist = False
                self.address_score = 1
                self.comment_adress = 'Address does not exist'
                print(f'***Address Score  = {self.address_score} since {self.comment_adress}')

            else:
                self.comment_adress_exist = True

    def other_address_issues(self) -> None:
        self.address_exists()
        other_address_test = int(input('----Any other issues with the address? \n\n1. Correct with formating \n2. Cant verify \n3. No'))
        if other_address_test ==1:
            self.address_score = -2
            self.comment_adress = 'Correct with formating'
            print(f'***Address Score  = {self.comment_adress}')
        elif other_address_test ==2:
            self.address_score = 0
            self.comment_adress = 'Cant Verify'
            print(f'***Address Score  = {self.comment_adress}')

    def evaluate_address(self) -> None:
        self.address_components()
        self.other_address_issues()

    def missing_pin(self) -> None:
        missing_pin_result = int(input('----Is the pin missing? \n\n1. Yes \n2. No '))
        if missing_pin_result == 1:
            self.pin_score = 1
            self.comment_pin = 'Pin missing'
            print(f'***Pin Score  = {self.pin_score} since {self.comment_pin}')

    def simple_roof(self) -> None:
        single_roof_result = int(input('----Where the pin is bitch? \n\n1. Perfect (Pin on roof) \n2. Approximate (Pin within boundaries) \n3. Next Door (Next to boundaries but not on the other side of the st.) \n4. Wrong (Anything else) \n5. Cant Verify (Blocked but within expected area) '))
        if single_roof_result ==1:
            self.pin_score = 4
            self.comment_pin = 'Perfect'
        elif single_roof_result ==2:
            self.pin_score = 3
            self.comment_pin = 'Approximate'
        elif single_roof_result ==3:
            self.pin_score = 2
            self.comment_pin = 'Next Door'
        elif single_roof_result ==4:
            self.pin_score = 1
            self.comment_pin = 'Wrong'
        else:
            self.pin_score = 0
            self.comment_pin = 'Cant Verify'

        print(f'***Pin Score  = {self.pin_score} since {self.comment_pin}')
    
    def single_roof(self) -> None:
        self.simple_roof()

    def complex_roof(self) -> None:
        multiple_roof_result2 = int(input('----Is the pin within the boundaries? \n\n1. Yes \n2. No \n3. n/a'))
        if multiple_roof_result2 ==1:
            self.pin_score = 4
            self.comment_pin = 'Perfect'
        elif multiple_roof_result2 ==2:
            self.pin_score = 1
            self.comment_pin = 'Wrong'
        elif multiple_roof_result2 ==3:
            self.pin_score = 0
            self.comment_pin = 'Cant Verify'

        print(f'***Pin Score  = {self.pin_score} since {self.comment_pin}')

    def multiple_roof(self) -> None:
        multiple_roof_result = int(input('----Is it a complex or multiple roofs? \n\n1. Complex (Universities, Shopping Malls, etc) \n2. Multiple Roofs (Multiple Buildings) '))
        if multiple_roof_result ==1:
            self.complex_roof()
        elif multiple_roof_result ==2:
            self.simple_roof()

    def natural_feature(self) -> None:
        natural_feature_result = int(input('----Where the pin is bitch? \n\n1. Perfect (Pin on roof) \n2. Approximate (Pin within boundaries) \n3. Wrong (Anything else) \n4. Cant Verify (Blocked but within expected area) '))
        if natural_feature_result ==1:
            self.pin_score = 4
            self.comment_pin = 'Perfect'
        elif natural_feature_result ==2:
            self.pin_score = 3
            self.comment_pin = 'Approximate'
        elif natural_feature_result ==3:
            self.pin_score = 1
            self.comment_pin = 'Wrong'
        else:
            self.pin_score = 0
            self.comment_pin = 'Cant Verify'

        print(f'***Pin Score  = {self.pin_score} since {self.comment_pin}')

    def no_roof(self) -> None:
        no_roof_result = int(input('----What is it? \n\n1. Streets/Administrative Divisions(Countries or Neighborhoods) \n2. Natural Features '))
        if no_roof_result ==1:
            self.complex_roof()
        elif no_roof_result ==2:
            self.natural_feature()

    def transit_POI(self) -> None:
        transit_result = int(input('----Where the pin is bitch? \n\n1. Perfect (Area you wait for transit) \n2. Approximate (Within 50m) \n3. Wrong (Anything else) \n4. Cant Verify (Blocked but within expected area) '))
        if transit_result ==1:
            self.pin_score = 4
            self.comment_pin = 'Perfect'
        elif transit_result ==2:
            self.pin_score = 3
            self.comment_pin = 'Approximate'
        elif transit_result ==3:
            self.pin_score = 1
            self.comment_pin = 'Wrong'
        else:
            self.pin_score = 0
            self.comment_pin = 'Cant Verify'

        print(f'***Pin Score  = {self.pin_score} since {self.comment_pin}')

    def evaluate_pin(self) -> None:
        self.missing_pin()
        pin_method = int(input('----Choose Method \n\n1. Single Roof \n2. Multiple Roof \n3. Natural Features \n4. No roof \n5. Transit POI '))

        if pin_method == 1:
            self.single_roof()
        elif pin_method == 2:
            self.multiple_roof()
        elif pin_method == 3:
            self.natural_feature()
        elif pin_method == 4:
            self.no_roof()
        elif pin_method == 5:
            self.transit_POI()

    def create_demoted_history(self) -> None:
        history = pd.DataFrame()
        history['Demoted_Score'] = self.demoted_scores
        history['Scores'] = self.resulting_scores
        history['Comments'] = self.demotion_reason
        self.demoted_history = history

    def create_final_comment(self) -> None:
        print('----Set-up')
        print(f'Location Intent  = {self.comment_location_intent}')
        print(f'Query Type  = {self.comment_query_type}')
        print(f'Navigational  = {self.comment_navigation}')
        print(f'Language Isues  = {self.comment_language}')
        print(f'Closed  = {self.comment_closure}')
        
        print('----Relevance + Reasons')
        print(f'Other Options  = {self.comment_options}')
        print(f'Legal?  = {self.comment_legal}')
        print(f'Connections  = {self.comment_connection}')
        print(f'Prominence  = {self.comment_prominence}')

        print(f'Relevance Type  = {self.relevance_type}')
        print(f'Relevance  = {self.comment_relevance}')

        print('----Name Accuracy + Reasons')
        print(f'Name  = {self.comment_name}')
        print(f'Name Score  = {self.name_score}')

        print(f'Category  = {self.comment_category}')
        print(f'Category Score  = {self.category_score}')

        print(f'Combined = {self.comment_name_category}')
        print(f'Combined Score  = {self.name_category_score}')

        print('----Address Accuracy + Reasons')
        print(f'Address = {self.comment_adress}')
        print(f'Address Components  = {self.comment_components}')
        print(f'Address Score = {self.address_score}')

        print('----Pin Accuracy + Reasons')
        print(f'Pin = {self.comment_pin}')
        print(f'Pin Score  = {self.pin_score}')

        print('----History')
        print(self.demoted_history)


def main() -> None:
     Survey = Mapping
     Survey.user_intent()
     Survey.navigational()
     Survey.result_level_issues()
     Survey.evaluate_relevance()
     Survey.evaluate_name()
     Survey.evaluate_address()
     Survey.evaluate_pin()
     Survey.create_demoted_history()
     Survey.create_final_comment()

     return Survey

if __name__ == '__main__':
    Data = main()
        