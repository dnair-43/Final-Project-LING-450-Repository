# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

class ActionAddTodo(Action):
    """Adds a task to the to-do list with optional priority"""
    def name(self) -> Text:
        return "action_add_todo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        task = next(tracker.get_latest_entity_values("task"), None)
        priority = next(tracker.get_latest_entity_values("priority"), "whenever")
        
        if not task:
            dispatcher.utter_message(response="utter_ask_task")
            return []
            
        todo_list = tracker.get_slot("todo_list") or []
        todo_list.append({"task": task, "priority": priority})
        
        # Snarky confirmation based on priority
        if priority == "ASAP":
            dispatcher.utter_message(text=f"Ugh, FINE. Added '{task}' as TOP priority. *dramatic eye roll*")
        else:
            dispatcher.utter_message(text=f"*Sigh* Added '{task}' to your list (priority: {priority})")
        
        return [SlotSet("todo_list", todo_list)]

class ActionShowTodos(Action):
    """Displays the current to-do list with priorities"""
    def name(self) -> Text:
        return "action_show_todos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        todo_list = tracker.get_slot("todo_list") or []
        
        if not todo_list:
            dispatcher.utter_message(text="Your list is empty. Enjoy your false sense of productivity.")
            return []
            
        # Format tasks with priorities
        tasks_formatted = []
        for i, item in enumerate(todo_list, 1):
            task = item["task"]
            priority = item["priority"].upper()
            tasks_formatted.append(f"{i}. {task} [{priority}]")
        
        dispatcher.utter_message(text="Your pitiful to-do list:\n" + "\n".join(tasks_formatted))
        return []

class ActionDeleteTodo(Action):
    """Removes a specific task from the list"""
    def name(self) -> Text:
        return "action_delete_todo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        task = next(tracker.get_latest_entity_values("task"), None)
        todo_list = tracker.get_slot("todo_list") or []
        
        if not task:
            dispatcher.utter_message(text="Delete what exactly? Use your words.")
            return []
            
        # Case-insensitive search
        found = next((item for item in todo_list 
                     if item["task"].lower() == task.lower()), None)
        
        if found:
            todo_list.remove(found)
            responses = [
                f"Deleted '{task}'. Probably wasn't important anyway.",
                f"'{task}' is gone. Like my will to live.",
                f"Poof! '{task}' vanished. Like my motivation."
            ]
            dispatcher.utter_message(text=random.choice(responses))
        else:
            dispatcher.utter_message(text=f"'{task}' wasn't on your list. Typical forgetfulness.")
        
        return [SlotSet("todo_list", todo_list)]

class ActionClearAllTodos(Action):
    """Nuclear option - clears the entire list"""
    def name(self) -> Text:
        return "action_clear_all_todos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        responses = [
            "Boom! List obliterated. Enjoy your clean slate (until tomorrow).",
            "All tasks deleted. Now you can stress about nothing!",
            "List cleared. *pretends to be surprised*"
        ]
        dispatcher.utter_message(text=random.choice(responses))
        return [SlotSet("todo_list", [])]

class ActionCheckPendingTasks(Action):
    """Checks for unfinished tasks when saying goodbye"""
    def name(self) -> Text:
        return "action_check_pending_tasks"
    def run(self, dispatcher, tracker, domain):
        todo_list = tracker.get_slot("todo_list") or []
        
        if not todo_list:
            dispatcher.utter_message(response="utter_goodbye_all_done")
        else:
            count = len(todo_list)
            urgent = sum(1 for item in todo_list if item["priority"] == "ASAP")
            if urgent:
                dispatcher.utter_message(text=f"Wait! You have {urgent} URGENT tasks pending. *facepalm*")
            else:
                dispatcher.utter_message(text=f"Leaving? You still have {count} tasks. Typical.")
        return []
##    def run(self, dispatcher: CollectingDispatcher,
##            tracker: Tracker,
##            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
##        
##        todo_list = tracker.get_slot("todo_list") or []
##        
##        if todo_list:
##            count = len(todo_list)
##            urgent = sum(1 for item in todo_list if item["priority"] == "ASAP")
##            
##            if urgent:
##                dispatcher.utter_message(text=f"Wait! You have {urgent} URGENT tasks pending. *facepalm*")
##            else:
##                dispatcher.utter_message(text=f"Leaving? You still have {count} tasks. Typical.")
##        else:
##            dispatcher.utter_message(response="utter_goodbye_all_done")
##        
##        return []

class ActionGiveMotivation(Action):
    """Provides sarcastic 'motivation'"""
    def name(self) -> Text:
        return "action_give_motivation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        motivations = [
            "The only thing standing between you and success is... well, everything.",
            "Dream big! Or don't. I'm not your life coach.",
            "You can do it! (Statistically unlikely, but possible.)",
            "Rise and grind! Or just rise. Grinding is optional.",
            "Be the best version of yourself! (The bar is low.)"
        ]
        dispatcher.utter_message(text=random.choice(motivations))
        return []
