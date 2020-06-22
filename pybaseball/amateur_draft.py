import pandas as pd
import requests

pitcherStatColumns = ['WAR', 'G.1', 'W', 'L', 'ERA', 'WHIP', 'SV']
batterStatColumns = ['WAR', 'G', 'AB', 'HR', 'BA', 'OPS']

def getDraftResults(year, round): 
    url = f"https://www.baseball-reference.com/draft/?year_ID={year}&draft_round={round}&draft_type=junreg&query_type=year_round&"
    res = requests.get(url, timeout=None).content 
    draftResults = pd.read_html(res)
    return draftResults

def amateur_draft(year, round):
    draftResults = getDraftResults(year, round)
    draftResults = pd.concat(draftResults)
    draftResults = postprocess(draftResults)
    return draftResults

def amateur_draft_stats(year, round):
    draftResults = getDraftResults(year, round)
    draftResults = pd.concat(draftResults)
    drafteeStats = outputMajorLeagueStats(draftResults)
    return drafteeStats

def outputMajorLeagueStats(draftResults):
    pitchers = draftResults.loc[(pd.notna(draftResults['ERA']))] 
    batters = draftResults.loc[pd.notna(draftResults['AB'])]
    pitcherStats = postprocessStats(pitchers, "Pitcher")
    batterStats = postprocessStats(batters, "Batter")
    return (pitcherStats, batterStats)

def postprocess(draftResults):
    draftResults = removeNameSuffix(draftResults)
    draftResults.drop(['Year', 'Rnd', 'RdPck', 'DT', 'FrRnd', 'WAR', 'G', 'AB', 'HR', 'BA', 'OPS', 'G.1', 'W', 'L', 'ERA', 'WHIP', 'SV'], axis=1, inplace=True)
    return draftResults

def postprocessStats(draftResults, playerType):
    draftResults = removeNameSuffix(draftResults)
    columnsToKeep = ['Name']
    columnsToKeep.extend(pitcherStatColumns) if playerType == "Pitcher" else columnsToKeep.extend(batterStatColumns)
    draftResults = draftResults[columnsToKeep]
    if (playerType == "Pitcher"):
        draftResults.rename({'G.1': 'G'}, axis=1, inplace=True)
    return draftResults

def removeNameSuffix(draftResults):
    draftResults = draftResults.copy()
    draftResults.loc[:,'Name'] = draftResults['Name'].apply(removeMinorsLink)
    return draftResults

def removeMinorsLink(draftee):
    return draftee.split('(')[0]
