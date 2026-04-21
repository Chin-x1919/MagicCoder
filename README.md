# MagicCodeพ
Local vibecoder tool — basically "Claude Code" but running on your own machine (and your own mistakes).

Yeah… it’s called *MagicCode* because I saw a Magic Mouse on my desk.  
Claude Code + Magic Mouse = MagicCode.  
Makes sense? No? Good.

---

## Why?

Because setting up real tools felt like too much work.

So instead of learning them… this exists.

---

## How does it work?

Simple (in theory):

User prompt  
+ system prompt  
→ sent to AI (via Ollama)  
→ AI returns executable command  
→ command gets sent to your terminal  
→ something happens (hopefully the intended thing)

---

## Does it work?

Sometimes...
Most of the time… not really 

---

## Features (kind of)

- AI generates terminal commands
- Auto-executes them (yes, really)
- Strong “it might work” energy

---

## Setup

1. (Optional, but recommended) create a virtual environment  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```
3. Make sure Ollama is running:
      ```bash
   ollama serve
    ```
4. Run the CLI:
      ```bash
   python3 cli.py
    ```


---

## Warning

- This executes REAL commands on your system  
- If it deletes your files, that’s on you  
- Do NOT use this on anything important  
- Seriously

---

## Roadmap (aka dreams)

- [ ] Make it less dumb  
- [ ] Reduce command hallucinations  
- [ ] Add memory that doesn’t forget instantly  
- [ ] Become actually usable  

---

## Final Note

If it works → miracle  
If it breaks → internal system design

---

License MIT
