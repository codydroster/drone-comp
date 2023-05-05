import argparse

def do_something():
    print("Doing something")

def do_something_else():
    print("Doing something else")

def main():
    parser = argparse.ArgumentParser(description="A script to demonstrate argparse usage")
    parser.add_argument("--task", choices=["task1", "task2"], help="Specify the task to perform")

    args = parser.parse_args()

    if args.task == "task1":
        do_something()
    elif args.task == "task2":
        do_something_else()
    else:
        print("No task specified. Use --task with 'task1' or 'task2' as an argument.")

if __name__ == "__main__":
    main()
