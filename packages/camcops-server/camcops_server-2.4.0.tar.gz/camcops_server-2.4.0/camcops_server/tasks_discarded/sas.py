#!/usr/bin/env python

"""
camcops_server/tasks_discarded/sas.py

===============================================================================

    Copyright (C) 2012-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CamCOPS.

    CamCOPS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CamCOPS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CamCOPS. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

**SAS task.**

"""

_ = '''

from typing import Any, Dict, List, Tuple, Type

from cardinal_pythonlib.stringfunc import strseq
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.sqltypes import Integer

from camcops_server.cc_modules.cc_constants import CssClass
from camcops_server.cc_modules.cc_db import add_multiple_columns
from camcops_server.cc_modules.cc_request import CamcopsRequest
from camcops_server.cc_modules.cc_summaryelement import SummaryElement
from camcops_server.cc_modules.cc_task import (
    get_from_dict,
    Task,
    TaskHasPatientMixin,
)
from camcops_server.cc_modules.cc_text import SS
from camcops_server.cc_modules.cc_trackerhelpers import TrackerInfo


# =============================================================================
# SAS
# =============================================================================

class SasMetaclass(DeclarativeMeta):
    # noinspection PyInitNewSignature
    def __init__(cls: Type['Sas'],
                 name: str,
                 bases: Tuple[Type, ...],
                 classdict: Dict[str, Any]) -> None:
        add_multiple_columns(cls, "q", 1, cls.NQUESTIONS)
        super().__init__(name, bases, classdict)


class Sas(TaskHasPatientMixin, Task,
          metaclass=SasMetaclass):
    tablename = "sas"
    shortname = "SAS"
    provides_trackers = True

    NQUESTIONS = 10
    TASK_FIELDS = strseq("q", 1, NQUESTIONS)
    MAX_TOTAL = 40

    @staticmethod
    def longname(req: "CamcopsRequest") -> str:
        _ = req.gettext
        return _("Simpson–Angus Extrapyramidal Side Effects Scale")

    def get_trackers(self, req: CamcopsRequest) -> List[TrackerInfo]:
        return [TrackerInfo(
            value=self.total_score(),
            plot_label="SAS total score",
            axis_label="Total score (out of {})".format(self.MAX_TOTAL),
            axis_min=-0.5,
            axis_max=self.MAX_TOTAL + 0.5
        )]

    def get_summaries(self, req: CamcopsRequest) -> List[SummaryElement]:
        return self.standard_task_summary_fields() + [
            SummaryElement(
                name="total",
                coltype=Integer(),
                value=self.total_score(),
                comment="Total score (out of {})".format(self.MAX_TOTAL)
            ),
        ]

    def is_complete(self) -> bool:
        return self.are_all_fields_complete(self.TASK_FIELDS)

    def total_score(self) -> int:
        return self.sum_fields(self.TASK_FIELDS)

    def get_task_html(self, req: CamcopsRequest) -> str:
        score = self.total_score()
        answer_dicts = []
        for q in range(1, self.NQUESTIONS + 1):
            d = {None: "?"}
            for option in range(0, 5):
                d[option] = self.wxstring(req, "q" + str(q) + "_option" +
                                          str(option))
            answer_dicts.append(d)
        h = """
            <div class="{CssClass.SUMMARY}">
                <table class="{CssClass.SUMMARY}">
                    {is_complete}
                    <tr>
                        <td>{total_score_str}</td>
                        <td><b>{score}</b> / {max_total}</td>
                    </tr>
                </table>
            </div>
            <table class="{CssClass.TASKDETAIL}">
                <tr>
                    <th width="30%">Question</th>
                    <th width="70%">Answer</th>
                </tr>
        """.format(
            CssClass=CssClass,
            is_complete=self.get_is_complete_tr(req),
            total_score_str=req.sstring(SS.TOTAL_SCORE),
            score=score,
            max_total=self.MAX_TOTAL,
        )
        for q in range(1, self.NQUESTIONS + 1):
            h += """<tr><td>{}</td><td><b>{}</b></td></tr>""".format(
                self.wxstring(req, "q" + str(q) + "_s"),
                get_from_dict(answer_dicts[q - 1], getattr(self, "q" + str(q)))
            )
        h += """
            </table>
        """
        return h

'''
