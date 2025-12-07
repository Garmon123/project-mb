
import requests
import time

BASE_URL = "http://localhost:5000"
current_token = None
current_user_id = None


def register_user(username=None, password=None, interactive=True):
    global current_token, current_user_id

    if interactive:
        print("\nRegistration")
        if username is None:
            username = input("Enter username: ").strip()
        if password is None:
            password = input("Enter password: ").strip()

    if not username:
        print("Username cannot be empty!")
        return None, None

    if not password:
        print("Password cannot be empty!")
        return None, None

    data = {"name": username, "password": password}

    try:
        response = requests.post(
            f"{BASE_URL}/api/users/register",
            json=data,
            timeout=5
        )

        if interactive:
            print(f"Status: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            if interactive:
                print("Registration successful!")
                print(f"Name: {result['name']}")
                print(f"ID: {result['user_id']}")

            current_token = result.get('access_token')
            current_user_id = result['user_id']
            return result.get('access_token'), result['user_id']

        elif response.status_code == 409:
            if interactive:
                print("User with this name already exists!")
        else:
            if interactive:
                print(f"Error: {response.text}")

    except requests.exceptions.ConnectionError:
        if interactive:
            print("Cannot connect to localhost:5000")
    except Exception as e:
        if interactive:
            print(f"Error: {e}")

    return None, None


def login_user(username=None, password=None, interactive=True):
    global current_token, current_user_id

    if interactive:
        print("\nLogin")
        if username is None:
            username = input("Username: ").strip()
        if password is None:
            password = input("Password: ").strip()

    data = {"name": username, "password": password}

    try:
        response = requests.post(
            f"{BASE_URL}/api/users/login",
            json=data,
            timeout=5
        )

        if interactive:
            print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if interactive:
                print("Login successful!")
                print(f"Name: {result['name']}")
                print(f"ID: {result['user_id']}")

            current_token = result.get('access_token')
            current_user_id = result['user_id']
            return result.get('access_token'), result['user_id']

        else:
            if interactive:
                print("Invalid username or password!")

    except requests.exceptions.ConnectionError:
        if interactive:
            print("Cannot connect to server!")
    except Exception as e:
        if interactive:
            print(f"Error: {e}")

    return None, None


def get_all_users(interactive=True):
    global current_token

    if interactive and not current_token:
        print("Please authorize first!")
        return None

    if not current_token:
        return None

    if interactive:
        print("\nAll users")

    headers = {"Authorization": f"Bearer {current_token}"}

    try:
        response = requests.get(
            f"{BASE_URL}/api/users",
            headers=headers,
            timeout=5
        )

        if interactive:
            print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if interactive:
                print(f"Users found: {result['count']}")
                for i, user in enumerate(result['users'], 1):
                    print(f"{i}. {user['name']}")
                    print(f"   ID: {user['id']}")
            return result
        else:
            if interactive:
                print(f"Error: {response.json().get('error', 'Unknown error')}")

    except Exception as e:
        if interactive:
            print(f"Error: {e}")

    return None


def get_my_info(interactive=True):
    global current_token, current_user_id

    if interactive and not current_token:
        print("Please authorize first!")
        return None

    if not current_token:
        return None

    if interactive:
        print("\nMy information")

    headers = {"Authorization": f"Bearer {current_token}"}

    try:
        response = requests.get(
            f"{BASE_URL}/api/users/me",
            headers=headers,
            timeout=5
        )

        if interactive:
            print(f"Status: {response.status_code}")

        if response.status_code == 200:
            user = response.json()
            if interactive:
                print(f"Name: {user['name']}")
                print(f"ID: {user['id']}")
            return user
        else:
            if interactive:
                print(f"Error: {response.json().get('error', 'Unknown error')}")

    except Exception as e:
        if interactive:
            print(f"Error: {e}")

    return None


def get_user_by_id(user_id=None, interactive=True):
    global current_token

    if interactive and not current_token:
        print("Please authorize first!")
        return None

    if not current_token:
        return None

    if interactive:
        print("\nFind user by ID")
        if user_id is None:
            user_id = input("Enter user ID: ").strip()

    if not user_id:
        if interactive:
            print("ID cannot be empty!")
        return None

    headers = {"Authorization": f"Bearer {current_token}"}

    try:
        response = requests.get(
            f"{BASE_URL}/api/users/{user_id}",
            headers=headers,
            timeout=5
        )

        if interactive:
            print(f"Status: {response.status_code}")

        if response.status_code == 200:
            user = response.json()
            if interactive:
                print("User found!")
                print(f"Name: {user['name']}")
                print(f"ID: {user['id']}")
            return user
        elif response.status_code == 404:
            if interactive:
                print("User not found!")
        else:
            if interactive:
                print(f"Error: {response.json().get('error', 'Unknown error')}")

    except Exception as e:
        if interactive:
            print(f"Error: {e}")

    return None


def update_my_info(new_name=None, new_password=None, interactive=True):
    global current_token

    if interactive and not current_token:
        print("Please authorize first!")
        return False

    if not current_token:
        return False

    if interactive:
        print("\nUpdate data")
        if new_name is None:
            new_name = input("New username (leave empty to keep current): ").strip()
        if new_password is None:
            new_password = input("New password (leave empty to keep current): ").strip()

    data = {}
    if new_name:
        data['name'] = new_name
    if new_password:
        data['password'] = new_password

    if not data:
        if interactive:
            print("Nothing to update!")
        return False

    headers = {
        "Authorization": f"Bearer {current_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(
            f"{BASE_URL}/api/users/me",
            headers=headers,
            json=data,
            timeout=5
        )

        if interactive:
            print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if interactive:
                print("Data updated!")
                print(f"New name: {result['name']}")
                print(f"ID: {result['id']}")
            return True
        else:
            if interactive:
                error = response.json().get('error', 'Unknown error')
                print(f"Error: {error}")

    except Exception as e:
        if interactive:
            print(f"Error: {e}")

    return False


def delete_my_account(interactive=True):
    global current_token, current_user_id

    if interactive and not current_token:
        print("Please authorize first!")
        return False

    if not current_token:
        return False

    if interactive:
        print("\nDelete account")
        print("Warning: This action is irreversible!")
        print("Your account and all data will be deleted.")
        confirm = input("\nAre you sure? (yes/NO): ").strip().lower()

        if confirm != 'yes':
            print("Deletion canceled.")
            return False
    else:
        confirm = 'yes'

    if confirm != 'yes':
        return False

    headers = {"Authorization": f"Bearer {current_token}"}

    try:
        response = requests.delete(
            f"{BASE_URL}/api/users/me",
            headers=headers,
            timeout=5
        )

        if interactive:
            print(f"Status: {response.status_code}")

        if response.status_code == 200:
            if interactive:
                print("Account deleted!")
            current_token = None
            current_user_id = None
            return True
        else:
            if interactive:
                print(f"Error: {response.json().get('error', 'Unknown error')}")

    except Exception as e:
        if interactive:
            print(f"Error: {e}")

    return False


def test_all_functions():
    test_results = []

    try:
        print("Test user registration")

        test_username = f"testuser_{int(time.time())}"
        test_password = "TestPassword123!"

        print(f"Username: {test_username}")
        print(f"Password: {test_password}")

        token, user_id = register_user(test_username, test_password, interactive=False)

        if token and user_id:
            print("Registration successful!")
            test_results.append(("Registration", "Success"))
        else:
            print("Registration failed!")
            test_results.append(("Registration", "Error"))
            return

        print("\nGet my information")

        user_info = get_my_info(interactive=False)
        if user_info:
            print(f"Information received: {user_info['name']} ({user_info['id']})")
            test_results.append(("Get my information", "Success"))
        else:
            print("Could not get information")
            test_results.append(("Get my information", "Error"))

        print("\nGet all users")

        all_users = get_all_users(interactive=False)
        if all_users:
            print(f"Users found: {all_users['count']}")
            test_results.append(("Get all users", "Success"))
        else:
            print("Could not get user list")
            test_results.append(("Get all users", "Error"))

        print("\nFind user by ID")

        found_user = get_user_by_id(user_id, interactive=False)
        if found_user:
            print(f"User found: {found_user['name']}")
            test_results.append(("Find user by ID", "Success"))
        else:
            print("Could not find user")
            test_results.append(("Find user by ID", "Error"))

        print("\nUpdate data")

        new_username = f"updated_{test_username}"
        if update_my_info(new_username, None, interactive=False):
            print(f"Data updated: {new_username}")
            test_results.append(("Update data", "Success"))

            updated_info = get_my_info(interactive=False)
            if updated_info and updated_info['name'] == new_username:
                print(f"Verification: name changed to {new_username}")
            else:
                print("Name did not change after update")
        else:
            print("Could not update data")
            test_results.append(("Update data", "Error"))

        print("\nDelete account")

        if delete_my_account(interactive=False):
            print("Account deleted")
            test_results.append(("Delete account", "Success"))
        else:
            print("Could not delete account")
            test_results.append(("Delete account", "Error"))

        print("\nCheck deleted account")

        token, user_id = login_user(new_username, test_password, interactive=False)
        if token:
            print("Account was not deleted (login successful)")
        else:
            print("Account successfully deleted (login failed)")
            test_results.append(("Check deleted account", "Success"))

        print("\nTest results")

        success_count = 0
        for test_name, result in test_results:
            status = "Success" if result == "Success" else "Failed"
            print(f"{test_name}: {status}")
            if result == "Success":
                success_count += 1

        print(f"\nSuccessfully completed: {success_count}/{len(test_results)} tests")

        if success_count == len(test_results):
            print("\nAll tests passed successfully!")
        else:
            print(f"\nFailed tests: {len(test_results) - success_count}")

    except Exception as e:
        print(f"Error during testing: {e}")



def main():
    test_all_functions()


if __name__ == "__main__":
    print("Checking connection to localhost:5000...")
    try:
        response = requests.get("http://localhost:5000/api", timeout=3)
        if response.status_code == 200:
            print("Server is available!")
        else:
            print("Server responds but with error")
    except requests.exceptions.ConnectionError:
        print("Server is not available!")
        print("\nStart server now? (y/n): ")
        if input().strip().lower() == 'y':
            print("Starting server...")
            import subprocess

            subprocess.Popen(["python", "run.py"])
            print("Server is starting... Wait 3 seconds.")
            time.sleep(3)

    main()
