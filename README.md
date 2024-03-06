# owltracker
Track time spent in each task with ease

## Main project goals
I've built this project to help me manage my time spent on each task. 

### Main features:
- Ability to sync with clickup (open to integrate with other websites)
- Recognize computer idle time and subtract it from the timer or not. This way, if you leave your computer for a larger period of time there is no need to remember to stop the timer.

## Chosen technologies
PySimpleGui GUI was chosen simply because is easy and fast to develop and so far all functionalities needed were present.
The project doesn't focus on design, but in functionality

## How to use it
- If you want integration with clickup you need to either have env variables with your `workspace_id` and `api_token` or have a `.env` file in the directory level of requirements.txt
The `.env` file should look like this:
```workspace_id=XXXX
api_token=YYYY```
- Then you need to run `main.py` but with PYTHONPATH=. in the main directory
