#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: takenote
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import datetime  # Basic date and time types
from random import choice  # Generate pseudo-random numbers
try:
    import thread  # Low-level threading API (Python 2.7)
except ImportError:
    import _thread as thread  # Low-level threading API (Python 3.x)

from ava.reminder import Reminder

reminder = Reminder()


class TakeNoteCommand():
    """Class to contains taking notes process with simply if-else struct.
    """

    def takenote_first_compare(self, com, doc, h, note_taker, user_answering_note, userin, user_prefix):
        """Method to ava's first command struct of taking note ability.

        Args:
            note_taker (object):        note_taker class's object.
            user_answering_note:       User answering string array.
            userin:                    :class:`ava.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        if h.check_verb_lemma("add") or h.check_verb_lemma("generate") or h.check_verb_lemma("create") or (h.check_verb_lemma("take") and h.check_noun_lemma("note")) or h.check_verb_lemma("remind"):
            if h.check_verb_lemma("do") or (h.check_verb_lemma("do") and h.check_noun_lemma("list")):        # FOR creating To Do list
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "add" or token.lemma_ == "generate" or token.lemma_ == "create" or
                            token.lemma_ == "do" or token.lemma_ == "list" or token.lemma_ == "ava" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                user_answering_note['status'] = True
                user_answering_note['is_todo'] = True
                if not takenote_query:  # when command come without note.
                    return userin.say(choice([
                        "Okay, " + user_prefix + ". What is the name?",
                        "I'm listening for give a name to list, " + user_prefix + ".",
                        "Alright, " + user_prefix + ". Please, say a list name.",
                        "Ready. What is the name of list?",
                        "Say a name for list."
                    ]))
                else:  # when command came with note.
                    user_answering_note['todo_listname'] = ""
                    user_answering_note['todo_listcount'] = 1

                    rep = com.replace('create to do list', '')
                    rep = rep.replace('add to do list', '')
                    rep = rep.replace('generate to do list', '')

                    user_answering_note['note_keeper'] = rep
                    return userin.say(choice([
                        "1. item receipt. Give a name to the list, " + user_prefix + "."

                    ]))
            if h.check_text("me") or h.check_noun_lemma("reminder"):  # FOR reminder
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "add" or token.lemma_ == "generate" or token.lemma_ == "remind" or token.lemma_ == "create" or
                            token.lemma_ == "reminder" or token.lemma_ == "ava" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                user_answering_note['status'] = True
                user_answering_note['is_remind'] = True
                if not takenote_query:  # when command came without note.
                    return userin.say(choice([
                        "Understood. what is note?",
                        "Yes! I'm listening the note.",
                        "Alright, " + user_prefix + ". What will I remind?",
                        "Ready to record, " + user_prefix + ". what is the note?",
                        "Okay, " + user_prefix + ". Please enter the note."
                    ]))
                else:  # when command came with note.
                    rep = com.replace('remind me', '')
                    rep = rep.replace('create reminder', '')
                    rep = rep.replace('add reminder', '')
                    rep = rep.replace('generate reminder', '')

                    user_answering_note['note_keeper'] = rep
                    return userin.say(choice([
                        "It's Okay, " + user_prefix + ". When will I remind?",
                        "Alright. When do you want to remember?",
                        "Alright, " + user_prefix + ". What is the remind time?",
                        "Note taken. Give the remind time.",
                        "I get it, " + user_prefix + ". Please enter the remind time."
                    ]))
            if (h.check_noun_lemma("note") or h.check_lemma("")) and not (h.directly_equal("add") or h.directly_equal("create") or h.directly_equal("generate")):  # FOR taking note.
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "add" or token.lemma_ == "take" or token.lemma_ == "note" or token.lemma_ == "create" or
                            token.lemma_ == "generate" or token.lemma_ == "ava" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                if not takenote_query:  # when command came without note.
                    user_answering_note['status'] = True
                    return userin.say(choice([
                        "Yes, " + user_prefix + ".",
                        "Yes. I'm listening",
                        "Ready, " + user_prefix + ".",
                        "Ready to record, " + user_prefix + ".",
                        "Keep going, " + user_prefix + "."
                    ]))
                else:  # when command came with note.
                    rep = com.replace('take note', '')
                    rep = rep.replace('create note', '')
                    rep = rep.replace('add note', '')
                    rep = rep.replace('generate note', '')

                    note_taker.db_upsert(rep)
                    user_answering_note['status'] = False
                    return userin.say(choice(["The note taken", "The note was recorded", "I get it"]) + choice(
                        [".", ", " + user_prefix + "."]))
        return None

    def takenote_second_compare(self, com, doc, h, note_taker, user_answering_note, userin, user_prefix):
        """Method to ava's first command struct of taking note ability.

        Args:
            com (str):                 User's command.
            doc:                       doc of com from __init__.py
            h:                         doc helper from __init__.py
            note_taker (object):        note_taker class's object.
            user_answering_note:       User answering string array.
            userin:                    :class:`ava.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        if user_answering_note['status']:
            if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith("forget it") or com.startswith("WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW") or com.startswith("FORGET IT"):  # for writing interrupt while taking notes and creating reminders.
                user_answering_note['status'] = False
                user_answering_note['is_todo'] = False
                user_answering_note['todo_listname'] = None
                user_answering_note['todo_listcount'] = 0
                user_answering_note['note_keeper'] = None
                user_answering_note['is_remind'] = False
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([".", ", " + user_prefix + "."]))

            if user_answering_note['is_todo']:
                if not user_answering_note['todo_listname']:
                    user_answering_note['todo_listname'] = com
                    if not user_answering_note['note_keeper']:  # keeper compare for the elastic usage.
                        return userin.say("I get it. Enter the 1. item...")
                    else:
                        note_taker.db_upsert(user_answering_note['note_keeper'], None, None,
                                             user_answering_note['todo_listname'],
                                             user_answering_note['todo_listcount'], user_answering_note['is_todo'])
                        return userin.say(
                            "I get it. Enter the " + str(user_answering_note['todo_listcount'] + 1) + ". item...")
                else:
                    if com.startswith("enough") or com.startswith("it is okay") or com.startswith(
                            "it is ok") or com.startswith("it's okay") or com.startswith("it's ok") or com.startswith(
                            "end") or com.startswith(
                            "ENOUGH") or com.startswith("IT IS OKAY") or com.startswith("IT IS OK") or com.startswith(
                            "IT'S OKAY") or com.startswith("IT'S OK") or com.startswith("END"):
                        temporary_keeper = user_answering_note['todo_listname']
                        user_answering_note['status'] = False
                        user_answering_note['is_todo'] = False
                        user_answering_note['todo_listname'] = None
                        user_answering_note['todo_listcount'] = 0
                        user_answering_note['note_keeper'] = None

                        return userin.say(choice(
                            ["List was recorded", temporary_keeper + " ToDo List generated",
                             "Get it. List ready"]) + choice([".", ", " + user_prefix + "."]))
                    user_answering_note['todo_listcount'] += 1
                    note_taker.db_upsert(com, None, None, user_answering_note['todo_listname'],
                                         user_answering_note['todo_listcount'], user_answering_note['is_todo'])

                    return userin.say(choice(
                        ["It is Okay. Give " + str(user_answering_note['todo_listcount'] + 1) + ". item",
                         "Get it. Give other item", "Okay. Enter other one", "Okay, you can say other",
                         "Get it. Listening for other"]) + choice([".", ", " + user_prefix + "."]))

            if user_answering_note['is_remind']:
                if user_answering_note['is_again']:  # for using same reminder on different time.
                    user_answering_note['is_again'] = False
                    if com.startswith("yes") and com.endswith("yes") or com.startswith("yep") and com.endswith("yep") or com.startswith("okay") and com.endswith("okay") or h.check_deps_contains("do it"):
                        return userin.say(choice(["It's okay", "Get it", "reminder will repeat", " It has been set again"]) + choice(
                            [", " + user_prefix + ". ", ". "]) + choice(
                            ["What is the remind time?", "When do you want to remind?", "Give remind time.",
                             "Say the time"]))
                    else:
                        user_answering_note['status'] = False
                        user_answering_note['is_remind'] = False
                        user_answering_note['note_keeper'] = None
                        return userin.say(choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([". ", ", " + user_prefix + ". "]))

                if not user_answering_note['note_keeper']:
                    user_answering_note['note_keeper'] = com
                    return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice(
                        [", " + user_prefix + ". ", ". "]) + choice(
                        ["What is the remind time?", "When do you want to remind?", "Give the remind time.",
                         "Say the time"]))
                else:  # flexible usage is going to be set.
                    if com.startswith("after") or com.endswith("later") or com.startswith("in") or com.startswith(""):
                        if h.check_noun_lemma("minute") or h.check_noun_lemma("minutes"):
                            takenote_query = ""
                            for token in doc:
                                if not (
                                        token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "minute" or token.lemma_ ==
                                        "minutes" or token.is_stop):
                                    takenote_query += ' ' + token.text
                                    minute = float(takenote_query)
                                    if isinstance(minute, float):
                                        # timestamp is a kind of second.
                                        time = datetime.datetime.now().timestamp() + minute * 60
                                        time = int(time / 60)
                                        note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True, True)
                                        # return userin.say(str(time.strftime("%H:%M")))
                                    else:
                                        return userin.say("Repeat!")
                        elif h.check_noun_lemma("hour") or h.check_noun_lemma("hours"):
                            takenote_query = ""
                            for token in doc:
                                if not (
                                        token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "hour" or token.lemma_ ==
                                        "hours" or token.is_stop):
                                    takenote_query += ' ' + token.text
                                    hour = int(takenote_query)
                                    if isinstance(hour, float):
                                        # timestamp is a kind of second.
                                        time = datetime.datetime.now().timestamp() + hour * 60 * 60
                                        time = int(time / 60)
                                        note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True, True)
                                        # return userin.say(str(time))
                                    else:
                                        return userin.say("Repeat!")
                        elif h.check_noun_lemma("day") or h.check_noun_lemma("days"):
                            takenote_query = ""
                            for token in doc:
                                if not (
                                        token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "day" or token.lemma_ ==
                                        "days" or token.is_stop):
                                    takenote_query += ' ' + token.text
                                    day = int(takenote_query)
                                    if isinstance(day, float):
                                        # timestamp is a kind of second.
                                        time = datetime.datetime.now().timestamp() + day * 24 * 60 * 60
                                        time = int(time / 60)
                                        note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True, True)
                                        # return userin.say(str(time))
                                    else:
                                        return userin.say("Repeat!")
                        user_answering_note['status'] = False
                        user_answering_note['is_remind'] = False
                        user_answering_note['note_keeper'] = None
                        if not user_answering_note['is_active']:  # if reminder checker loop not run, start the loop.
                            thread.start_new_thread(reminder.remind, (note_taker, userin, user_prefix, user_answering_note))
                        return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice(
                            [", " + user_prefix + ". ", ". "]) + choice(
                            ["Reminder Added.", "I'm waiting to remind.", "I will remind.",
                             "Reminder has been set."]))
            else:                                      # taking note second compare here.
                user_answering_note['status'] = False
                note_taker.db_upsert(com)
                return userin.say(choice(
                    ["The note Taken", "Alright", "I noted", "Ready whenever you want to get it", "Get it"]) + choice(
                    [".", ", " + user_prefix + ". "]))

        return None

    def getnote_first_compare(self, com, doc, h, note_taker, user_answering_note, userin, user_prefix):
        """Method to ava's first command struct of getting note ability.

                Args:
                    com (str):                 User's command.
                    note_taker (object):        note_taker class's object.
                    user_answering_note:       User answering string array.
                    userin:                    :class:`ava.utilities.TextToAction` instance.
                    user_prefix:               user's preferred titles.
                """

        if h.check_verb_lemma("say") or h.check_verb_lemma("get") or h.check_verb_lemma("give"):

            if h.check_noun_lemma("note") or h.check_noun_lemma("notes"):
                return userin.say(note_taker.db_get(None, None))

            if h.check_verb_lemma("do") or (h.check_verb_lemma("do") and h.check_noun_lemma("list")):
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "say" or token.lemma_ == "get" or token.lemma_ == "give" or
                            token.lemma_ == "do" or token.lemma_ == "list" or token.lemma_ == "ava" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                if not takenote_query:  # when command come without note.
                    user_answering_note['has_listname'] = False
                    result = note_taker.db_get(None, None, True)
                    if not result:
                        user_answering_note['has_listname'] = True
                        return userin.say("There is no list")
                    return userin.say(choice([
                        "which list",
                        "Alright, say the list name",
                        "Okay, What is the name of list",
                        "List name"
                    ]) + choice(["?", ", " + user_prefix + "?"]))
                else:  # when command came with note.
                    result = note_taker.db_get(None, com, True)
                    if not result:
                        user_answering_note['has_listname'] = False
                        return userin.say(choice([
                            "This name is not exist",
                            "I couldn't find it, say again",
                            "Not found, Repeat",
                            "Not exist, speak again"
                        ]) + choice(["?", ", " + user_prefix + "?"]))
                    else:
                        return userin.say(result)
        return None

    def getnote_second_compare(self, com, h, note_taker, user_answering_note, userin, user_prefix):
        """Method to ava's second command struct of getting note ability.

        Args:
            com (str):                 User's command.
            h:                         doc helper from __init__.py
            note_taker (object):       note_taker class's object.
            user_answering_note:       User answering string array.
            userin:                    :class:`ava.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        if not user_answering_note['has_listname']:
            if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith("forget it") or com.startswith("WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW") or com.startswith("FORGET IT"):  # for writing interrupr while taking notes and creating reminders.
                user_answering_note['has_listname'] = True
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice(
                        [". ", ", " + user_prefix + ". "]))

            if (h.check_lemma("give") or h.check_lemma("say") or h.check_lemma("get")) or h.check_verb_lemma("remind"):
                if h.check_noun_lemma("names") or h.check_noun_lemma("them") or not h.check_noun_lemma(""):
                    result = note_taker.db_get(None, None, True)
                    return userin.say("list of the lists:\n" + result)

            result = note_taker.db_get(None, com, True)
            if not result:
                return userin.say(choice([
                    "This name is not exist",
                    "I couldn't find it, say again",
                    "Not found, Repeat",
                    "Not exist, speak again"
                ]) + choice(["?", ", " + user_prefix + "?"]))
            else:
                user_answering_note['has_listname'] = True
                return userin.say(result)
        return None

    def deletenote_(self, h, note_taker, userin):
        """Method to ava's first command struct of getting note ability.

                Args:
                    note_taker (object):        note_taker class's object.
                    userin:                    :class:`ava.utilities.TextToAction` instance.
                """

        if h.check_lemma("delete") or h.check_verb_lemma("remove"):
            if h.check_lemma("all"):
                if h.check_lemma("over") and h.check_noun_lemma("database"):
                    note_taker.db_delete(None, None, True)
                    return userin.say("notes database cleared")

                if h.check_lemma("note") or h.check_lemma("notes"):
                    note_taker.db_delete()
                    return userin.say("All notes Deleted")

                if (h.check_verb_lemma("do") and h.check_noun_lemma("lists")) or (h.check_verb_lemma("do") and h.check_noun_lemma("list")):
                    note_taker.db_delete(None, None, False, None, None, True)
                    return userin.say("All to do lists deleted")

                if h.check_lemma("reminder") or h.check_lemma("reminders"):
                    note_taker.db_delete(None, None, False, None, None, False, True)
                    return userin.say("All reminders deleted")
        return None







