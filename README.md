# wanderskull

we are so back

## Todo and Notes
<details><summary>change to state stack</summary>

  - also figure out division and heiarchy of states
</details>
<details><summary>create tick rate system</summary>

  - for potential time related magic and enviroments
</details>
<details><summary>enemies</summary>

  - behaviour modules
    - wander
    - pathfind: simple, constant(range), avoidant, tracking, direct
      - get a* down
      - figure out when to run and how to store results
    - enm-enm, enm-env
  - lore
    - figure out enemy-enemy and enemy-enviroment interactions
</details>
<details><summary>modular attack system</summary>

  - magic synthesis
    - solid liquid gas plasma ether force
    - mana consumption
    - matter synthesis vs using surroundings should have different consumptions
    - eg, chaining commands (ether synthesis) + (force synthesis: vector) -> a force applied on a peice of ether forming a magic bullet; values should be tweakable
  - physical attacks
    - start with sword forms from basic sword attacks; form custom attack combinations
    - figure out balance for recoil, recovery frames, movement, attack area
    - figure out system for linking 1 basic attack to another, calculate recovery frames and recoil from that</details>
<details><summary>hp system</summary>

  - this ones gonna be a pain to implement
  - take inspo from rimworld CE
    - blunt peircing slashing temperature
    - limb hp, vital hp hearts horizontal, blood vertical filling the hearts
    - blunt force trauma: body durability
    - asphyxilation: O2 stat
    - blood loss: blood stat
    - disease: generalize into infection
    - possibly research into sepsis</details>
<details><summary>map gen</summary>

  - partial should be previously generated (city, npc areas, etc etc)
    - TODO: these areas can be permanently changed in game, figure out if saving all data or optimizing and saving only parts that are different
  - procgen dungeons
    - current world system uses rooms not one cohesive world, plan accordingly </details>
<details><summary>minimap system</summary>

  - 2d top down, using layering and fade system; refer to MC Xaero's Minimap
  - possible 3d wireframe isometric render when focused (M or TAB?) (if im crazy enough to implement that)</details>

<details><summary>sprite creation</summary>

-  <img src="https://media1.tenor.com/m/9PTGVf4BLwYAAAAC/crying-emoji-dies.gif" width="300" />
- probably 8 directions per
- |sprite|desc|status|
  |------|----|------|
  |player|base|0/8|
  |player|sword|0/8x8|
  </details>


## Current list of (known) bugs

<!-- (the description can be longer than the table vvvv) -->
| Bug         | Description                             | Importance | notes |
| ----------- | --------------------------------------- | ---------- |-------|
| Example     | Causes player to cry.                   | \*\*\*     | Skill issue |
| Exit Crash  | Exiting the game crashes it on re-entry | \*\*\*\*\* | caused by using the same state on re-entry, state vars and init conditions are desynced. ignore, will address when creating actual play state |
| Doorways    | for shared doorways, only one side will open, leaving it still blocked | \*\*\*\*  | Don't actually need to fix as for any dungeon, only 1 room will have closed doors at a time. Though because of this, monsters can only appear in a room when the doors are closed.|

#### We all start somewhere
keybind for multiline comment/uncomment: {ctrl or cmd} + /

To install dependencies, use `make install`

To build, use `make build`
---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
