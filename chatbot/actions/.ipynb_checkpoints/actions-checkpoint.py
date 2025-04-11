from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random


todo_list = []

class ActionAddTodo(Action):
    def name(self) -> Text:
        return "action_add_todo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        task = next(tracker.get_latest_entity_values("task"), None)
        priority = next(tracker.get_latest_entity_values("priority"), None)

        if task:
            # set it to default
            if not priority:
                priority = "normal"
            else:
                priority = self.normalize_priority(priority)

            todo_list.append({"task": task, "priority": priority})
            dispatcher.utter_message(response="utter_added_task")
            
        else:
            dispatcher.utter_message(response="utter_ask_task")
        
        return []

    def normalize_priority(self, priority: str) -> str:
        priority = priority.lower()
        if priority in ["urgent", "asap", "high", "important"]:
            return "urgent"
        elif priority in ["normal", "medium", "soon"]:
            return "normal"
        elif priority in ["low", "low priority", "not important"]:
            return "low"
        else:
            return "normal"

class ActionShowTodos(Action):
    def name(self) -> Text:
        return "action_show_todos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not todo_list:
            dispatcher.utter_message(text="Your to-do list is empty. Must be nice.")
            return []

        tasks_formatted = [
            f"{i+1}. {item['task']} [{item['priority'].upper()}]" 
            for i, item in enumerate(todo_list)
        ]
        
        dispatcher.utter_message(text="Your never-ending list:\n" + "\n".join(tasks_formatted))
        return []

class ActionDeleteTodo(Action):
    def name(self) -> Text:
        return "action_delete_todo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        task = next(tracker.get_latest_entity_values("task"), None)

        if not task:
            dispatcher.utter_message(text="Delete what exactly? Try again.")
            return []
        
        for item in todo_list:
            if item["task"].lower() == task.lower():
                todo_list.remove(item)
                responses = [
                    f"Deleted '{task}'. Probably wasn't important anyway.",
                    f"'{task}' is gone. Like my will to live.",
                    f"Poof! '{task}' vanished. Like my motivation."
                ]
                dispatcher.utter_message(text=random.choice(responses))
                return []
        
        dispatcher.utter_message(text=f"'{task}' wasn't on your list.")
        return []

class ActionClearAllTodos(Action):
    def name(self) -> Text:
        return "action_clear_all_todos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        todo_list.clear()
        responses = [
            "Boom! List obliterated. Enjoy your clean slate (until tomorrow).",
            "All tasks deleted. Now you can stress about nothing!",
            "List cleared. *pretends to be surprised*"
        ]
        dispatcher.utter_message(text=random.choice(responses))
        return []

class ActionCheckPendingTasks(Action):
    def name(self) -> Text:
        return "action_check_pending_tasks"

    def run(self, dispatcher, tracker, domain):
        if not todo_list:
            dispatcher.utter_message(response="utter_goodbye_all_done")
            return []
        
        count = len(todo_list)
        urgent = sum(1 for item in todo_list if item["priority"].upper() == "urgent")

        if urgent:
            dispatcher.utter_message(text=f"Wait! You have {urgent} URGENT tasks pending. *facepalm*")
        else:
            dispatcher.utter_message(text=f"Leaving? You still have {count} tasks. Typical.")

        return []

class ActionGiveMotivation(Action):
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
