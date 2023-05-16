# script-coverage-ai
Demo Proof of concept project of AI writing script coverage of screenplays.

Will read PDFs, .txt, .fountain, or pre-processed .json files with "metadata" and "content" entries.

Press the "Flag" button to save the output into an entry into "flagged/log.csv"

Only GPT-3.5-turbo model works. "debug" outputs the contents of the converted JSON contents to verify the screenplay is being parsed correctly.

Screenplay length is limited to the 4096 token limit of GPT-3.5-turbo. This will roughly translate to 12-15 page screenplays.

With access larger context models (GPT4-32k, Claude-100k), submitting entire feature-length screenplays would be possible.

I have no coding experience prior to this project. Created with 90% ChatGPT code.

==Install and Run==

Python 3.10 required.

Windows: Use run.bat to install and run.
Mac and Linux: Use run.sh to install and run.
