def teamStatsQuery(msfReturn, errorMessage):
  "Queries MSF to get requested stat for requested team."

  resp = errorMessage
        
  if len(msfReturn['teamStatsTotals']) > 0:
    team = msfReturn['teamStatsTotals'][0]['team']['name']
    try:
      if len(msfReturn['references']['teamStatReferences']) < 2:
        jsonCategory = msfReturn['references']['teamStatReferences'][0]['category'].lower()
        statName = msfReturn['references']['teamStatReferences'][0]['fullName']
        statAbr = msfReturn['references']['teamStatReferences'][0]['abbreviation']
        statResult = msfReturn['teamStatsTotals'][0]['stats'][jsonCategory][statName]
        resp = f"{team} {statAbr} is {statResult}"

      else:
        statAbr = msfReturn['references']['teamStatReferences'][0]['abbreviation']
        jsonCategory0 = msfReturn['references']['teamStatReferences'][0]['category'].lower()
        statName0 = msfReturn['references']['teamStatReferences'][0]['fullName']
        statResult0 = msfReturn['teamStatsTotals'][0]['stats'][jsonCategory0][statName0]
        jsonCategory1 = msfReturn['references']['teamStatReferences'][1]['category'].lower()
        statName1 = msfReturn['references']['teamStatReferences'][1]['fullName']
        statResult1 = msfReturn['teamStatsTotals'][0]['stats'][jsonCategory1][statName1]
        resp = f"{team} {statAbr} pitching is {statResult1}, and {statAbr} batting is {statResult0}."

    except KeyError:
      resp = "Sorry I don't have that stat."
      
  return resp; 