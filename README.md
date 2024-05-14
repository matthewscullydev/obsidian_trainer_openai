## Obsidian Mindmap Generator
---

This is a tool for generating mindmaps and practicing retention within obsidian. In order to use this you will want to follow these preliminary steps first.

* Create a new Obsidian vault
	* This is for the safety of your other .md files within the directory you will place this script.
	* It becomes harder to visualize your mindmaps with larger vaults so small vault sizes will be the most optimal

- Place mindmap_generator.py in your obsidian vault directory
```bash
mv mindmap_generator.py /home/User/Documents/yourvault/
```
- Configure your Obsidian Graph View Force Filters so that the mindmap is discernible
	- Set Center Force, Repel Force, and Link Force to 1.0
	- Set Link Distance to 30
 
---
## Selecting Bubble Tree to Train With
---

Once you have generated a mindmap choose option 2 to select a root node for retention training.

Type in the name of the bubble whose children you would like to practice retention with.


When you enter free mode using option 1 its children will be turned into question marks.

You will type in the names of the children which are converted into question marks in order to practice retention!

---

https://github.com/matthewscullydev/obsidian_trainer/assets/26017402/29597e4a-a8fc-454a-b691-bd49a7ec9e39

## Importing Mindmaps
---

To import mindmaps find your Flashcard directory where mindmaps are saved.

use a copy command with a wildcard to copy all markdown files into your vault

```
cd Flashcards/
cp History/*.md /your_vault/
```

