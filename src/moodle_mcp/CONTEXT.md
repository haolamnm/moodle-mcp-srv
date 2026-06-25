# Moodle MCP Domain

Domain language for the Moodle MCP server. Every concept has one canonical name.

## Language

**Course**:
A Moodle course the user is enrolled in. Has ID, fullname, shortname, summary.
_Avoid_: Class, subject, module

**Site Info**:
Authenticated Moodle site and current-user metadata returned by the Web Service entrypoint.
_Avoid_: Status, health, instance info

**Assignment**:
A graded coursework item with due/cutoff dates, grade, and submission state.
_Avoid_: Homework, task, exercise

**Submission Status**:
The submission state (submitted, draft, noattempt) and grading status (graded, notgraded) of an Assignment.
_Avoid_: Hand-in status, deliverable state

**Quiz**:
A timed assessment with open/close dates, attempt tracking, and question-by-question review.
_Avoid_: Test, exam

**Quiz Attempt**:
One attempt at a Quiz with timestamps, state, and grade.
_Avoid_: Quiz try, submission

**Quiz Question Review**:
Per-question breakdown: your answer, correct answer, marks awarded.
_Avoid_: Quiz feedback, answer review, question breakdown

**Grade**:
A score/result on an Assignment or Quiz. Represented as raw, percentage, and letter form.
_Avoid_: Score, mark

**Forum**:
A discussion board. Types: news (announcements, instructor-only post) and general.
_Avoid_: Board, thread group, channel

**Forum Discussion**:
A thread within a Forum with author, post count, and pin status.
_Avoid_: Topic, thread

**Announcement**:
A post in a news-type Forum.
_Avoid_: News post, broadcast

**Calendar Event**:
An upcoming event across all Courses with start time and description. Also the personal (user) event created by `create_calendar_event`.
_Avoid_: Schedule item, reminder

**Activity Completion**:
The completion state of a Course module (complete/incomplete), read via progress and set manually by `mark_activity_complete` where manual completion is enabled.
_Avoid_: Progress flag, done status

**Dashboard Summary**:
Aggregated morning brief: overdue items, due today/week, new grades.
_Avoid_: Digest, homepage, overview

**Moodle Feature**:
An app-level capability mapped to required Moodle Web Service Function Names for diagnostics and friendly availability errors.
_Avoid_: Permission, capability, authorization

**Access Error**:
A runtime Moodle refusal of an otherwise-available call (e.g. `accessexception`), distinct from a missing Moodle Feature. Moodle enforces it; the server never authorizes anything.
_Avoid_: Permission denied, forbidden, unauthorized
