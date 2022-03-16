def playerStatsQuery(msfReturn, errorMessage):
  "Queries MSF to get requested stat for requested player."

  resp = errorMessage
        
  if len(msfReturn['playerStatsTotals']) > 0:
    playerTeam = msfReturn['playerStatsTotals'][0]['player']['currentTeam']['abbreviation']
    playerFirstName = msfReturn['playerStatsTotals'][0]['player']['firstName']
    playerLastName = msfReturn['playerStatsTotals'][0]['player']['lastName']
    try:
      if len(msfReturn['references']['playerStatReferences']) < 2:
        jsonCategory = msfReturn['references']['playerStatReferences'][0]['category'].lower()
        statName = msfReturn['references']['playerStatReferences'][0]['fullName']
        statAbr = msfReturn['references']['playerStatReferences'][0]['abbreviation']
        statResult = msfReturn['playerStatsTotals'][0]['stats'][jsonCategory][statName]
        resp = f"{playerFirstName} {playerLastName} ({playerTeam}) {statAbr} is {statResult}"

      else:
        statAbr = msfReturn['references']['playerStatReferences'][0]['abbreviation']
        jsonCategory0 = msfReturn['references']['playerStatReferences'][0]['category'].lower()
        statName0 = msfReturn['references']['playerStatReferences'][0]['fullName']
        statResult0 = msfReturn['playerStatsTotals'][0]['stats'][jsonCategory0][statName0]
        jsonCategory1 = msfReturn['references']['playerStatReferences'][1]['category'].lower()
        statName1 = msfReturn['references']['playerStatReferences'][1]['fullName']
        statResult1 = msfReturn['playerStatsTotals'][0]['stats'][jsonCategory1][statName1]
        resp = f"{playerFirstName} {playerLastName} ({playerTeam}) {statAbr} pitching is {statResult1}, and {statAbr} batting is {statResult0}."

    except KeyError:
      resp = "Sorry I don't have that stat."
      
  return resp; 