import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import plotly.express as px

def format_k(x, pos):
    return f'{int(x / 1000)}k'

def main():
    # US PRESIDENTIAL ELECTION 2016
    election_data  = pd.read_csv("./datasets/election-dataset.tab", sep='\t', on_bad_lines='skip')
    presidential_2016 = election_data[
        (election_data['year'] == 2016) & 
        (election_data['office'] == 'US PRESIDENT')
    ].groupby(['state_fips', 'party_simplified']).agg({
        'candidatevotes': 'sum'
    }).reset_index()
    
    # Pivot to get Democrat and Republican columns
    pivot_data = presidential_2016.pivot_table(
        index=['state_fips'], 
        columns='party_simplified', 
        values='candidatevotes', 
        fill_value=0
    ).reset_index()

    # Create FIPS column to match your data
    pivot_data['fips'] = pivot_data['state_fips'].astype(str).str.zfill(2)

    # Create state abbreviations mapping (you'll need to add this to your data)
    state_mapping = {
        '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA', '08': 'CO',
        '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL', '13': 'GA', '15': 'HI',
        '16': 'ID', '17': 'IL', '18': 'IN', '19': 'IA', '20': 'KS', '21': 'KY',
        '22': 'LA', '23': 'ME', '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN',
        '28': 'MS', '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH',
        '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND', '39': 'OH',
        '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI', '45': 'SC', '46': 'SD',
        '47': 'TN', '48': 'TX', '49': 'UT', '50': 'VT', '51': 'VA', '53': 'WA',
        '54': 'WV', '55': 'WI', '56': 'WY'
    }

    pivot_data['state_abbr'] = pivot_data['fips'].map(state_mapping)

    if 'DEMOCRAT' in pivot_data.columns and 'REPUBLICAN' in pivot_data.columns:
        pivot_data['total_votes'] = pivot_data['DEMOCRAT'] + pivot_data['REPUBLICAN']
        pivot_data['dem_percentage'] = (pivot_data['DEMOCRAT'] / pivot_data['total_votes']) * 100
        pivot_data['rep_percentage'] = (pivot_data['REPUBLICAN'] / pivot_data['total_votes']) * 100
        pivot_data['margin'] = pivot_data['rep_percentage'] - pivot_data['dem_percentage']
    elif 'democratic' in pivot_data.columns and 'republican' in pivot_data.columns:
        pivot_data['total_votes'] = pivot_data['democratic'] + pivot_data['republican']
        pivot_data['dem_percentage'] = (pivot_data['democratic'] / pivot_data['total_votes']) * 100
        pivot_data['rep_percentage'] = (pivot_data['republican'] / pivot_data['total_votes']) * 100
        pivot_data['margin'] = pivot_data['rep_percentage'] - pivot_data['dem_percentage']
    else:
        print("Column names are different. Available party columns:")
        print([col for col in pivot_data.columns if col not in ['state_fips', 'fips']])

    print(pivot_data)
    fig = px.choropleth(pivot_data, 
                    locations='state_abbr',
                    color='margin',
                    color_continuous_scale='RdBu_r',
                    range_color=[-50, 50],
                    locationmode='USA-states',
                    hover_data=['state_abbr', 'total_votes'],
                    title='2016 Presidential Election Results by State')

    fig.update_layout(geo_scope="usa")
    fig.show()

    # SALARY 
    salaries = pd.read_csv("./datasets/salary-dataset.csv")
    jobs = {}
    counter = {}

    for _, row in salaries.iterrows():
        job_title = row["job_title"]
        salary = row["salary"]

        counter[job_title] = counter.get(job_title, 0) + 1

        jobs[job_title] = jobs.get(job_title, 0) + salary
    
    for key in jobs.keys():
        jobs[key] = jobs.get(key) / counter[key]

    x = []
    y = []

    for job in jobs.keys():
        x.append(job)
        y.append(jobs.get(job))

    x = np.array(x)
    y = np.array(y)

    plt.figure(figsize=(10, 5))
    plt.bar(x, y)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_k))
    plt.title('Most Payed Job Salaries per Year')
    plt.xlabel('Jobs')
    plt.ylabel('Salaries')
    plt.savefig('./exports/salaries.png')
    plt.show()


if __name__ == "__main__":
    main()