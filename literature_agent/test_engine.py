import time
import json

from literature_agent.router.engine import LiteratureEngine

def pretty_print_state(state):
    print("\n==============================")
    print("ENGINE STATUS:", state["engine"]["status"])
    print("Total Processed:", state["engine"]["total_processed"])
    print("Total Routed:", state["engine"]["total_routed"])
    print("Total Discarded:", state["engine"]["total_discarded"])

    if state["current_processing"]:
        cp = state["current_processing"]
        print("\n--- CURRENT PROCESSING ---")
        print("Paper:", cp["title"])
        print("Stage:", cp["stage"])

        if cp["extraction"]:
            print("Extraction:", cp["extraction"])

        if cp["project_scores"]:
            print("Project Scores:")
            for name, score_data in cp["project_scores"].items():
                print(f"  {name}: {score_data['score']}")

    print("\n--- PROJECT SUMMARY ---")
    for name, proj in state["projects"].items():
        print(f"{name}: {proj['total_papers']} papers")

    print("==============================\n")


def main():
    engine = LiteratureEngine()

    print("Starting engine...")
    engine.start()

    try:
        while True:
            state = engine.get_state()
            pretty_print_state(state)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nStopping engine...")
        engine.reset()
        print("Reset complete.")


if __name__ == "__main__":
    main()
