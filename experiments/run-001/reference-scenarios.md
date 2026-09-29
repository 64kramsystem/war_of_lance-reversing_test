# Reference scenarios frozen before the run

For each case, first record the original version's setup, exact inputs and observable results; then repeat those inputs in the port. Select concrete units/locations from the original and preserve the chosen setup. A case without reproducible original evidence remains untested. Preserve the initial scenario definitions; extensions are additions, not replacements.

| ID | Behavior to compare | Required evidence |
| --- | --- | --- |
| R01 | Boot and begin a new game with recorded settings | Original menus, initial map, factions/units and initial turn state; matching port state and rendering |
| R02 | Select a unit, inspect it and move it legally | Starting/destination positions, displayed properties, movement availability and state changes |
| R03 | Attempt an illegal move and end movement | Original rejection or alternative behavior and preservation/change of state |
| R04 | Resolve a combat between recorded forces | Before/after troop values, modifiers visible or recovered from code, retreat/destruction and result rendering; identify random inputs |
| R05 | Perform a diplomatic action and advance to its resolution | Relevant country/faction state, action cost or constraints, result and timing; identify randomness |
| R06 | Send or manage a champion on a quest and advance its resolution | Champion state, action rules, time progression and outcome; identify randomness |
| R07 | Advance an AI turn from a preserved state | Turn/phase sequence, resource/unit changes and AI decisions; exact matches require controlled randomness |
| R08 | Save a non-initial state and load it in the same implementation | Round-trip preservation of all recovered game state; original and port save formats need not be identical |
| R09 | Reach each distinct victory/defeat condition | Original triggering rules supported by code and runtime observation, resulting state and display; missing runtime coverage remains explicit |
| R10 | Render the recorded menus, map views, unit information and combat/results screens | Original captures plus palette/asset/position evidence and programmatic comparison where possible; unexplained differences are deviations |

For random behavior, matching one outcome is insufficient. Recover the selection logic and relevant distributions/thresholds or control the original random state; state which comparison was performed. Do not treat different seeds as proof of a wrong implementation or use randomness to dismiss unexplained differences.
