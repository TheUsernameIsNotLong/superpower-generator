# superpower-generator
tool to generate superpowers based on the name provided.


## Luck System

The generator uses a luck mechanic, which alters two aspects of the power generation:

- Slightly increases the likelihood of generating multiple powers.
- Considerably increases the likelihood of generating higher-rarity powers.

### Calculating Luck

Luck is calculated through three main components, which all contribute an equal score towards the final luck value. They are:

- Vowel-Consonant Balance - Having a greater balance in vowels and consonants will achieve a greater luck value. A perfect balance will reach max luck in this component (e.g. `Dave` -> C, V, C, V = 2 Vowels, 2 Consonant)
- Even-Odd Balance - A balance in each letter's numerical position in the alphabet (A=1, B=2, etc...). A perfect balance will reach max luck in this component (e.g. `Dave` -> 4, 1, 22, 5 = 2 Even, 2 Odd) (This system wasn't meant to specifically merit Dave, it just happened to be a convenient example for both components)
- Name Length - Having a name's length closer to 6 letter's will provide a better score in the Name Length component. (e.g. `Graham`)

#### Vowel-Consonant Balance

One component is the balance between vowels and consonsants.

$`c_1=1-\frac{|v-c|}{v+c}`$

with

$`v`$ representing the number of vowels in the name (a, e, i, etc..)

and

$`c`$ representing the number of consonants in the name (b, c, d, etc..)

This is relative to the total number of letters in the name ($`v+c`$), so the name `Bob` (1 vowel, 2 consonants) will be hindered more than the name `Karen` (2 vowels, 3 consonants), despite both having a difference in 1 between vowels and consanants.

#### Even-Odd Balance

Another component is the balance between even and odd positioned letters.

$`c_2=1-\frac{|o-e|}{o+e}`$

with

$`o`$ representing the number of letters with an odd position (a, c, e, etc..)

and

$`e`$ representing the number of letters with an even position (b, d, f, etc..)

As with the Vowel-Consonant Balance component, the length of the name will also have a small impact on this component's value, due to the ($`o+e`$) in the function.

#### Name Length

The final component is the length of the name.

$`c_3=1-\frac{|6-l|}{6+l}`$

with

$`l`$ representing the number of letters in the name.

#### Final Formula

Combining all components results in the following formula:

$`L=\frac{c_1+c_2+c_3}{3}\times300`$

with

$`L`$ representing the ultimate luck value for the input name.

Unsimplified:

$`L=\frac{1-\frac{|v-c|}{v+c}+1-\frac{|o-e|}{o+e}+1-\frac{|6-l|}{6+l}}{3}\times300`$

<!-- $`\to L=\frac{3-\frac{|v-c|}{v+c}-\frac{|o-e|}{o+e}-\frac{|6-l|}{6+l}}{3}\times300`$

$`\to L=\frac{3-\frac{|v-c|}{l}-\frac{|o-e|}{l}-\frac{|6-l|}{6+l}}{3}\times300`$

$`\to L=\frac{3-\frac{|v-c|-|o-e|}{l}-\frac{|6-l|}{6+l}}{3}\times300`$

$`\to L=\frac{300(3-\frac{|v-c|-|o-e|}{l}-\frac{|6-l|}{6+l})}{3}`$

$`\to L=100(3-\frac{|v-c|-|o-e|}{l}-\frac{|6-l|}{6+l})`$

$`\to L=300-\frac{100(|v-c|-|o-e|)}{l}-\frac{100|6-l|}{6+l}`$ -->

This produces a final luck value between 0 and 100. Getting exactly 0 is impossible, mathematically speaking, but due to rounding, should be achievable through the program (albeit difficult).

#### Applying Luck

Luck is used for two functions, which affect the likelihood of certain powers being selected.

##### Luck Modifiers

Before being applied to the functions, a modifer is added.

Rarity Modifier:

$`L_r=\frac{L^2}{400}`$

Power Quanitity Modifier:

$`L_p=\frac{L^2}{2000}`$

This was split in order to reduce luck's impactfulness when using it to determine the number of powers one is assigned.

##### Luck Functions

> more added soon!!