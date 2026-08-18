# Size proof

Open the **local** file in a browser at **100% zoom**:

`/Users/jacobroecker/code/waloyo/art/reference/size-proof/index.html`

GitHub’s file view will not load the pictures.

Each cell is a pre-cropped square on the **same dark field**. Pedia cells have more headroom; hex tokens are packed tighter. Parchment, peach, and checkerboard backgrounds are stripped so you are comparing figures, not paper.

Regenerate thumbs after new stills:

```
python3 -m venv /tmp/waloyo-proof && /tmp/waloyo-proof/bin/pip install pillow
/tmp/waloyo-proof/bin/python3 art/reference/size-proof/build_thumbs.py
```
