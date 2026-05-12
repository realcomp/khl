# Performance Audit

## Executive Summary

This audit identifies the root cause of a 7.4-second PostgreSQL slow query with repeated INNER JOINs to hockeyapp_clubplayermatch. The query contains 63 identical JOINs with different aliases (T6, T8, T10, ..., T130), indicating an N+1 query problem where filter conditions are applied individually rather than using efficient bulk operations. The issue is traced to Django ORM query patterns that generate a separate JOIN for each match ID filter instead of using a more efficient subquery or IN clause approach.

## Evidence Reviewed

- docs/performance/slow_sql_only.log
- docs/performance/db_scan_stats.txt
- docs/performance/db_table_sizes.txt
- Codebase in /Volumes/Projects/khl/

## Critical Finding: ironmans() in hockeyapp/managers/player.py

### Source Location
File: hockeyapp/managers/player.py
Method: ironmans() in ClubPlayerQuerySet class

### Problematic Code
```python
def ironmans(self, club, season):
    ''''
    Железный человек - игрок (кроме вратаря),
    поучаствовавший во всех матчах сезона
    '''
    from hockeyapp.models import Match
    matches = set(
        Match.objects
        .filter(Q(home_team=club) | Q(guest_team=club))
        .filter(challenge_type__isnull=False, challenge_type__gt=0)
        .filter(clubplayermatch__clubplayer__season=season)
        .values_list('pk', flat=True))
    qs = self.exclude(line=1).filter(
        clubplayermatch__match__isnull=False,
        clubplayermatch__match__challenge_type__isnull=False,
        clubplayermatch__match__challenge_type__gt=0)
    for pk in matches:
        qs = qs.filter(clubplayermatch__match=pk)
    return qs
```

## Exact Slow SQL Pattern from Logs

From docs/performance/slow_sql_only.log:
```sql
SELECT "hockeyapp_clubplayer"."id", "hockeyapp_clubplayer"."player_id", "hockeyapp_clubplayer"."club_id", "hockeyapp_clubplayer"."number", "hockeyapp_clubplayer"."line", "hockeyapp_clubplayer"."start_date", "hockeyapp_clubplayer"."end_date", "hockeyapp_clubplayer"."league_id", "hockeyapp_clubplayer"."season_id" 
FROM "hockeyapp_clubplayer" 
INNER JOIN "hockeyapp_clubplayermatch" ON ( "hockeyapp_clubplayer"."id" = "hockeyapp_clubplayermatch"."clubplayer_id" ) 
INNER JOIN "hockeyapp_match" ON ( "hockeyapp_clubplayermatch"."match_id" = "hockeyapp_match"."id" ) 
INNER JOIN "hockeyapp_clubplayermatch" T6 ON ( "hockeyapp_clubplayer"."id" = T6."clubplayer_id" ) 
INNER JOIN "hockeyapp_clubplayermatch" T8 ON ( "hockeyapp_clubplayer"."id" = T8."clubplayer_id" ) 
INNER JOIN "hockeyapp_clubplayermatch" T10 ON ( "hockeyapp_clubplayer"."id" = T10."clubplayer_id" ) 
INNER JOIN "hockeyapp_clubplayermatch" T12 ON ( "hockeyapp_clubplayer"."id" = T12."clubplayer_id" ) 
[...continuing with 58 more identical JOINs with aliases T14 through T130...]
WHERE ("hockeyapp_clubplayer"."club_id" = 56 AND "hockeyapp_clubplayer"."season_id" = 19 AND NOT ("hockeyapp_clubplayer"."line" = 1) AND "hockeyapp_match"."challenge_type" IS NOT NULL AND "hockeyapp_match"."challenge_type" > 0 AND "hockeyapp_clubplayermatch"."match_id" IS NOT NULL AND T6."match_id" = 36482 AND T8."match_id" = 33060 AND T10."match_id" = 35849 [...continuing with 60 more match_id conditions...])
ORDER BY "hockeyapp_clubplayer"."id" DESC LIMIT 1
```

## Why the Repeated .filter() Loop Generates Many INNER JOINs

The Django ORM's query construction mechanism treats each `.filter(clubplayermatch__match=pk)` call as a new condition that requires joining the `hockeyapp_clubplayermatch` table again. Since this filter is called in a loop for each match ID, Django generates a separate JOIN with a unique alias for each iteration:

1. First filter: Creates JOIN with base alias "hockeyapp_clubplayermatch"
2. Second filter: Creates JOIN with alias "T6" 
3. Third filter: Creates JOIN with alias "T8"
4. And so on up to "T130"

Each JOIN has a specific WHERE condition matching one match ID, resulting in the inefficient cartesian product pattern instead of a more efficient subquery approach.

## Proposed Django 1.7 / Python 2.7 Compatible Fix

Replace the loop-based filtering approach with a counting-based solution using Django's aggregation capabilities:

```python
def ironmans(self, club, season):
    ''''
    Железный человек - игрок (кроме вратаря),
    поучаствовавший во всех матчах сезона
    '''
    from django.db.models import Count
    from hockeyapp.models import Match
    
    # Get the total number of matches for this club/season
    total_matches = Match.objects.filter(
        Q(home_team=club) | Q(guest_team=club)
    ).filter(
        challenge_type__isnull=False, 
        challenge_type__gt=0
    ).filter(
        clubplayermatch__clubplayer__season=season
    ).distinct().count()
    
    if total_matches == 0:
        return self.none()
    
    # Find players who participated in all matches
    return self.exclude(line=1).filter(
        clubplayermatch__match__challenge_type__isnull=False,
        clubplayermatch__match__challenge_type__gt=0
    ).annotate(
        match_count=Count('clubplayermatch__match', distinct=True)
    ).filter(match_count=total_matches)
```

This approach:
1. Calculates the total number of matches once
2. Uses annotation to count how many matches each player participated in
3. Filters players whose participation count equals the total matches
4. Generates a single efficient query instead of multiple JOINs

## Risk Level

Medium - This is a logic change from a JOIN-based approach to a counting-based approach. While the end result should be identical, there's a risk of:
1. Different behavior with edge cases (empty matches, NULL values)
2. Subtle differences in how Django handles the counting vs. JOIN logic
3. Performance characteristics may vary depending on data distribution

## Test Plan

1. Create unit tests that verify the same players are identified as "ironman" players before and after the optimization
2. Test with various edge cases:
   - Clubs with no matches
   - Seasons with no matches
   - Players who participated in zero matches
   - Players who participated in all matches
3. Profile query execution time and compare before/after
4. Verify query plan improvements using EXPLAIN ANALYZE
5. Test with production-like data volumes to ensure the optimization provides the expected performance benefits

## Additional Findings

### PlayerTimelineGenerator N+1 Issues
File: hockeyapp/timeline_tasks.py
Multiple methods execute ClubPlayerMatch queries in loops, creating classic N+1 patterns:
- first_hat_trick_event()
- first_poker_event() 
- points_events()
- matches_events()
- club_matches_events()

### RelatedPlayer Similarity Calculation Inefficiencies
File: hockeyapp/models/players.py
Method: RelatedPlayer.calc()
Nested loops with repeated database queries causing exponential time complexity for similarity calculations.

### API View select_related/prefetch_related Opportunities
Files: 
- hockeyapp/views/v1/api/players.py
- hockeyapp/views/api/players.py
Current queryset only uses select_related('clubplayer') but could benefit from additional related object optimizations during serialization.

## Recommended Implementation Order

1. **Critical**: Fix the ironmans() method in hockeyapp/managers/player.py - Addresses the 7.4s query directly
2. **High**: Optimize PlayerTimelineGenerator in hockeyapp/timeline_tasks.py - Reduces multiple N+1 query patterns
3. **High**: Refactor RelatedPlayer.calc() in hockeyapp/models/players.py - Improves similarity calculation performance
4. **Medium**: Add select_related/prefetch_related optimizations in API views - General query efficiency improvements