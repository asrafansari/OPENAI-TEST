import os
import shutil
import pygit2

def main():
    # Set the repository name, URL, and access token
    repo_name = os.environ.get('REPO_NAME')
    repo_url = os.environ.get('REPO_URL')
    access_token = os.environ.get('GITHUB_ACCESS_TOKEN')  # Replace with your actual access token
    
    # Call the clone function
    success, error = clone(repo_name, repo_url, access_token)
    
    if success:
        print(f"The repository {repo_name} has been cloned successfully.")
    else:
        print(error)


def clone(repo_name, repo_url, access_token):
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        repo_path = os.path.join(current_dir, repo_name)
        
        # Remove the directory if it already exists
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        
        # Set up authentication for cloning
        auth_method = 'x-access-token'
        callbacks = pygit2.RemoteCallbacks(pygit2.UserPass(auth_method, access_token))
        
        # Clone the repository
        pygit2.clone_repository(url=repo_url, path=repo_path, callbacks=callbacks, bare=False)
        return True, None
    except Exception as e:
        return False, {"errors": f'Clone failed: {e}'}


# Call the main method if this script is executed
if __name__ == '__main__':
    main()