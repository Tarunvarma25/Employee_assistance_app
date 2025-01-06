import requests

def chat():
    print("Welcome to Employee Assistance Chat!")
    print("Ask for help with a skill or task.\n")

    while True:
        query = input("You: ")
        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        response = requests.get("http://127.0.0.1:5000/search", params={"query": query})
        if response.status_code == 200:
            employees = response.json().get("employees", [])
            if employees:
                print("\nThese employees have knowledge or experience in", query + ":\n")
                for emp in employees:
                    print(f"- {emp['name']}")
            else:
                print(f"No employees found with expertise in {query}.")
        else:
            print("Error: ", response.json().get("error"))

if __name__ == '__main__':
    chat()
