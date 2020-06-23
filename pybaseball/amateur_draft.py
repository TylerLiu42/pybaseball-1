import pandas as pd
import requests

pitcher_stat_columns = ['WAR', 'G.1', 'W', 'L', 'ERA', 'WHIP', 'SV']
batter_stat_columns = ['WAR', 'G', 'AB', 'HR', 'BA', 'OPS']

def get_draft_results(year, round): 
    url = f"https://www.baseball-reference.com/draft/?year_ID={year}&draft_round={round}&draft_type=junreg&query_type=year_round&"
    res = requests.get(url, timeout=None).content 
    draft_results = pd.read_html(res)
    return draft_results

def amateur_draft(year, round):
    draft_results = get_draft_results(year, round)
    draft_results = pd.concat(draft_results)
    draft_results = postprocess(draft_results)
    return draft_results

def amateur_draft_stats(year, round):
    draft_results = get_draft_results(year, round)
    draft_results = pd.concat(draft_results)
    draftee_stats = output_major_league_stats(draft_results)
    return draftee_stats

def output_major_league_stats(draft_results):
    pitchers = draft_results.loc[(pd.notna(draft_results['ERA']))] 
    batters = draft_results.loc[pd.notna(draft_results['AB'])]
    pitcher_stats = postprocess_stats(pitchers, "Pitcher")
    batter_stats = postprocess_stats(batters, "Batter")
    return (pitcher_stats, batter_stats)

def postprocess(draft_results):
    draft_results = remove_name_suffix(draft_results)
    draft_results.drop(['Year', 'Rnd', 'RdPck', 'DT', 'FrRnd', 'WAR', 'G', 'AB', 'HR', 'BA', 'OPS', 'G.1', 'W', 'L', 'ERA', 'WHIP', 'SV'], axis=1, inplace=True)
    return draft_results

def postprocess_stats(draft_results, player_type):
    draft_results = remove_name_suffix(draft_results)
    columns_to_keep = ['Name']
    columns_to_keep.extend(pitcher_stat_columns) if player_type == "Pitcher" else columns_to_keep.extend(batter_stat_columns)
    draft_results = draft_results[columns_to_keep]
    if (player_type == "Pitcher"):
        draft_results.rename({'G.1': 'G'}, axis=1, inplace=True)
    return draft_results

def remove_name_suffix(draft_results):
    draft_results = draft_results.copy()
    draft_results.loc[:,'Name'] = draft_results['Name'].apply(remove_minors_link)
    return draft_results

def remove_minors_link(draftee):
    return draftee.split('(')[0]
