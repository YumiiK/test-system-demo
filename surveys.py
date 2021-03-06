import json


class Question:
    """Question on a questionnaire."""

    def __init__(self, index, question, choices=None, answer=None, image=None, allow_text=False):
        """Create question (assume Yes/No for choices."""

        if not choices:
            choices = ["Yes", "No"]
        self.qindex = index
        self.question = question
        self.choices = choices
        self.answer = answer
        self.image = image
        self.allow_text = allow_text


class Survey:
    """Questionnaire."""

    def __init__(self, title, instructions, questions):
        """Create questionnaire."""

        self.title = title
        self.instructions = instructions
        self.questions = questions


class ResultList:
    def __init__(self, set_no, t_no, ans_time, t_index, c_a, p_a, ifright):
        self.set_no = set_no
        self.t_no = t_no
        self.ans_time = ans_time
        self.t_index = t_index
        self.c_a = c_a
        self.p_a = p_a
        self.ifright = ifright

# trial = Survey(
#     "Trial",
#     "In this section, we have prepared several questions to familiarize you with them. After you choose the "
#     "answer, the correct answer will appear.",
#     [
#         Question("Have you shopped here before?"),
#         Question("Did someone else shop with you today?"),
#         Question("On average, how much do you spend a month on frisbees?",
#                  ["Less than $10,000", "$10,000 or more"]),
#         Question("Are you likely to shop here again?"),
#     ])

# test = Survey(
#     "Test",
#     "In this section, you have 45 questions to answer. After every 15 questions, you can take a rest, then continue. "
#     "Begin the formal test now!",
#     [
#         Question("Do you ever dream about code?"),
#         Question("Do you ever have nightmares about code?"),
#         Question("Do you prefer porcupines or hedgehogs?",
#                  ["Porcupines", "Hedgehogs"]),
#         Question("Which is the worst function name, and why?",
#                  ["do_stuff()", "run_me()", "wtf()"],
#                  allow_text=True),
#     ]
# )


# surveys = {
#     "trial": trial,
#     "test": test,
# }