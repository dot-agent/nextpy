# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

#credit: Martin Schroder
#research paper: https://arxiv.org/abs/2306.03197
#organization: Swedish Embedded Consulting Group Research
#linkedin: martinschroder 
#email: martin.schroder@swedishembedded.com
import json
from pathlib import Path

import pkg_resources as pg
from dotagent import compiler
from dotagent.llms._openai import OpenAI

compiler.llm = OpenAI("gpt-3.5-turbo")

class AutoScrum:
    def __init__(self, path):
        self.featurizer = self.load_program("featurizer")
        self.storylizer = self.load_program("storylizer")
        self.goalmaker = self.load_program("goalmaker")
        self.clarifier = self.load_program("clarifier")
        self.acceptance = self.load_program("acceptance")
        self.taskalizer = self.load_program("taskalizer")
        self.requalizer = self.load_program("requalizer")
        self.planner = self.load_program("planner")
        if not Path(path).exists():
            self.reset()
            self.save(path)
        self.data = self.load_data(path)

    def reset(self):
        self.data = {
            "product": "Your product name",
            "vision": "Your product vision",
            "niche": "Your product niche",
            "current_state": {},
            "desired_state": {},
            "plan": [],
            "requirements": [],
            "sprint_duration": "2 weeks",
            "features": [],
            "stories": [],
            "avoid": []
        }

    def load_data(self, path):
        """Loads data json file."""
        return json.loads(Path(path).read_text())

    def load_program(self, name: str):
        path = pg.resource_filename(__name__, f'data/{name}.hbs')
        return compiler(Path(path).read_text(), silent=True)

    def save(self, path):
        Path(path).write_text(json.dumps(self.data, indent=4))


    def gen_plan(self, count:int):
        prog = self.planner(
            current_state=self.data["current_state"],
            desired_state=self.data["desired_state"],
            plan=[p["task"] for p in self.data["plan"]],
            count=count
        )
        try:
            # print(prog)
            obj = json.loads(prog["response"])
            return obj
        except:
            # print(prog)
            print("Error: JSON conversion failed")
        return []

    def add_plan(self, steps: list):
        self.data["plan"].extend(steps)

    @property
    def plan(self):
        return self.data["plan"]


    def gen_requirements(self, count:int):
        prog = self.requalizer(
            product=self.data["product"],
            vision=self.data["vision"],
            niche=self.data["niche"],
            current_state=self.data["current_state"],
            desired_state=self.data["desired_state"],
            requirements=[f["name"] for f in self.data["requirements"]],
            count=count
        )
        try:
            # print(prog)
            obj = json.loads(prog["response"])
            return obj
        except:
            print(prog)
            print("Error: JSON conversion failed")
        return []

    def add_requirements(self, reqs: list):
        self.data["requirements"].extend(reqs)

    @property
    def requirements(self):
        return self.data["requirements"]

    def gen_features(self, count:int):
        prog = self.featurizer(
            product=self.data["product"],
            vision=self.data["vision"],
            requirements=[req["description"] for req in self.data["requirements"]],
            story_features=[s["feature"] for s in self.data["stories"]],
            features = [feature["name"] for feature in self.data["features"]],
            avoid=self.data["avoid"],
            count=count
        )
        try:
            print(prog)
            obj = json.loads(prog["response"])
            return obj
        except:
            print(prog)
            print("Error: JSON conversion failed")
        return []

    def add_features(self, features: list):
        self.data["features"].extend(features)

    @property
    def features(self):
        return self.data["features"]

    def gen_stories(self, count:int):
        prog = self.storylizer(
            product=self.data["product"],
            niche=self.data["niche"],
            vision=self.data["vision"],
            features = [feature["name"] for feature in self.data["features"]],
            current_state=self.data["current_state"],
            desired_state=self.data["desired_state"],
            stories = [story["name"] for story in self.data["stories"]],
            count=count
        )
        print(prog)
        return json.loads(prog["response"])

    def add_stories(self, stories: list):
        self.data["stories"].extend(stories)

    @property
    def stories(self):
        return self.data["stories"]

    def gen_goals(self, count:int):
        prog = self.goalmaker(
            project=self.data["project"],
            sprint_duration=self.data["sprint_duration"],
            product_vision=self.data["goal"],
            backlog = [story["name"] for story in self.data["stories"]],
            goals = [goal["title"] for goal in self.data["goals"]],
            count=count
        )
        print(prog)
        return json.loads(prog["goals"])

    def add_goals(self, goals: list):
        self.data["goals"].extend(goals)

    @property
    def goals(self):
        return self.data["goals"]

    def gen_acceptance_criteria(self, story, count:int):
        prog = self.acceptance(
            product=self.data["product"],
            requirements=[req["description"] for req in self.data["requirements"]],
            story=story,
            count=count
        )
        print(prog)
        return json.loads(prog["response"])

    def gen_tasks(self, story, count:int):
        prog = self.taskalizer(
            product=self.data["product"],
            story=story,
            count=count
        )
        print(prog)
        return json.loads(prog["response"])

    def gen_clarification(self, story, count:int):
        prog = self.clarifier(
            story=story,
            completed_tasks=[],
            resources=[],
            count=count
        )
        print(prog)
        return json.loads(prog["response"])


