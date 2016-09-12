# Exceptions
class AlarmNotFound(Exception):
    pass

class AlarmNotAdded(Exception):
    pass

class InvalidData(Exception):
    pass

# Start here

class Alarm(object):
    """Implements an Alarm function. Alarms can be registered and inspected"""

    def __init__(self):
        self.alarms = dict()
        self.current_id = 0
    
    def list(self):
        """ return list of alarms """
        return repr(self.alarms)
 
    def add(self, title, fire_time, repeat=False):
        """ add new alarm to the list """
        try:
            self.alarms[self.current_id] = { 'title': title,
                                        'fire_time': fire_time,
                                        'repeat': bool(repeat) }
            return self.current_id
        except KeyError:
            raise AlarmNotAdded
        finally:
            self.current_id += 1
 
    def update(self, id, title=None, fire_time=None, repeat=False):
        """ update alarm by its id, with optionally new data """

        try:
            self.alarms[id] = { 'title': title,
                                'fire_time': fire_time,
                                'repeat': bool(repeat) }
        except KeyError:
            raise AlarmNotFound
        except ValueError:
            raise InvalidData
 
    def remove(self, id):
        """ remove alarm by its id """
        try:
            self.alarms.pop(id)
        except KeyError:
            raise AlarmNotFound
 
    def clear(self):
        """ remove all alarms """
        self.alarms.clear()
 
    def count(self):
        """ return count of alarms """
        return len(self.alarms)
 
    def get(self, id):
        """ get an alarm by its id """
        try:
            return self.alarms[id]
        except KeyError:
            raise AlarmNotFound
