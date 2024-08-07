import pandas as pd


def get_paginated_responses(df, rows_per_page, cols_per_page, page=1):
    """
    Takes dataframe along with the desired size to transform it to(int), auto 1 page
    Returns list[list[int]]: responses plus totals at the end of each row
    """
    count = 0
    transformed_data : list[list[int]] = [[] for _ in range(rows_per_page)]
    start_row = 0 
    end_row = rows_per_page
    paginated_df = df.iloc[start_row:end_row]
    all_responses = paginated_df.values.flatten()
    pulled = {}
    #Cut out bonus questions
    while(cols_per_page * rows_per_page != len(all_responses)):
        all_responses = all_responses[1:]
    #From list to matrix
    for _ in range(cols_per_page):
        for row in range(rows_per_page):
            transformed_data[row].append(all_responses[count])
            count += 1

    #Add the total of each row to the end
    for row in range(rows_per_page):
        total = 0
        for val in transformed_data[row]:
            total += int(val)
        transformed_data[row].append(total)


    #Add the 16 Gift Labels
    Gifts = {1:'Administration',2: 'Apostleship',3: 'Discernment',4: 'Evangelism',5: 'Exhortation',6: 'Faith',7: 'Giving',8: 'Hospitality',9: 'Knowledge',10: 'Leadership',11: 'Mercy',12: 'Prophecy',13: 'Shepherding',14: 'Helps/Service',15: 'Teaching',16: 'Wisdom'}
    for row in range(rows_per_page):
        transformed_data[row].insert(0,Gifts[row+1])

    #--pull the totals
    pulled = pull_totals(pulled,transformed_data )
    
    #Reorder Rows from biggest to smallest6
    data_copy = transformed_data.copy()
    sortedData = []

    for i in range(len(data_copy)):
        minValue = data_copy[0]
        for x in data_copy:
            if x[9] < minValue[9]:
                minValue = x
        sortedData.append(minValue)
        data_copy.remove(minValue)

    sortedList = sortedData[::-1]
    #--pull ranks
    pulled = pull_ranks(pulled, sortedData)
    
    return sortedList, page, pulled

def pull_totals(dic, lst):
    #pulls the totals to a dictionary to it can later be assigned back to the main df
    for val in lst:
        dic[val[0]] = val[-1]
    return dic

def pull_ranks(dic, lst):
    #the ranks to later be assigned
    for i,val in enumerate(lst):
        dic[f"Rank {i+1}"] = val[0]
    return dic

def generate_summary_html(data):
    # Generate HTML for the top three gifts
    top_three_html = """
    <h2>Your Top Three Spiritual Gifts</h2>
    <table class="summary-table">
        <thead>
            <tr>
                <th>Gift</th>
                <th>Much (3)</th>
                <th>Some (2)</th>
                <th>Little (1)</th>
                <th>None (0)</th>
            </tr>
        </thead>
        <tbody>
    """
    for row in data[:3]:
        gift_name = row[0]
        counts = {3: row[1:-1].count("3"), 2: row[1:-1].count("2"), 1: row[1:-1].count("1"), 0: row[1:-1].count("0")}
        top_three_html += f"""
        <tr>
            <td>{gift_name}</td>
            <td>{counts[3]}</td>
            <td>{counts[2]}</td>
            <td>{counts[1]}</td>
            <td>{counts[0]}</td>
        </tr>
        """
    top_three_html += "</tbody></table>"

    # Generate HTML for the full summary table
    summary_html = """
    <h2>Summary of All Spiritual Gifts</h2>
    <table class="summary-table">
        <thead>
            <tr>
                <th>Gift</th>
                <th>Much (3)</th>
                <th>Some (2)</th>
                <th>Little (1)</th>
                <th>None (0)</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
    """
    for row in data:
        gift_name = row[0]
        total = row[-1]
        counts = {3: row[1:-1].count("3"), 2: row[1:-1].count("2"), 1: row[1:-1].count("1"), 0: row[1:-1].count("0")}
        summary_html += f"""
        <tr>
            <td>{gift_name}</td>
            <td>{counts[3]}</td>
            <td>{counts[2]}</td>
            <td>{counts[1]}</td>
            <td>{counts[0]}</td>
            <td>{total}</td>
        </tr>
        """
    summary_html += "</tbody></table>"

    return top_three_html + summary_html
