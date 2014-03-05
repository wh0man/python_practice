"""
Return Code:
    0. Successful
    1. The provided URL does not exist (could be caused by inputting wrong state name)

On default this will generate a CSV file in module's directory called output.csv
"""

import urllib2
import json
import csv


#Global Values
g_states = [
"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
"HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
"MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
"NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
"SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

#Read the file from HTTP and check if the URL was valid
def getJson(state):
    url = "http://api.sba.gov/geodata/city_county_links_for_state_of/" + state + ".json"
    try:
        return urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return None


def createDatabase():
    data_by_state = {}
    for state in g_states:
        file = getJson(state)

        #Validate the JSON txt file
        if (file == None):
            print "URL for state \"" + state + "\" was not found"
            continue

        #Store all the info in a dictionary
        data = json.loads(file)
        data_by_state[state] = data

    return data_by_state



def generateFile(outputPath = "output.csv"):
    output_file = open(outputPath, "wb")
    csvFile = csv.writer(output_file, delimiter=",", )
    data_by_state = createDatabase()


    #Print header
    header = []
    for headerInfo in data_by_state[g_states[0]][0]:
        header.append(headerInfo)
    csvFile.writerow(header)


    #just to ensure that text file is in order we will use g_state to iterate through the dictionary
    for state in g_states:
        #iterate through all the counties in each state
        print state
        for county_info in data_by_state[state]:
            tempArray = []
            for key in county_info:
                #If the value is none then don't encode
                if (county_info[key] == None):
                    tempArray.append(None)
                else:
                    tempArray.append(county_info[key].encode("utf-8"))

            csvFile.writerow(tempArray)

    output_file.close()




if __name__ == "__main__":
    generateFile()



