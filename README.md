# Połonizacyja (opolaczywanije)
An exercise in applying Polish orthography to Russian language.
Check [the online version](https://https://polonizacyja.bakunin.nl/).

|слово|słowo|
|-|-|
| андрей | andrzej |
| полёт | polot |
| медведь | miedwiedź |
| полонизация | połonizacyja |


## The rules

This description might be slightly lagging the implementation.

1. **Basic vowels** are `а`, `о`, `у`, `э`, `ы` represented as `a`, `o`, `u`, `e`, `y`.

2. **Iotized vowels** are `я`, `ё`, `ю`, `е`, `и` represented as `ja`, `jo`, `ju`, `je`, `i`.

3. **Basic consonants** are `б`, `в`, `г`, `з`, `к`, `м`, `н`, `п`, `с`, `т`, `ф` represented as `b`, `w`, `g`, `z`, `k`, `m`, `n`, `p`, `s`, `t`, `f`.

4. Basic consonants are considered **soft (palatalized) consonants** when followed by either a **iotized vowel** (`я`, `ё`, `ю`, `е`, `и`) or `ь`. Palatalized versions of consonants are represented by appending `i` or `j` to them, such as `бь` becomes `bi` midword, `bj` terminal. The following vowel is represented without a `j`, f.e. `бя` => `bia`, one exception being `би` becomes `bi` (not `biy`).

5. `д` is repesented as `d`, the soft version is `dzi` midword or `dz` terminal; `ди` becomes `dzi`.

6. `л` is repesented as `ł`, the soft version is `l`.

7. `р` is represented as `r`, the soft version is `rz`. `ри` becomes `rzy`.

8. **Always-soft consonants** are `ж`, `х`, `ц`, `ч`, `ш`, `щ` repesented as `ż`, `ch`, `c`, `cz`, `sz`, `szcz`. The following vowel is always represented by its basic (non-iotized) version, f.e. `жи`, `ши` => `ży`, `szy`.

9. `й` and `ъ` are both represented as `j`.  The following vowel is always represented by its basic (non-iotized) version, f.e. `папайя` => `papaja`,  `подъезд` => `podjezd`.
