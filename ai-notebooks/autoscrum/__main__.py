# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.



import argparse

from autoscrum.autoscrum import AutoScrum


def main():
    parser = argparse.ArgumentParser(description='AutoScrum Demo')
    parser.add_argument('-f', '--data-file', type=str, help='Scrum data json file')
    subparsers = parser.add_subparsers(dest="command")

    stories_parser = subparsers.add_parser("stories")
    stories_parser.add_argument("-n", "--count", type=int, default=3)

    features_parser = subparsers.add_parser("features")
    features_parser.add_argument("-n", "--count", type=int, default=3)

    goals_parser = subparsers.add_parser("goals")
    goals_parser.add_argument("-n", "--count", type=int, default=3)

    clarify_parser = subparsers.add_parser("clarify")
    clarify_parser.add_argument("-n", "--count", type=int, default=3)

    subparser = subparsers.add_parser("acceptance")
    subparser.add_argument("-n", "--count", type=int, default=3)

    subparser = subparsers.add_parser("tasks")
    subparser.add_argument("-n", "--count", type=int, default=3)

    subparser = subparsers.add_parser("requirements")
    subparser.add_argument("-n", "--count", type=int, default=3)

    subparser = subparsers.add_parser("plan")
    subparser.add_argument("-n", "--count", type=int, default=1)

    subparser = subparsers.add_parser("init")

    args = parser.parse_args()

    print(f"Using datafile: {args.data_file}")
    autoscrum = AutoScrum(args.data_file)


    if args.command == "init":
        autoscrum.reset()
        autoscrum.save(args.data_file)

    elif args.command == "plan":
        print("Existing plan: ")
        for i,f in enumerate(autoscrum.plan):
            print(f"{i}: {f['task']}")

        res = autoscrum.gen_plan(count=args.count)

        print("Identified new steps: ")
        for i,f in enumerate(res):
            print(f"{i}: {f['task']}")

        autoscrum.add_plan(res)
        autoscrum.save(args.data_file)

    elif args.command == "requirements":
        print("Existing requirements: ")
        for i,f in enumerate(autoscrum.requirements):
            print(f"{i}: {f['name']}")

        new_reqs = autoscrum.gen_requirements(count=args.count)

        print("Identified new requirements: ")
        for i,f in enumerate(new_reqs):
            print(f"{i}: {f['name']}")

        autoscrum.add_requirements(new_reqs)
        autoscrum.save(args.data_file)

    elif args.command == "features":
        print("Existing features: ")
        for i,f in enumerate(autoscrum.features):
            print(f"{i}: {f['name']}")

        new_features = autoscrum.gen_features(count=args.count)

        print("Identified new features: ")
        for i,f in enumerate(new_features):
            print(f"{i}: {f['name']}")

        autoscrum.add_features(new_features)
        autoscrum.save(args.data_file)
    elif args.command == "stories":
        print("Existing stories: ")
        for i,f in enumerate(autoscrum.stories):
            print(f"{i}: {f['name']}")

        new_stories = autoscrum.gen_stories(count=args.count)

        print("New stories: ")
        for i,f in enumerate(new_stories):
            print(f"{i}: {f['name']}")

        autoscrum.add_stories(new_stories)
        autoscrum.save(args.data_file)
    elif args.command == "goals":
        print("Existing sprint goals: ")
        for i,f in enumerate(autoscrum.goals):
            print(f"{i}: {f['title']}")

        new_goals = autoscrum.gen_goals(count=args.count)

        print("New goals: ")
        for i,f in enumerate(new_goals):
            print(f"{i}: {f['title']}")

        autoscrum.add_goals(new_goals)
        autoscrum.save(args.data_file)

    elif args.command == "tasks":
        for story in autoscrum.data["stories"]:
            if ("tasks" in story) and (len(story["tasks"]) > 0):
                continue

            res = autoscrum.gen_tasks(story=story, count=args.count)

            print("New tasks: ")
            for i,f in enumerate(res):
                print(f"{i}: {f['task']}")
            story["tasks"] = res
            autoscrum.save(args.data_file)

    elif args.command == "acceptance":
        for story in autoscrum.data["stories"]:
            if ("acceptance" in story) and (len(story["acceptance"]) > 0):
                continue

            res = autoscrum.gen_acceptance_criteria(story=story, count=args.count)

            print("New criteria: ")
            for i,f in enumerate(res):
                print(f"{i}: {f}")
            story["acceptance"] = res
            autoscrum.save(args.data_file)


    elif args.command == "clarify":
        for story in autoscrum.data["stories"]:
            if ("resources" in story) and (len(story["resources"]) > 0):
                continue

            res = autoscrum.gen_clarification(story, count=args.count)

            print("New clarification: ")
            for i,f in enumerate(res):
                print(f"{i}: {f['question']}")

            story["resources"] = res
            autoscrum.save(args.data_file)

        #autoscrum.add_goals(new_goals)
        #autoscrum.save(args.data_file)

    #data["stories"].extend(new_stories)
    #print(json.dumps(data, indent=4))

