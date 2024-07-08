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

    Query_types = {
        1: 'Address',
        2: 'Point of Interest',
        3: 'Business',
        4: 'Category',
        5: 'Products and Service',
        6: 'Coordinates or My location',
        7: 'Emoji',
        8: 'No map Intent',
    }

    history = []







    def __init__(self) -> None:
        '''These values represent the best rating
        for each category, which might be demoted later on'''

        self.relevance_score = 5
        self.name_score = 3
        self.category_score = 3
        self.address_score = 3
        self.pin_score = 4

    def save_comments(self, left_side:str, self_comment:str, reason:str) -> None:
        present_results = left_side+' : '+self_comment+' because '+reason
        self.history.append(present_results)

        print('******'+present_results)

    def infinite_blank_check(self, loc_intents:list[str], self_iter, left_side:str, reason:str) -> str:
        '''In-Progress'''
        rep = len(loc_intents) + 1
        lap = 1

        while lap != rep:
            if self_iter == lap:
                self_comment = loc_intents[lap-1]
            lap += 1

        self.save_comments(left_side, self_comment, reason)
        
        return self_comment







    def fresh_viewport(self, left_side:str, reason:str) -> None:
        str_list = ['User Location',
                    'Viewport > User Location',
                    'Viewport']
        
        self.comment_location_intent = self.infinite_blank_check(str_list, self.user_location, left_side, reason)


    def stale_viewport(self, left_side:str, reason:str) -> None:
        str_list = ['User Location',
                    'User Location',
                    'Stale Viewport']
        
        self.comment_location_intent = self.infinite_blank_check(str_list, self.user_location, left_side, reason)


    def missing_viewport(self, left_side:str, reason:str) -> None:
        str_list = ['User Location',
                    'Test Locale']
        
        self.comment_location_intent = self.infinite_blank_check(str_list, self.user_location, left_side, reason)


    def explicit_location(self, left_side:str) -> None:
        self.explicit_intent = int(input('\n----Select Explicit Intent \n\n1. Specific Location, \n2. Near me \n\nAnswer:     '))
        reason = ['Specific Location',
                  'Near me']

        str_list = ['Ignore User and Viewpoint Location',
                    'User Location']
        
        self.comment_location_intent = self.infinite_blank_check(str_list, self.explicit_intent, left_side, reason[self.explicit_intent-1]+' Query')


    def implicit_location(self) -> None:
        self.viewport_type = int(input('\n----Select Viewport type \n\n1. Fresh, \n2. Stale, \n3. Age Missing, \n4. Missing \n\nAnswer:     '))
        viewport_type = ['Fresh', 
                         'Stale', 
                         'Age Missing', 
                         'Missing']
        
        left_side = f'{viewport_type[self.viewport_type]}' + ' Viewpoint - Location Intent'

        if self.viewport_type < 3:
            self.user_location = int(input('\n----Select User Location \n\n1. Inside Viewport, \n2. Outside Viewport, \n3. Missing \n\nAnswer:     '))
            reason = ['Inside Viewport',
                      'Outside Viewport',
                      'Missing']

            if self.viewport_type == 1:
                self.fresh_viewport(left_side, reason[self.user_location-1])
            elif self.viewport_type == 2:
                self.stale_viewport(left_side, reason[self.user_location-1])

        else:
            self.user_location = int(input('\n----Select User Location \n\n1. Present, \n2. Missing \n\nAnswer:     '))
            reason = ['Present',
                      'Missing']

            if self.viewport_type == 3:
                self.fresh_viewport(left_side, reason[self.user_location-1])
            elif self.viewport_type == 4:
                self.missing_viewport(left_side, reason[self.user_location-1])


    def get_query_type(self) -> None:
        self.query_type = int(input('\n----Select Queary Type \n\n1. Address(street number, street name, locality, state, country, and postal code), \n2. Point of Interest(POI), \n3. Business, \n4. Category, \n5. Products and Service, \n6. Coordinates or My location, \n7. Emoji, \n8. No map Intent \n\nAnswer:     '))
        self.comment_query_type = self.Query_types[self.query_type]
        reason = 'N/A'
        self.save_comments('Query Type', self.comment_query_type, reason)


    def get_location_intent(self) -> None:
        self.location_type = int(input('\n----Select Location Intent \n\n1. Explicit (Specific), \n2. Implicit (Not Specific) \n\nAnswer:     '))
        
        if self.location_type == 2:
            self.implicit_location()

        elif self.location_type == 1:
            left_side = 'Viewpoint - Location Intent'
            self.explicit_location(left_side)


    def user_intent(self) -> None:
        '''Describe User intent by specifing Query Type and Location Intent
        Results in: 
        
        ---self.comment_query_type---,
        ---self.comment_location_intent---'''
        self.get_query_type()
        self.get_location_intent()







    boolean = ['n/a', True, False]
    def navigational(self) -> None:
        self.comment_navigation  = self.boolean[int(input('\n----Is this a Navigational Intent? \nThe intent is unique and clear enough that there is only a single result in the world \n\n1. Yes \n2. No \n\nAnswer:     '))]
        reason = 'The intent is unique and clear enough that there is only a single result in the world'
        if self.comment_navigation  == False:
            self.relevance_score = 4
            reason = 'The intent is NOT unique and clear enough that there is only a single result in the world'

        self.save_comments('Navigational', str(self.comment_navigation), reason)


    def language_test(self) -> None:
        self.comment_language = self.boolean[int(input('\n----Is the language matching for test_locale, query, and result region? \n\n1. Yes \n2. No \n\nAnswer:     '))]
        reason = 'N/A'
        if self.comment_language == False:
            self.address_score = 1

        self.save_comments('Language Match', str(self.comment_language), reason)


    def closure_test(self) -> None:
        self.comment_closure = self.boolean[int(input('\n----Is the status PERMANENT_CLOSURE? \n\n1. Yes \n2. No \n\nAnswer:     '))]
        if self.comment_closure:
            exp = self.boolean[int(input('\n----Is this result Expected? \nIt completely satisfies user intent or there are no other options? \n\n1. Yes \n2. No \n\nAnswer:     '))]
            if exp == False:
                self.relevance_score = 2
                left_side = 'Unexpected PERMANENT_CLOSURE'
                reason = 'It does not satisfies user intent or there are no other options'
            else:
                left_side = 'Expected PERMANENT_CLOSURE'
                reason = 'It completely satisfies user intent or there are no other options'

            self.save_comments(left_side, str(self.comment_closure), reason)


    def all_level_issues(self) -> None:
        '''Check for issues related to Query or the Results
        Results in: 

        ---self.comment_navigation---, 
        ---self.comment_language---, 
        ---self.comment_closure---'''
        # Query
        self.navigational()

        # Result
        self.language_test()
        self.closure_test()







    
    def no_other_options(self) -> None:
        self.comment_options = self.boolean[int(input('\n----Are there any better results not shown? \n\n1. Yes \n2. No \n\nAnswer:     '))]
        reason = 'N/A'
        if self.comment_options:
            demotion_req = self.boolean[int(input('\n----Does it require demotion? \n\n1. Yes \n2. No \n\nAnswer:     '))]
            if demotion_req:
                amount = input('\n----How many points? \n\nAnswer:     ')
                reason = f'There are missing options that fit the query better, relevance demoted {amount} points'
                self.relevance_score = self.relevance_score - amount

        left_side = 'Other Options'
        self.save_comments(left_side, str(self.comment_options), reason)


    def is_legal(self) -> None:
        self.comment_legal = self.boolean[int(input('\n----Is it unexpectedly inappropriate? \n\n1. Yes \n2. No \n\nAnswer:     '))]
        reason ='N/A'
        if self.comment_legal:
            self.relevance_score = 1
        
        left_side = 'Inappropriate results'
        self.save_comments(left_side, str(self.comment_legal), reason)


    def query_result_connection(self) -> None:
        result_connection_test_p1 = int(input('\n----Does the connection satisfy intent? \nGeneral, Abbreviation/Alternate, Category, Spell Correction \nTransit, Special Character, Address? \n\n1. Yes \n2. No \n\nAnswer:     '))
        conections = ['', 
                      'Address',
                      'Not Address']
        left_side = 'Query Connections'
        reason = 'N/A'

        if result_connection_test_p1 == 1:
            result_connection_test_p2 = int(input('\n----Is it address? \n\n1. Yes \n2. No \n\nAnswer:     '))
            left_side = conections[result_connection_test_p2-1] + ' ' + left_side
            
            if result_connection_test_p2 == 1:
                result_connection_test_p3 = int(input('\n----What is missing? \n\n1. Unit Number \n2. Incomplete \n3. Wrong \n4. None \n\nAnswer:     '))
                str_list = ['Unit Number', 
                            'Incomplete', 
                            'Wrong', 
                            'All good']
                
                scores = [3,
                          2,
                          1,
                          self.relevance_score]
                
                self.relevance_score = scores[result_connection_test_p3-1]
                reason = f'of this the Current/Final Relevant Score is {self.Relevance_levels[self.relevance_score]}'
                self.comment_connection = self.infinite_blank_check(str_list, result_connection_test_p3, left_side, reason)

            else:
                self.comment_connection = 'Not Address'
                reason = 'General, Abbreviation/Alternate, Category, Spell Correction, Transit, or Special Character'
                self.save_comments(left_side, self.comment_connection, reason)

        else:
            self.comment_connection = 'Not satisfied'
            self.relevance_score = 1

            self.save_comments(left_side, self.comment_connection, reason)


    def prominence(self) -> None:
        result_prominence_test = int(input('\n----Should there be a promotion due to interantional prominence? \n\n1. Yes \n2. No \n\nAnswer:     '))
        if result_prominence_test == 1:
            self.comment_prominence = 'International'
            self.relevance_score = 3
        else:
            self.comment_prominence = 'No Promotion'

        left_side = 'Prominence Promotion'
        reason = 'N/A'
        self.save_comments(left_side, self.comment_prominence, reason)
    

    def distance(self) -> None:
        result_many_test3 = int(input('\n----How far is the location from viewport? \n\n1. Near \n2. Near-ish \n3. Far-ish \n4. Far \n\nAnswer:     '))
        str_list = ['Near', 
                    'Near-ish', 
                    'Far-ish', 
                    'Far']
        
        scores = [999, 
                  self.relevance_score, 
                  min(self.relevance_score,3), 
                  min(self.relevance_score,2), 
                  min(self.relevance_score,1)]
        
        left_side = f'{self.relevance_type} Relevance'
        self.relevance_score = scores[result_many_test3]
        reason = f'of this Relevance Score is {self.Relevance_levels[self.relevance_score]}'

        self.comment_relevance = self.infinite_blank_check(str_list, result_many_test3, left_side, reason)


    def many_possible_results(self) -> None:
        '''Many results that could satisfy the user'''

        self.relevance_type = 'Many possible options'
        if self.user_location == 1:
            result_many_test = int(input('\n----How far is the location from user? \n\n1. Near/In \n2. Near-ish/In \n3. Far/In \n4. Near/Out \n5. Far/Out \n\nAnswer:     '))
            str_list = ['Near/In', 
                        'Near-ish/In', 
                        'Far/In', 
                        'Near/Out', 
                        'Far/Out']
            
            scores = [999, 
                      self.relevance_score, 
                      min(self.relevance_score,3), 
                      min(self.relevance_score,2), 
                      self.relevance_score, 
                      min(self.relevance_score,1)]
            
            left_side = f'{self.relevance_type} Relevance'
            self.relevance_score = scores[result_many_test]
            reason = f'of this Relevance Score is {self.Relevance_levels[self.relevance_score]}'

            self.comment_relevance = self.infinite_blank_check(str_list, result_many_test, left_side, reason)

        elif self.user_location == 2:
            result_many_test2 = int(input('\n----Is the location in or out of the viewport? \n\n1. In \n2. Out \n\nAnswer:     '))
            str_list = [
                'In', 
                'Out']
            
            scores = [999,
                      self.relevance_score, 
                      min(self.relevance_score,1)]
            
            left_side = f'{self.relevance_type} Relevance'
            self.relevance_score = scores[result_many_test2]
            reason = f'of this Relevance Score is {self.Relevance_levels[self.relevance_score]}'

            self.comment_relevance = self.infinite_blank_check(str_list, result_many_test2, left_side, reason)

        else:
            self.distance()

    
    def few_possible_results(self) -> None:
        '''Fewer number of locations'''
        self.relevance_type = 'Few possible options'
        self.distance()


    def lenient_distance(self) -> None:
        self.distance()

        if self.relevance_score == 1:
            self.relevance_score = 2

        left_side = f'{self.relevance_type} Relevance'
        self.comment_relevance = self.Relevance_levels[self.relevance_score]
        self.save_comments(left_side, self.comment_relevance, 'Lenient diatance Intance')


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

        if self.navigational == False:
            result_deviation_test = int(input('\n----Is the location in the viewport, and near the user? \n\n1. Yes \n2. No \n\nAnswer:     '))
            if result_deviation_test == 1:
                reason = 'It is in the viewport, and near the user'
            else:
                self.relevance_score = 1
                reason = 'Not in the viewport, and near the user'
        
        left_side = f'{self.relevance_type} Relevance'
        self.comment_relevance = self.Relevance_levels[self.relevance_score]
        self.save_comments(left_side, self.comment_relevance, reason)

    def other_types(self) -> None:
        self.relevance_type = 'String Relevance'
        print(f'Current Relevance Score: {self.relevance_score}')
        self.relevance_score = int(input('\n----Write score based on relationship between query and result \n\nAnswer:     '))
        reason = input('----Provide reason')

        left_side = f'{self.relevance_type} Relevance'
        self.comment_relevance = self.Relevance_levels[self.relevance_score]
        self.save_comments(left_side, self.comment_relevance, reason)

    def relevance_tests(self) -> None:
        self.prominence()
        
        relevance_method = int(input('\n----Choose Method \n\n1. Many Resuslts \n2. Few Results(FPR) \n3. FPR and Further \n4. Rural \n5. Deviations in Location \n6. String Issues \n\nAnswer:     '))

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
        '''Check for issues related to Relevance and Evaluate Relvance

        Results in:
        ---self.comment_relevance---, 
        ---self.relevance_score---, 
        ---self.comment_prominence---, 
        ---self.comment_connection---,
        ---self.comment_legal---'''

        # Relevance Issues
        self.no_other_options()
        self.is_legal()
        self.query_result_connection()

        # Evaluate Relevance
        if self.comment_connection == 'Not Address':
            self.relevance_tests()







    def check_name(self) -> None:
        name_result = int(input('\n----Rate the name \n\n1. Correct \n2. Partially Correct (Mispell, Service Mismatches, Missing/Unnecesary additions) \n3. Incorrect (Unrecognizable) \n4. Cant Verify \n\nAnswer:     '))
        
        str_list = ['Correct', 
                    'Partially Correct', 
                    'Incorrect', 
                    'Cant Verify']
        
        scores = [999, 
                 3,
                 2,
                 1,
                 0]
        
        left_side = f'Name Rating'
        self.name_score = scores[name_result]
        reason = f'of this Name Score is {self.name_score}'
        
        self.comment_name = self.infinite_blank_check(str_list, name_result, left_side, reason)


    def check_category(self) -> None:
        category_result = int(input('\n----Is the category wrong, misleading, misspelled, incomplete or different language? \n\n1. Yes \n2. No \n3. n/a \n\nAnswer:     '))
        str_list = ['Incorrect', 
                    'Correct', 
                    'n/a']
        
        scores = [999, 
                 1,
                 3,
                 -1]
        
        left_side = f'Category Rating'
        self.category_score = scores[category_result]
        reason = f'of this Category Score is {self.category_score}'
        
        self.comment_category = self.infinite_blank_check(str_list, category_result, left_side, reason)


    def check_combined(self) -> None:
        cs = self.category_score
        ns = self.name_score
        
        if cs == 1 | ns == 1:
            self.name_category_score = 1
        elif (ns == 3 & cs == 3) | (ns == 3 & cs == -1):
            self.name_category_score = 3
        elif (ns == 2 & cs == 3) | (ns == 2 & cs == -1):
            self.name_category_score = 2
        elif (ns == 3 & cs == -1):
            self.name_category_score = -1
        else:
            self.name_category_score = int(input(f'\n----Name = {ns}, Category = {cs}. What is the score then? \n\nAnswer:     '))

        left_side = f'Combined Name-Category Rating'
        self.comment_name_category = self.Accuracy_levels[self.name_category_score]
        reason = f'of this Name-Category Score is {self.category_score}'

        self.save_comments(left_side, self.comment_name_category, reason)


    def evaluate_name(self) -> None:
        '''Check for Name, Category and Combined scores

        Results in:
        ---self.comment_name---, 
        ---self.comment_category---, 
        ---self.comment_name_category---'''

        if self.comment_query_type == 'Address':
            address_name = self.boolean[int(input('\n----Does the address result include a name? \n\n1. Yes \n2. No \n3. n/a \n\nAnswer:     '))]
            
            if address_name == False:
                self.name_score = -1

                left_side = f'Name Rating'
                reason = 'Query Type is Address'
                self.comment_name = self.Accuracy_levels[self.name_score]
                self.save_comments(left_side, self.comment_name, reason)
            else:
                self.check_name
        else:
            self.check_name

        self.check_category()
        self.check_combined()







    def address_components(self) -> None:
        self.comment_components = []
        selection = int(input('\n----Check for the following address components based on result address \n\n1. Street #/Extensions/Ranges \n2. Unit/Apt \n3. St. Name/Alternate/Directions/Type \n4. Sub-locality \n5. Reggion/State \n6. Postal Code \n7. Country \n8. Exit \n\nAnswer:     '))
        issues = ['Street #/Extensions/Ranges','Unit/Apt', 'St. Name/Alternate/Directions/Type' ,'Sub-locality' ,'Reggion/State' ,'Postal Code' ,'Country']
        while selection != 8:
            self.comment_components.append(issues[selection-1])
            selection = int(input('\n----Check for the following address components based on result address \n\n1. Street #/Extensions/Ranges \n2. Unit/Apt \n3. St. Name/Alternate/Directions/Type \n4. Sub-locality \n5. Reggion/State \n6. Postal Code \n7. Country \n8. Exit \n\nAnswer:     '))
        
        if not self.comment_components:
            self.address_score = 3
        else:
            self.address_score = 1

        left_side = f'Address Score'
        reason = f'there are issues with {self.comment_components}'
        self.comment_adress = self.Accuracy_levels[self.address_score]
        self.save_comments(left_side, self.comment_adress, reason)


    def address_exists(self) -> bool:
        test_result = False
        if self.comment_query_type == 'Address':
            self.comment_adress_exist = self.boolean[int(input('\n----Does the address exist? \n\n1. Yes \n2. No \n\nAnswer:     '))]
            if self.comment_adress_exist == False:
                self.address_score = 1
                self.comment_adress = 'Address does not exist'

                left_side = f'Address Score'
                reason = f'of this the Address Score in {self.address_score}'
                self.save_comments(left_side, self.comment_adress, reason)
                test_result = True

        return test_result


    def other_address_issues(self) -> None:
        other_address_test = int(input('\n----Any other issues with the address? \n\n1. Correct with formating \n2. Cant verify \n3. No \n\nAnswer:     '))
        str_list = ['', 
                    'Correct with formating', 
                    'Cant verify']
        
        scores = [999, 
                  -2, 
                  0]
        
        if other_address_test != 3:
            left_side = f'Other address issues'
            self.address_score = scores[other_address_test]
            reason = f'of this Address Score is {self.address_score}'
            
            self.comment_address = self.infinite_blank_check(str_list, other_address_test, left_side, reason)


    def evaluate_address(self) -> None:
        '''Check the Address

        Results in:
        ---self.comment_address ---, 
        ---self.comment_adress_exist---'''

        if self.address_exists() == False:
            self.address_components()
            self.other_address_issues()







    def missing_pin(self) -> bool:
        missing_pin_result = self.boolean[int(input('\n----Is the pin missing? \n\n1. Yes \n2. No \n\nAnswer:     '))]
        if missing_pin_result:
            self.pin_score = 1
            self.comment_pin = 'Pin missing'

            left_side = f'Missing Pin'
            reason = f'of this Pin Score is {self.pin_score}'
            self.save_comments(left_side, self.comment_pin, reason)

        return missing_pin_result
            

    def simple_roof(self) -> None:
        single_roof_result = int(input('\n----Where the pin is bitch? \n\n1. Perfect (Pin on roof) \n2. Approximate (Pin within boundaries) \n3. Next Door (Next to boundaries but not on the other side of the st.) \n4. Wrong (Anything else) \n5. Cant Verify (Blocked but within expected area) \n\nAnswer:     '))
        str_list = ['Perfect', 
                    'Approximate', 
                    'Next Door',
                    'Wrong',
                    'Cant Verify']
        
        scores = [999, 
                 4,
                 3,
                 2,
                 1,
                 0]
        
        left_side = f'Pin Score'
        self.pin_score = scores[single_roof_result]
        reason = f'of this Pin Score is {self.pin_score}'
        
        self.comment_pin = self.infinite_blank_check(str_list, single_roof_result, left_side, reason)

    
    def single_roof(self) -> None:
        self.simple_roof()

    def complex_roof(self) -> None:
        multiple_roof_result2 = int(input('\n----Is the pin within the boundaries? \n\n1. Yes \n2. No \n3. n/a \n\nAnswer:     '))
        str_list = ['Perfect',
                    'Wrong',
                    'Cant Verify']
        
        scores = [999, 
                 4,
                 1,
                 0]
        
        left_side = f'Pin Score'
        self.pin_score = scores[multiple_roof_result2]
        reason = f'of this Pin Score is {self.pin_score}'
        
        self.comment_pin = self.infinite_blank_check(str_list, multiple_roof_result2, left_side, reason)
        

    def multiple_roof(self) -> None:
        multiple_roof_result = int(input('\n----Is it a complex or multiple roofs? \n\n1. Complex (Universities, Shopping Malls, etc) \n2. Multiple Roofs (Multiple Buildings) \n\nAnswer:     '))
        if multiple_roof_result ==1:
            self.complex_roof()
        elif multiple_roof_result ==2:
            self.simple_roof()


    def natural_feature(self) -> None:
        natural_feature_result = int(input('\n----Where the pin is bitch? \n\n1. Perfect (Pin on roof) \n2. Approximate (Pin within boundaries) \n3. Wrong (Anything else) \n4. Cant Verify (Blocked but within expected area) \n\nAnswer:     '))
        str_list = ['Perfect',
                    'Approximate',
                    'Wrong',
                    'Cant Verify']
        
        scores = [999, 
                 4,
                 3,
                 1,
                 0]
        
        left_side = f'Pin Score'
        self.pin_score = scores[natural_feature_result]
        reason = f'of this Pin Score is {self.pin_score}'
        
        self.comment_pin = self.infinite_blank_check(str_list, natural_feature_result, left_side, reason)


    def no_roof(self) -> None:
        no_roof_result = int(input('----\nWhat is it? \n\n1. Streets/Administrative Divisions(Countries or Neighborhoods) \n2. Natural Features \n\nAnswer:     '))
        if no_roof_result ==1:
            self.complex_roof()
        elif no_roof_result ==2:
            self.natural_feature()


    def transit_POI(self) -> None:
        transit_result = int(input('----\nWhere the pin is bitch? \n\n1. Perfect (Area you wait for transit) \n2. Approximate (Within 50m) \n3. Wrong (Anything else) \n4. Cant Verify (Blocked but within expected area) \n\nAnswer:     '))
        str_list = ['Perfect',
                    'Approximate',
                    'Wrong',
                    'Cant Verify']
        
        scores = [999, 
                 4,
                 3,
                 1,
                 0]
        
        left_side = f'Pin Score'
        self.pin_score = scores[transit_result]
        reason = f'of this Pin Score is {self.pin_score}'
        
        self.comment_pin = self.infinite_blank_check(str_list, transit_result, left_side, reason)


    def evaluate_pin(self) -> None:
        if self.missing_pin() == False:
            pin_method = int(input('\n----Choose Method \n\n1. Single Roof \n2. Multiple Roof \n3. Natural Features \n4. No roof \n5. Transit POI \n\nAnswer:     '))

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

def print_report(comments) -> None:
    for item in comments:
        print(item)

def main() -> None:
    print('\nLegend\n------ Question \n****** Results \n')

    Survey = Mapping()

    Survey.history.append('-----Set-Up')
    Survey.user_intent()
    Survey.all_level_issues()
     
    Survey.history.append(' ')
    Survey.history.append('-----Relevance')
    Survey.evaluate_relevance()

    Survey.history.append(' ')
    Survey.history.append('-----Name-Category')
    Survey.evaluate_name()

    Survey.history.append(' ')
    Survey.history.append('-----Address')
    Survey.evaluate_address()

    Survey.history.append(' ')
    Survey.history.append('-----Pin')
    Survey.evaluate_pin()

    print('\n\n')
    print('REPORT SUMMARY')
    print_report(Survey.history)

    return Survey

if __name__ == '__main__':
    Survey = main()
        