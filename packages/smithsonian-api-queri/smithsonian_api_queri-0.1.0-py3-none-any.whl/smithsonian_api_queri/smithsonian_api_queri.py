def create_smithsonian_csv(category):
    """
    Query data from the Smithsonian Open Access API using category filters provided by user input.

    Parameters
    ----------
    Enter string input. 
      create_smithsonian_csv("userinput")

    Returns
    -------
    userinput_smithsonian_data.csv
      Function will return a .csv file with Smithsonian data that matches the specified search parameter.
    
    Examples
    --------
    >>> from smithsonian_api_queri import smithsonian_api_queri
    >>> create_smithsonian_csv("postmodernism")
    200
    Querying database...
    Querying database...
    Querying database...
    Querying database...
    Querying database...
    Querying database...
    Querying database...
    Querying database...
    Querying database...
    Querying database...
    File finished.
    """
    
    assert isinstance(category, str), "Search query must be entered as a string."
    base = "https://api.si.edu/openaccess/api/v1.0/search?"
    start = "start=1&"
    size_of_array = 1000
    row = "rows=" + str(size_of_array) + "&"
    api_url = base + start + row + "q=" + category + "&" + api_key
    api_response = requests.get(api_url)
    smithsonian_metadata = json.loads(api_response.text)
    print(api_response.status_code)
    with open("%s_smithsonian_data.csv" % category, "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["id",
                             "title",
                             "object_type",
                             "physicalDescription",
                             "date",
                             "data_source",
                             "record_link"])
        for line in range(1, 10000, size_of_array):
            time.sleep(5)
            start = f"start={line}" + "&"
            api_url = base + start + row + "q=" + category + "&" + api_key
            api_response = requests.get(api_url)
            smithsonian_metadata = json.loads(api_response.text)
            print("Querying database...")
            if smithsonian_metadata["response"].get("rows") is not None:
                for artwork in smithsonian_metadata["response"]["rows"]:
                    physical_description =  artwork["content"]["freetext"].get("physicalDescription", None)
                    smithsonian_data_row = [
                        artwork.get("id", None),
                        artwork.get("title", None),
                        ", ".join(artwork["content"]["indexedStructured"].get("object_type", [])),
                        physical_description[0].get("content") if physical_description is not None else "",
                        ", ".join(artwork["content"]["indexedStructured"].get("date", [])),
                        artwork["content"]["descriptiveNonRepeating"].get("data_source", []),
                        artwork["content"]["descriptiveNonRepeating"].get("record_link", None)
                    ]
                    csv_writer.writerow(smithsonian_data_row)
        print("File finished.")
