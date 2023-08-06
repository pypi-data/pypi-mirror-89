'''
 rmtoo
   Free and Open Source Requirements Management Tool

  Status of a requirement

 (c) 2010-2012,2017 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''
import abc

from stevedore import extension

from rmtoo.lib.DateUtils import parse_date, format_date
from rmtoo.lib.RMTException import RMTException


# pylint: disable=too-few-public-methods
class RequirementStatusBase(object):
    """Base class for StatusBase"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_output_string(self):
        """Return the output string"""
        return


# pylint: disable=abstract-method
class RequirementStatusBaseExt(RequirementStatusBase):
    """Extended Base class for StatusBase"""

    def __init__(self, person, date):
        """Initialize the extended StatusBase with the given parameters"""
        self.__person = person
        self.__date = date

    def get_person(self):
        """Return the person"""
        return self.__person

    def get_date_str(self):
        """Return the date as string"""
        if self.__date is None:
            return ""
        return format_date(self.__date)

    def get_date(self):
        """Return the date"""
        return self.__date


class RequirementStatusNotDone(RequirementStatusBase):
    """Class representing the StatusNotDone"""
    tval = "not done"

    def __init__(self, _config, rid, t):
        if t != self.tval:
            raise RMTException(92, "%s: Not done contains "
                               "additional data '%s'" % (rid, t))

    def get_output_string(self):
        return self.tval


class RequirementStatusAssigned(RequirementStatusBaseExt):
    """Class representing the StatusAssigned"""
    tval = "assigned"

    def __init__(self, _config, rid, txt):
        txt_split = txt.split(":")

        if len(txt_split) != 3:
            raise RMTException(93, "%s: Assigned values invalid '%s'"
                               % (rid, txt))
        assert txt_split[0] == self.tval
        RequirementStatusBaseExt.__init__(
            self, txt_split[1], parse_date(rid, txt_split[2]))

    def get_output_string(self):
        """Generate output string"""
        return "%s (%s, %s)" % (self.tval, self.get_person(),
                                self.get_date_str())


class RequirementStatusFinished(RequirementStatusBaseExt):
    """Class representing the StatusFinished"""
    tval = "finished"

    def __init__(self, _config, rid, txt):
        if txt == self.tval:
            # This is the old way: only 'finished' is specified.
            person = None
            date = None
            self.duration = None
        else:
            txt_split = txt.split(":")
            if len(txt_split) != 4:
                raise RMTException(94, "%s: Finished values invalid [%s]"
                                   % (rid, txt_split))
            assert txt_split[0] == self.tval
            person = txt_split[1]
            date = parse_date(rid, txt_split[2])
            assert txt_split[3][-1] == 'h'
            self.duration = int(txt_split[3][:-1])
        RequirementStatusBaseExt.__init__(self, person, date)

    def get_duration(self):
        """Return the duration of the finished task"""
        return self.duration

    def get_output_string(self):
        """Generate output string"""
        return "%s (%s, %s, %s h)" % (self.tval, self.get_person(),
                                      self.get_date_str(), self.duration)


class RequirementsStatusFactory(object):
    """Factory for different RequirementStatus using stevedore"""

    def __init__(self):
        self.__plugin_manager = extension.ExtensionManager(
            namespace='rmtoo.input.requirement_status',
            invoke_on_load=False)

    def generate(self, config, rid, txt):
        """Generate a RequirementsStatus object based on the parameters"""
        txt_split = txt.split(':')
        try:
            return self.__plugin_manager[txt_split[0]].plugin(
                config, rid, txt)
        except KeyError:
            raise RMTException(91, "%s: Status tag invalid '%s'" % (rid, txt))


REQ_STAT_FACTORY = RequirementsStatusFactory()


def create_requirement_status(config, rid, txt):
    """Factory function for the RequirementStatus"""
    return REQ_STAT_FACTORY.generate(config, rid, txt)
